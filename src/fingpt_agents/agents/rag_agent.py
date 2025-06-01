# src/fingpt_agents/agents/rag_agent.py

from src.fingpt_agents.utils.rag_utils import (
    EmbeddingModel,
    VectorStore,
    QAChain,
    extract_text_from_pdf,
    log,
)
from colorama import Fore, Style


class RAGAgent:
    def __init__(self):
        log(f"{Fore.CYAN}Initializing RAGAgent...{Style.RESET_ALL}")
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(self.embedding_model)
        self.qa_chain = QAChain()

    def build_vector_store(self, texts):
        self.vector_store.add_texts(texts)

    def run_rag(self, pdf_path: str, query: str) -> str:
        log(f"{Fore.CYAN}Extracting text from PDF: {pdf_path}{Style.RESET_ALL}")
        texts = extract_text_from_pdf(pdf_path)
        log(f"{Fore.CYAN}Text extraction complete. Found {len(texts)} text chunks.{Style.RESET_ALL}")
        self.build_vector_store(texts)
        self.qa_chain.build(self.vector_store)
        return self.qa_chain.run(query)
