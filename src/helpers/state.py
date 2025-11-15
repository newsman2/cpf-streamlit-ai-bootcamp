import streamlit as st


def ensure_session_states():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

