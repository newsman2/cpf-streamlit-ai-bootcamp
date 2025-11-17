# Set up and run this Streamlit App
import os
from typing import List

import streamlit as st
from langchain.messages import AIMessage, ToolMessage
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agents import cpf
from helpers import file, llm, state, utility

state.ensure_session_states()
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="Home")

# Do not continue if check_password is not True.
if not utility.check_password():
    st.stop()
# endregion <--------- Streamlit App Configuration --------->

st.title("Retrieval (RAG)")
PERSIST_DIR = st.secrets["PERSIST_DIR"]
OPENAI_MODEL = st.secrets["OPENAI_MODEL"]


def split_document(docs):
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    splitted_documents = []
    for d in docs:
        splitted_documents.extend(splitter.split_documents([d]))

    return splitted_documents


def load_documents(prompt_files) -> List:
    docs = []
    for f in prompt_files:
        text = file.extract_text_from_pdf(f)
        # create a single Document for each PDF (you can also split per page)
        docs.append(Document(page_content=text, metadata={"source": f.name}))

    return docs


def save_collection(collection_name, splitted_documents, embeddings_model=None):
    vector_store = Chroma.from_documents(
        collection_name=collection_name,
        documents=splitted_documents,
        embedding=embeddings_model,
        persist_directory=PERSIST_DIR,  # Where to save data locally, remove if not neccesary
    )


with st.sidebar:
    st.header("Upload & Index PDFs")

    collection_name = st.text_input(
        "Collection name (unique)", key="collection_name_input"
    )
    uploaded_files = st.file_uploader(
        "Upload PDF files", accept_multiple_files=True, type=["pdf"]
    )

    if st.button("Upload + Index"):
        if not collection_name or collection_name.strip() == "":
            st.error("Please provide a collection name before indexing.")
        elif not uploaded_files:
            st.error("Please upload one or more PDF files to index.")
        else:
            with st.spinner(
                "Processing PDFs and indexing into Chroma — this may take a minute..."
            ):
                # Ensure embeddings
                embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
                docs = load_documents(uploaded_files)
                splitted_docs = split_document(docs)
                save_collection(collection_name, splitted_docs, embeddings_model)

                # After saving, create retrieval chain and store it in session_state
                chain = llm.make_retrieval_chain(
                    collection_name, embeddings_model, llm_model=OPENAI_MODEL
                )
                st.session_state.conversations[collection_name] = chain

                st.success(
                    f"Indexed {len(uploaded_files)} file(s) into collection '{collection_name}'."
                )

    st.markdown("---")
    st.subheader("Existing collections (from persist directory)")

    collections = []
    try:
        # List collections by inspecting the persist directory (Chroma stores per-collection folders)
        if os.path.exists(PERSIST_DIR):
            embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
            vector_store = Chroma(
                embedding_function=embeddings_model,
                persist_directory=PERSIST_DIR,
            )
            collections = [
                collection.name
                for collection in vector_store._client.list_collections()
            ]
    except Exception:
        collections = []

    if collections is None:
        st.write("No collections yet")
    else:
        st.write(f"There are {len(collections)} existing collections.")

selected_collection = ""

st.header("Chat with a collection")

options = [""] + list(st.session_state.conversations.keys())

conversations_key = st.session_state.conversations_key
index = options.index(conversations_key) if conversations_key in options else 0

selected_collection = st.selectbox(
    "Choose collection to query",
    options=options,
    key="selected_coll",
    index=index,
)

if selected_collection is None:
    selected_collection = ""

if selected_collection == "":
    st.info(
        "Index or load a collection on the left panel. After indexing, it should appear in the dropdown."
    )
else:
    st.session_state.conversations_key = selected_collection
    if selected_collection not in st.session_state.conversations:
        # attempt to lazily load chain if collection exists on disk
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        try:
            chain = llm.make_retrieval_chain(
                selected_collection, embeddings_model, llm_model=OPENAI_MODEL
            )
            st.session_state.conversations[selected_collection] = chain
            st.success(f"Loaded collection '{selected_collection}'.")
        except Exception as e:
            st.error(f"Failed to load collection: {e}")

    chain = st.session_state.conversations.get(selected_collection)

    # Input box
    prompt = st.chat_input("Ask a question about the uploaded documents...")
    if prompt:
        if chain is None:
            st.error(
                "Retrieval chain not ready. Try indexing the collection or reload the app."
            )
        else:
            if len(st.session_state.chat_history) > 0:
                # Display chat history
                for i, turn in enumerate(st.session_state.chat_history):
                    role = turn.get("role")
                    content = turn.get("content")
                    if role == "user":
                        st.chat_message("user").write(content)
                    else:
                        st.chat_message("assistant").write(content)

            # append user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Generating response — this may take a minute..."):
                    answer = ""
                    agent = cpf.init_agent()
                    result = agent.invoke(
                        {
                            "messages": [{"role": "user", "content": prompt}],
                            "collection_name": selected_collection,
                        }
                    )
                    for msg in result["messages"]:
                        # If tool returned a docx path, show download button
                        if isinstance(msg, ToolMessage):
                            try:
                                server_path = file.extract_docx_path(msg.content)
                                # Read file bytes
                                with open(server_path, "rb") as f:
                                    file_bytes = f.read()
                                    filename = file.extract_filename(server_path)
                                    st.download_button(
                                        "Download Word Document",
                                        file_bytes,
                                        filename,
                                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    )
                            except Exception as e:
                                st.error(f"Failed to load file: {e}")

                        if isinstance(msg, AIMessage):
                            answer += msg.content

                    # store assistant answer in history
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )

                    st.write(answer)

    else:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for i, turn in enumerate(st.session_state.chat_history):
                role = turn.get("role")
                content = turn.get("content")
                if role == "user":
                    st.chat_message("user").write(content)
                else:
                    st.chat_message("assistant").write(content)

    st.markdown("---")
    st.subheader("Source documents returned (last query)")
    if "result" in locals() and result.get("context"):
        for src in result.get("context"):
            meta = getattr(src, "metadata", {})
            page = meta.get("page", "n/a")
            source = meta.get("source", "n/a")
            st.write(
                f"**Source**: {source} — page: {page}\n\n{src.page_content[:400]}..."
            )
