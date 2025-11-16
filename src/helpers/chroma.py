import streamlit as st
from langchain_chroma import Chroma

PERSIST_DIR = st.secrets["PERSIST_DIR"]


def get_collection(collection_name: str, embeddings) -> Chroma:
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    return vector_store


def get_vector_store(embeddings) -> Chroma:
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    return vector_store
