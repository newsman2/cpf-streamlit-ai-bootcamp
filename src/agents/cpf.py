from typing import Any

import streamlit as st
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, AgentState
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel

from helpers import chroma
from tools import office

OPENAI_MODEL = st.secrets["OPENAI_MODEL"]
MAX_OUTPUT_TOKENS = st.secrets["MAX_OUTPUT_TOKENS"]


class FileDescription(BaseModel):
    filename: str
    download_link: str


class State(AgentState):
    context: list[Document]
    collection_name: str


class RetrieveDocumentsMiddleware(AgentMiddleware[State]):
    state_schema = State

    def before_model(self, state: State) -> dict[str, Any] | None:
        collection_name = state["collection_name"]
        last_message = state["messages"][-1]

        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = chroma.get_collection(collection_name, embeddings_model)
        retrieved_docs = vector_store.similarity_search(last_message.text)

        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

        augmented_message_content = (
            f"{last_message.text}\n\n"
            "Use the following context to answer the query:\n"
            f"{docs_content}"
        )
        return {
            "messages": [
                last_message.model_copy(update={"content": augmented_message_content})
            ],
            "context": retrieved_docs,
        }


model = init_chat_model(
    OPENAI_MODEL, temperature=0, timeout=10, max_tokens=MAX_OUTPUT_TOKENS
)


def init_agent():
    agent = create_agent(
        model,
        tools=[office.create_word_doc],
        middleware=[RetrieveDocumentsMiddleware()],
    )
    return agent
