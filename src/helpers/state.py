import os

import streamlit as st
from langchain_openai import OpenAIEmbeddings

from helpers import chroma, llm

OPENAI_MODEL = st.secrets["OPENAI_MODEL"]
PERSIST_DIR = st.secrets["PERSIST_DIR"]


def ensure_session_states():
    if "last_context" not in st.session_state:
        st.session_state.last_context = None
    if "collection_name_input" not in st.session_state:
        st.session_state.collection_name_input = ""
    if "cpf_assistant_chat_history" not in st.session_state:
        st.session_state.cpf_assistant_chat_history = []
    if "conversations_key" not in st.session_state:
        st.session_state.conversations_key = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

        if os.path.exists(PERSIST_DIR):
            vector_store = chroma.get_vector_store(embeddings_model)

            for collection in vector_store._client.list_collections():
                chain = llm.make_retrieval_chain(
                    collection.name, embeddings_model, llm_model=OPENAI_MODEL
                )
                st.session_state.conversations[collection.name] = chain
