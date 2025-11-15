import os
import streamlit as st
from langchain.agents.middleware import dynamic_prompt, ModelRequest

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text

    persist_dir = "./chroma_langchain_db"

    # Load existing index if present
    if os.path.exists(persist_dir):
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = Chroma(
            embedding_function=embeddings_model,
            persist_directory=persist_dir,
        )

        retrieved_docs = vector_store.similarity_search(last_query)
        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

        system_message = (
            "You are a helpful assistant. Use the following context in your response:"
            f"\n\n{docs_content}"
        )

        return system_message
    else:
        st.error("Unable to retrieve from context. Please try again.")

        return None
