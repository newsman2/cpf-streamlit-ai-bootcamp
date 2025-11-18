import streamlit as st

# Custom CSS
st.markdown("""
    <style>
    /* Expander header (closed + open) */
    .stExpander {
        color: red !important;               /* White text */
        font-weight: bold !important;
        border-radius: 6px;
        padding: 8px;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    expander = st.expander("DISCLAIMER", icon=":material/warning:", expanded=True)
    expander.write("""
IMPORTANT NOTICE: This web application is a prototype developed for educational
                   purposes only. The information provided here is NOT intended
                   for real-world usage and should not be relied upon for
                   making any decisions, especially those related to financial,
                   legal, or healthcare matters.

Furthermore, please be aware that the LLM may generate inaccurate or incorrect
                   information. You assume full responsibility for how you use
                   any generated output.

Always consult with qualified professionals for accurate and personalized advice.
                   """)
    pg = st.navigation(
        [
            st.Page("pages/about_page.py", title="About", icon=":material/info:", default=True),
            st.Page(
                "pages/methodology_page.py",
                title="Methodology",
                icon=":material/graph_5:",
            ),
            st.Page(
                "pages/cpf_assistant_page.py",
                title="CPF Assistant",
                icon=":material/home:",
            ),
            st.Page(
                "pages/retrieval_page.py",
                title="Retrieval (RAG)",
                icon=":material/library_books:",
            ),
        ],
    )
    pg.run()


if __name__ == "__main__":
    main()
