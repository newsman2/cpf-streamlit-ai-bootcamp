# Set up and run this Streamlit App
import streamlit as st
from helpers import llm, file
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="My Streamlit App")
# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(
    "Ask anything about CPF", accept_file="multiple", file_type=["pdf"]
):
    prompt_text = prompt.text
    prompt_files = prompt.files

    with st.spinner("Extracting text and building vector store..."):
        docs = []
        for f in prompt_files:
            text = file.extract_text_from_pdf(f)
            # create a single Document for each PDF (you can also split per page)
            docs.append(Document(page_content=text, metadata={"source": f.name}))

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splitted_documents = []
        for d in docs:
            splitted_documents.extend(splitter.split_documents([d]))

        # An embeddings model is initialized using the OpenAIEmbeddings class.
        # The specified model is 'text-embedding-3-small'.
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

        persist_dir = "./chroma_langchain_db"

        # For more info on using the Chroma class, refer to the documentation https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
        vector_store = Chroma.from_documents(
            collection_name="prompt_engineering_playbook",
            documents=splitted_documents,
            embedding=embeddings_model,
            persist_directory=persist_dir,  # Where to save data locally, remove if not neccesary
        )

        st.success(
            f"Ingested {len(splitted_documents)} chunks into Chroma vector store and saved to '{persist_dir}'"
        )
        st.session_state["vectordb_exists"] = True

        print(vector_store._collection.peek(limit=1))

    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    with st.chat_message("assistant"):
        response = st.write_stream(llm.generate_response(prompt_text))
    st.session_state.messages.append({"role": "assistant", "content": response})
