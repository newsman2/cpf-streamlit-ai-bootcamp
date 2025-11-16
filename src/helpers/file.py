import os
import re
import tempfile

import pdfplumber


def extract_docx_path(text: str) -> str | None:
    # Matches only UNIX-style absolute paths ending with .docx
    pattern = r"(/(?:[\w\-\.]+/)*[\w\-\.]+\.docx)"
    match = re.search(pattern, text)
    return match.group(1) if match else None


def extract_filename(path: str) -> str:
    return os.path.basename(path)


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
