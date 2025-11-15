import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="About"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About")
st.header("CPF Assistant")

st.subheader("Project Scope")
st.markdown("This project aims to build an interactive RAG-based chatbot platform using Streamlit. The system will allow users to upload PDF documents, process their content into embeddings using LangChain, store them in a Chroma vector database, and retrieve relevant information through a conversational chat interface powered by an LLM.")

st.subheader("Objectives")
st.markdown(""" 
            - Deliver and deploy a fully functional Chatbot to help users to learn more about CPF
            - Implement a Streamlit-based RAG Chatbot with document upload and Chroma vector storage
            - Deploy an LLM-based assistant that can answer questions using uploaded documents
            - Show users which documents are reference during RAG process
            """)
st.subheader("Data Sources")
st.markdown(""" - [CPF Data](https://www.cpf.gov.sg/member/infohub) """)

st.subheader("Features")
st.markdown(""" 
            - Retrieval Augmented Generation (RAG)
                - PDF document ingestion and parsing
                - Automatic text chunking and metadata extraction
                - Embedding generation using LLM embedding models
                - Chroma vector database for similarity search
                - Display of retrieved document chunks with source references
            """)

