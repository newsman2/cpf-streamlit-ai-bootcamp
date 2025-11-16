import os
import tempfile

import pdfplumber


def extract_text_from_pdf(uploaded_file) -> str:
    """Return extracted text from an uploaded Streamlit file-like object."""
    # write to temp file because pdfplumber works with file paths
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    text_chunks = []
    try:
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text()
                if txt:
                    text_chunks.append(txt)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    return "\n\n".join(text_chunks)
