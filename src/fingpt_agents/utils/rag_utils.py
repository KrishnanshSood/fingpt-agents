import os
from typing import List
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from colorama import Fore, Style, init

init(autoreset=True)

def log(message: str):
    print(message)

class EmbeddingModel:
    def __init__(self):
        log(f"{Fore.YELLOW}Initializing Ollama Embedding model...{Style.RESET_ALL}")
        self.model = OllamaEmbeddings(model="llama3")

    def embed(self, texts: List[str]):
        log(f"{Fore.YELLOW}Generating embeddings for {len(texts)} texts...{Style.RESET_ALL}")
        return self.model.embed_documents(texts)

class VectorStore:
    def __init__(self, embedding_model: EmbeddingModel):
        log(f"{Fore.YELLOW}Initializing FAISS vector store...{Style.RESET_ALL}")
        self.store = None
        self.embedding_model = embedding_model

    def add_texts(self, texts: List[str]):
        log(f"{Fore.YELLOW}Adding texts to FAISS vector store...{Style.RESET_ALL}")
        self.store = FAISS.from_texts(
            texts=texts,
            embedding=self.embedding_model.model  # Correct way
        )

    def get_retriever(self):
        log(f"{Fore.YELLOW}Retrieving from FAISS vector store...{Style.RESET_ALL}")
        return self.store.as_retriever()

class QAChain:
    def __init__(self):
        self.qa = None

    def build(self, vector_store: VectorStore):
        log(f"{Fore.YELLOW}Initializing LLM (OllamaLLM) for QA chain...{Style.RESET_ALL}")
        llm = OllamaLLM(model="llama3")
        retriever = vector_store.get_retriever()
        self.qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    def run(self, query: str) -> str:
        log(f"{Fore.YELLOW}Running the QA chain on the query...{Style.RESET_ALL}")
        return self.qa.invoke({"query": query})["result"]

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    log(f"{Fore.MAGENTA}Attempting text extraction using PyPDF2...{Style.RESET_ALL}")
    try:
        reader = PdfReader(pdf_path)
        texts = [page.extract_text() for page in reader.pages if page.extract_text()]
        if texts:
            return texts
    except Exception as e:
        log(f"{Fore.RED}Failed to extract with PyPDF2: {e}{Style.RESET_ALL}")

    log(f"{Fore.MAGENTA}Falling back to OCR with pytesseract...{Style.RESET_ALL}")
    try:
        images = convert_from_path(pdf_path)
        texts = []
        for img in images:
            text = pytesseract.image_to_string(img)
            if text.strip():
                texts.append(text)
        return texts
    except Exception as e:
        log(f"{Fore.RED}OCR failed: {e}{Style.RESET_ALL}")
        return []
