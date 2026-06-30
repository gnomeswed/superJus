import os
import glob
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        text = soup.get_text(separator="\n", strip=True)
    return [Document(page_content=text, metadata={"source": file_path, "type": "html"})]

def process_pdf_file(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

def process_text_file(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    return loader.load()

def load_documents_from_directory(directory_path="c:/Projetos/Processo Julio/Processo"):
    documents = []
    
    # Process PDF files
    pdf_files = glob.glob(f"{directory_path}/**/*.pdf", recursive=True)
    for pdf in pdf_files:
        try:
            documents.extend(process_pdf_file(pdf))
        except Exception as e:
            print(f"Error processing {pdf}: {e}")
            
    # Process HTML files
    html_files = glob.glob(f"{directory_path}/**/*.html", recursive=True)
    for html in html_files:
        try:
            documents.extend(process_html_file(html))
        except Exception as e:
            print(f"Error processing {html}: {e}")
            
    # Process TXT files
    txt_files = glob.glob(f"{directory_path}/**/*.txt", recursive=True)
    for txt in txt_files:
        try:
            documents.extend(process_text_file(txt))
        except Exception as e:
            print(f"Error processing {txt}: {e}")

    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return text_splitter.split_documents(documents)

if __name__ == "__main__":
    docs = load_documents_from_directory()
    print(f"Loaded {len(docs)} document pages/sections.")
    chunks = split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
