import os
from typing import List
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from src.fingpt_agents.utils.logger_utils import logger
from src.fingpt_agents.agents.base_agent import Agent


class EmbeddingModel:
    def __init__(self):
        logger.info("Initializing Ollama Embedding model...")
        self.model = OllamaEmbeddings(model="llama3")

    def embed(self, texts: List[str]):
        logger.info(f"Generating embeddings for {len(texts)} texts...")
        return self.model.embed_documents(texts)


class VectorStore:
    def __init__(self, embedding_model: OllamaEmbeddings):
        logger.info("Initializing FAISS vector store...")
        self.store = None
        self.embedding_model = embedding_model

    def add_texts(self, texts: List[str]):
        logger.info("Adding texts to FAISS vector store...")
        self.store = FAISS.from_texts(
            texts=texts,
            embedding=self.embedding_model
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
    logger.info(f"[LOAD] Extracting text from {pdf_path}")
    try:
        reader = PdfReader(pdf_path)
        texts = [page.extract_text() for page in reader.pages if page.extract_text()]
        if texts:
            return texts
    except Exception as e:
        logger.error(f"PyPDF2 extraction failed for {pdf_path}: {e}")

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
        logger.error(f"OCR failed for {pdf_path}: {e}")
        return []


class RAGAgent(Agent):
    def __init__(self, filings_dir: str):
        logger.info("[INIT] Initializing RAGAgent...")

        self.embedding_model = OllamaEmbeddings(model="llama3")
        self.text_chunks = []

        for file in sorted(os.listdir(filings_dir), reverse=True):
            if file.endswith(".pdf") and file.startswith("AAPL_10K_"):
                file_path = os.path.join(filings_dir, file)
                texts = extract_text_from_pdf(file_path)
                self.text_chunks.extend(texts)

        logger.info(f"[LOAD] Extracted total {len(self.text_chunks)} text chunks from filings")

        self.vector_store = FAISS.from_texts(
            texts=self.text_chunks,
            embedding=self.embedding_model  # ✅ Pass the full object, not `.model`
        )
        logger.info("[BUILD] Vector store built successfully")

        self.qa_chain = QAChain()
        self.qa_chain.build(vector_store=self.vector_store)
        logger.info("[BUILD] QA chain initialized")

    def run(self, context: dict) -> dict:
        query = context.get("query", "Summarize Apple's financials over the years.")
        logger.info(f"[QUERY] Running query: {query}")
        answer = self.qa_chain.run(query)
        logger.info(f"[ANSWER]\n{answer}")
        return {"answer": answer}
