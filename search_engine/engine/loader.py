import os
import pymupdf as pymupdf

# Add any file types you want to support here
SUPPORTED_EXTENSIONS = (".txt", ".pdf", ".md", ".csv", ".html")

def load_documents(folder_path: str) -> dict:
    documents = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(SUPPORTED_EXTENSIONS):
            filepath = os.path.join(folder_path, filename)

            if filename.endswith(".pdf"):
                # Extract text from every page of the PDF
                text = ""
                with pymupdf.open(filepath) as pdf:
                    for page in pdf:
                        text += page.get_text()
                documents[filename] = text

            else:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    documents[filename] = f.read()

    return documents