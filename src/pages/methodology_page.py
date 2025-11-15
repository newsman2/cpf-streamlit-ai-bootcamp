import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Methodology"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology")

st.header("CPF Assistant")

st.subheader("Data flow")
st.markdown("""
            This Streamlit-based application enables users' to upload their PDF documents, process them into embeddings using LangChain, store them in a Chroma vector database, and retrieve relevant information through a conversational chat interface powered by an LLM. The Chroma vector database is stored locally in Streamlit community servers. Upon receiving the PDF document, the text will be extracted from the PDF and a single document is created for each PDF. Next, the document will undergo a chunking process using `RecursiveCharacterTextSplitter` with a chunk size of 1000 and chunk overlap of 200. Lastly, the chunked documents will be saved into Chroma vector store and persisted in a file directory.
            """)

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
