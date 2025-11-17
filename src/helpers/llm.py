import time

import streamlit as st
import tiktoken
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_openai.chat_models import ChatOpenAI
from openai import OpenAI

from helpers import chroma

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_MODEL = st.secrets["OPENAI_MODEL"]
MAX_OUTPUT_TOKENS = st.secrets["MAX_OUTPUT_TOKENS"]

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)
llm = init_chat_model(
    OPENAI_MODEL, temperature=0, timeout=10, max_tokens=MAX_OUTPUT_TOKENS
)


def make_retrieval_chain(collection_name: str, embeddings, llm_model=OPENAI_MODEL):
    from langchain_classic.chains import ConversationalRetrievalChain

    vector_store = chroma.get_collection(collection_name, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name=llm_model, temperature=0)
    chain = ConversationalRetrievalChain.from_llm(
        llm, retriever, return_source_documents=True
    )

    return chain


def generate_response(messages):
    # Use with chat models
    response = llm.stream(messages)

    for word in response:
        yield word
        time.sleep(0.05)


# def multi_query_retrieve(message):
#    from langchain.retrievers.multi_query import MultiQueryRetriever
#    from langchain_core.retrievers.multi_query import MultiQueryRetriever
#
#    persist_dir = "./chroma_langchain_db"
#
#    # Load existing index if present
#    if os.path.exists(persist_dir):
#        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
#        vector_store = Chroma(
#            embedding_function=embeddings_model,
#            persist_directory=persist_dir,
#        )
#        retriever_multiquery = MultiQueryRetriever.from_llm(
#            retriever=vectordb.as_retriever(),
#            llm=llm,
#        )
#        response = retriever_multiquery.stream(message)
#
#        for word in response:
#            yield word
#            time.sleep(0.05)
#    else:
#        st.error("Unable to find collection. Please try again.")


def get_embedding(input, model="text-embedding-3-small"):
    response = client.embeddings.create(input=input, model=model)
    return [x.embedding for x in response.data]


def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    return len(encoding.encode(text))


def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    value = " ".join([x.get("content") for x in messages])
    return len(encoding.encode(value))
