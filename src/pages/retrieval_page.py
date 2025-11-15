# Set up and run this Streamlit App
import os
from typing import List

import streamlit as st
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from helpers import file, llm, state

state.ensure_session_states()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="Home")
# endregion <--------- Streamlit App Configuration --------->

st.title("Retrieval (RAG)")
PERSIST_DIR = "./chroma_langchain_db"
OPENAI_MODEL = st.secrets["OPENAI_MODEL"]

def split_document(docs):
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
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

    # st.success(
    #    f"Ingested {len(splitted_documents)} chunks into Chroma vector store and saved to '{PERSIST_DIR}'"
    # )
    # st.session_state["vectordb_exists"] = True

    #print(vector_store._collection.peek(limit=1))

    # response = st.write_stream(llm.generate_response_from_context(prompt_text))
    # response = llm.generate_response_from_context(prompt_text)
    # stream_response(response)

    # return response


def stream_response(response):
    with st.chat_message("assistant"):
        # response = st.write_stream(llm.generate_response(prompt_text))
        st.write_stream(response)
    # st.write_stream(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


def get_chroma_collection(collection_name: str, embeddings) -> Chroma:
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    return vector_store


def make_retrieval_chain(collection_name: str, embeddings, llm_model=OPENAI_MODEL):
    from langchain_classic.chains import ConversationalRetrievalChain

    vector_store = get_chroma_collection(collection_name, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name=llm_model, temperature=0)
    chain = ConversationalRetrievalChain.from_llm(
        llm, retriever, return_source_documents=True
    )

    return chain


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

                # total_chunks = 0
                # for f in uploaded_files:
                #    path = save_uploaded_file(f)
                #    texts = load_and_split_pdf(path)
                #    total_chunks += len(texts)
                #    index_documents_to_chroma(texts, collection_name, embeddings)

                # After saving, create retrieval chain and store it in session_state
                chain = make_retrieval_chain(
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

with st.container():
    st.header("Chat with a collection")

    selected_collection = st.selectbox("Choose collection to query", options=[""] + list(st.session_state.conversations.keys()), key="selected_coll")

    if selected_collection is None:
        selected_collection = ""

    if selected_collection == "":
        st.info("Index or load a collection first on the left panel. After indexing, it should appear in the dropdown.")
    else:
        if selected_collection not in st.session_state.conversations:
            # attempt to lazily load chain if collection exists on disk
            embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
            try:
                chain = make_retrieval_chain(
                    selected_collection, embeddings_model, llm_model=OPENAI_MODEL
                )
                st.session_state.conversations[selected_collection] = chain
                st.success(f"Loaded collection '{selected_collection}'.")
            except Exception as e:
                st.error(f"Failed to load collection: {e}")

        chain = st.session_state.conversations.get(selected_collection)
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

        # Input box
        prompt = st.chat_input("Ask a question about the uploaded documents...")
        if prompt:
            if chain is None:
                st.error(
                    "Retrieval chain not ready. Try indexing the collection or reload the app."
                )
            else:
                # append user message to history
                st.session_state.chat_history.append(
                    {"role": "user", "content": prompt}
                )
                with st.chat_message("user"):
                    st.write(prompt)

                with st.chat_message("assistant"):
                    # Run chain
                    result = chain({"question": prompt, "chat_history": []})
                    answer = result.get("answer")
                    st.write(answer)

                # store assistant answer in history
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )

        st.markdown("---")
        st.subheader("Source documents returned (last query)")
        if "result" in locals() and result.get("source_documents"):
            for src in result.get("source_documents"):
                meta = getattr(src, "metadata", {})
                page = meta.get("page", "n/a")
                source = meta.get("source", "n/a")
                st.write(
                    f"**Source**: {source} — page: {page}\n\n{src.page_content[:400]}..."
                )
