import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from core.document_processor import load_documents_from_directory, split_documents
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_DIR = "c:/Projetos/Processo Julio/chroma_db"

def get_embeddings_model():
    # Uses Google Gemini Embeddings if API key is set
    # Ensure GOOGLE_API_KEY is in your .env file
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def get_vector_store():
    embeddings = get_embeddings_model()
    # Check if DB exists
    if os.path.exists(DB_DIR):
        print("Carregando banco de dados vetorial existente...")
        return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    else:
        print("Banco de dados vetorial não encontrado. Será necessário inicializar os dados.")
        return None

def initialize_vector_store():
    print("Iniciando processamento dos documentos...")
    docs = load_documents_from_directory()
    chunks = split_documents(docs)
    
    print(f"Gerando embeddings para {len(chunks)} trechos e salvando no ChromaDB...")
    embeddings = get_embeddings_model()
    
    # Create and persist the vector store
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    vector_store.persist()
    print("Banco de dados vetorial inicializado com sucesso!")
    return vector_store

if __name__ == "__main__":
    initialize_vector_store()
