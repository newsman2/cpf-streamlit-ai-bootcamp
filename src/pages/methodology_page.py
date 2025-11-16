import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="Methodology")
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
st.image(
    image="./assets/flowchart-general.png",
    caption="Figure 1 - Flowchart for General CPF Assistant (Home page)",
)
st.markdown(
    """
    Figure 1 shows the data flow for the General CPF Assistant page.
    To use the application, one must enter a prompt only about Singapore Central Provident Fund (CPF).
    There is a system message that will guide the LLM to perform the following steps:

    ```
    Your task is to perform the following steps:

    Step 1 - To answer questions about Singapore Central Provident Fund (CPF).
    Step 2 - To provide a summary and translate the answer into Chinese.

    If you don't know the answer, just say that you don't know.

    If the question is not about CPF, politely inform them that you are tuned to only answer questions about CPF.
    The response MUST be in the following format:
    Answer:#### <step 1 output>
    回答(概括):#### <step 2 output>
    ```

    The system message does two things:
    1. To ONLY answer questions about Singapore Central Provident Fund (CPF).
    2. To provide a summary in Chinese

    """
)

st.subheader("Retrieval Augmented Generation (RAG)")
st.image(
    image="./assets/flowchart-rag.png",
    caption="Figure 2 Flowchart for RAG (Retrieval Page)",
)
st.markdown(
    """
 Figure 2 shows the data flow for the Retrieval Augmented Generation (RAG) page.
 To use the application RAG, one must upload a PDF document.
 The application will perform splitting, chunking, and embedding of the PDF document.
 The text chunks will then be stored in a Chroma vector store.
 After which the user can select a collection name and perform a query on the uploaded documents.
 The UI will display an output of the retrieved document chunks with source references.
 """
)
