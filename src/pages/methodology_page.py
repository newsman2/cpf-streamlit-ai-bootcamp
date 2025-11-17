import streamlit as st

from helpers import utility

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="Methodology")

# Do not continue if check_password is not True.
if not utility.check_password():
    st.stop()
# endregion <--------- Streamlit App Configuration --------->

st.title("Methodology")

st.header("CPF Assistant")

st.subheader("Data flow")
st.markdown("""
            There are two data flows, home page and retrieval page in this application.

            **Home Page**

            In the home page, it is a General CPF Assistant that answers questions about
            Singapore Central Provident Fund. A summary in Chinese will also be
            displayed for users too.

            **Retrieval Page**

            In the retrieval page, it is a Retrieval Augmented Generation (RAG) page
            that allows users to upload a PDF document and perform a query on the
            uploaded documents. The application processes the documents into
            embeddings using LangChain, store them in a Chroma vector database, and
            retrieve relevant information through an agent RAG
            powered by an LLM. The Chroma vector database is stored locally in
            Streamlit community servers. Upon receiving the PDF document, the
            text will be extracted from the PDF and a single document is created for
            each PDF. Next, the document will undergo a chunking process
            using `RecursiveCharacterTextSplitter` with a chunk size of 1000 and chunk
            overlap of 200. Lastly, the chunked documents will be saved into
            Chroma vector store and persisted in a file directory. """)

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

st.subheader("Retrieval Augmented Generation (RAG) with Word Document Creation Tool")
st.image(
    image="./assets/flowchart-rag.png",
    caption="Figure 2 Flowchart for RAG (Retrieval Page)",
)
st.markdown(
    """
 Figure 2 shows the data flow for the Retrieval Augmented Generation (RAG) page.
 To use the application RAG, one must upload a PDF document and enter a collection name.
 The application will perform splitting, chunking, and embedding of the PDF document.
 The text chunks will then be stored in a Chroma vector store.
 After which the user can select a collection name and perform a query on the uploaded documents.
 The UI will display an output of the retrieved document chunks with source references.

 If the query matches a tool description of wanting to 'Export to a word document',
 the tool will be called and a download button will be displayed as the output.
 """
)
st.markdown(
    """
    **Test Prompt**
```
Can you help me do the following below.

Step 1 - Provide a 100-word summary of MediShield
Step 2 - Export the summary into a single word document
```
"""
)
