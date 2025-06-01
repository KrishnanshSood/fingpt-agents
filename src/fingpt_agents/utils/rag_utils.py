import os
from typing import List
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from src.fingpt_agents.utils.logger_utils import logger  # import centralized logger

class EmbeddingModel:
    def __init__(self):
        logger.info("Initializing Ollama Embedding model...")
        self.model = OllamaEmbeddings(model="llama3")

    def embed(self, texts: List[str]):
        logger.info(f"Generating embeddings for {len(texts)} texts...")
        return self.model.embed_documents(texts)

class VectorStore:
    def __init__(self, embedding_model: EmbeddingModel):
        logger.info("Initializing FAISS vector store...")
        self.store = None
        self.embedding_model = embedding_model

    def add_texts(self, texts: List[str]):
        logger.info("Adding texts to FAISS vector store...")
        self.store = FAISS.from_texts(
            texts=texts,
            embedding=self.embedding_model.model  # Correct usage
        )

    def get_retriever(self):
        logger.info("Retrieving from FAISS vector store...")
        return self.store.as_retriever()

class QAChain:
    def __init__(self):
        self.qa = None

    def build(self, vector_store: VectorStore):
        logger.info("Initializing LLM (OllamaLLM) for QA chain...")
        llm = OllamaLLM(model="llama3")
        retriever = vector_store.get_retriever()
        self.qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    def run(self, query: str) -> str:
        logger.info("Running the QA chain on the query...")
        return self.qa.invoke({"query": query})["result"]

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    logger.info("Attempting text extraction using PyPDF2...")
    try:
        reader = PdfReader(pdf_path)
        texts = [page.extract_text() for page in reader.pages if page.extract_text()]
        if texts:
            return texts
    except Exception as e:
        logger.error(f"Failed to extract with PyPDF2: {e}")

    logger.info("Falling back to OCR with pytesseract...")
    try:
        images = convert_from_path(pdf_path)
        texts = []
        for img in images:
            text = pytesseract.image_to_string(img)
            if text.strip():
                texts.append(text)
        return texts
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return []
