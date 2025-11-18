import streamlit as st

from helpers import utility

# region <--------- Streamlit App Configuration --------->
st.set_page_config(layout="centered", page_title="About")

# Do not continue if check_password is not True.
if not utility.check_password():
    st.stop()
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
            - [CPF - Example: To receive monthly payout of $1470](https://www.cpf.gov.sg/content/dam/web/member/retirement-income/documents/CPF%20LIFE%20payout%20examples%202022.pdf)
            - [CPF - Protecting your Home](https://www.cpf.gov.sg/content/dam/web/member/home-ownership/documents/HPS_Handbook_A_English.pdf)
            - [CPF - MediShield Life Booklet](https://www.cpf.gov.sg/content/dam/web/member/healthcare/documents/InformationBookletForTheNewlyInsured.pdf)
            - [CPF - Retirement Sum](https://www.cpf.gov.sg/member/infohub/educational-resources/what-is-the-cpf-retirement-sum)
            """)

st.subheader("Features")
st.markdown("""
            - General CPF Assistant
                - Chatbot that answers questions about Singapore Central Provident Fund (CPF)
                - Chatbot that provides a summary in Chinese
                - Chatbot that stream words in as the LLM response
            - Retrieval Augmented Generation (RAG) with Word Document Creation Tool
                - PDF document ingestion and parsing
                - Automatic text chunking and metadata extraction
                - Embedding generation using LLM embedding models
                - Chroma vector database for similarity search
                - Display of retrieved document chunks with source references
                - Tool to create a word document from the conversation
            """)
