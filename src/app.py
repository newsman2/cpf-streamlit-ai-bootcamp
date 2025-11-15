import streamlit as st


def main():
    pg = st.navigation(
        [
            st.Page(
                "pages/landing_page.py",
                title="Home",
                icon=":material/home:",
                default=True,
            ),
            st.Page(
                "pages/retrieval_page.py",
                title="Retrieval (RAG)",
                icon=":material/library_books:",
            ),
            st.Page("pages/about_page.py", title="About", icon=":material/info:"),
            st.Page(
                "pages/methodology_page.py",
                title="Methodology",
                icon=":material/graph_5:",
            ),
            st.Page(
                "pages/settings_page.py", title="Settings", icon=":material/settings:"
            ),
        ],
        position="top",
    )
    pg.run()


if __name__ == "__main__":
    main()
