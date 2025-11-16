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
st.markdown(""" This Streamlit-based application enables users' to upload their
            PDF documents, process them into embeddings using LangChain, store
            them in a Chroma vector database, and retrieve relevant information
            through a conversational chat interface powered by an LLM. The
            Chroma vector database is stored locally in Streamlit community
            servers. Upon receiving the PDF document, the text will be
            extracted from the PDF and a single document is created for each
            PDF. Next, the document will undergo a chunking process using
            `RecursiveCharacterTextSplitter` with a chunk size of 1000 and
            chunk overlap of 200. Lastly, the chunked documents will be saved
            into Chroma vector store and persisted in a file directory. """)

st.subheader("General CPF Assistant")
st.subheader("Retrieval Augmented Generation (RAG)")
