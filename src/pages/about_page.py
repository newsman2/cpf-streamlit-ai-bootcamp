import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="About")
# endregion <--------- Streamlit App Configuration --------->

st.title("About")
st.header("CPF Assistant")

st.subheader("Project Scope")
st.markdown(
    """
    This project aims to build an interactive RAG-based chatbot platform using Streamlit. The system will allow users to upload PDF documents, process their content into embeddings using LangChain, store them in a Chroma vector database, and retrieve relevant information through a conversational chat interface powered by an LLM.
    """
)

st.subheader("Objectives")
st.markdown(""" 
            - Deliver and deploy a fully functional Chatbot to help users to learn more about CPF
            - Implement a Streamlit-based RAG Chatbot with document upload and Chroma vector storage
            - Deploy an LLM-based assistant that can answer questions using uploaded documents
            - Show users which documents are reference during RAG process
            """)
st.subheader("Data Sources")
st.markdown("""
            - [CPF](https://www.cpf.gov.sg/)
            - [CPF Educational Resources](https://www.cpf.gov.sg/member/infohub/educational-resources?page=1&pagesize=9)
            - [CPF-related announcements](https://www.cpf.gov.sg/employer/infohub/news/cpf-related-announcements)
            - [CPF Investment](https://www.cpf.gov.sg/content/dam/web/member/business-partners/documents/CPFInvestmentGuidelinespdf.pdf)
            - [CPF Withdrawal Rules](https://www.cpf.gov.sg/content/dam/web/member/faq/retirement-income/documents/withdrawal-rules-table.pdf)
            - [CPF Contribution Rate Table](https://www.cpf.gov.sg/content/dam/web/employer/employer-obligations/documents/CPFcontributionratesfrom1Jan2026.pdf)
            """)

st.subheader("Features")
st.markdown("""
            - General CPF Assistant
                - Chatbot that answers questions about Singapore Central Provident Fund (CPF)
            - Retrieval Augmented Generation (RAG)
                - PDF document ingestion and parsing
                - Automatic text chunking and metadata extraction
                - Embedding generation using LLM embedding models
                - Chroma vector database for similarity search
                - Display of retrieved document chunks with source references
            """)
