from pypdf import PdfReader
from docx import Document

def extract_text(uploaded_file):

    if uploaded_file is None:
        return ""

    file_type = uploaded_file.name.split(".")[-1].lower() # extract the file extension and convert it to lowercase

# .txt
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

# .pdf
    elif file_type == "pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

# .docx
    elif file_type == "docx":
        doc = Document(uploaded_file)
        return "\n".join(
            para.text
            for para in doc.paragraphs
        )

    return ""