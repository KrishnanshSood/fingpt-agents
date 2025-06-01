from src.fingpt_agents.utils.rag_utils import (
    EmbeddingModel,
    VectorStore,
    QAChain,
    extract_text_from_pdf,
)
from src.fingpt_agents.utils.logger_utils import logger

class RAGAgent:
    def __init__(self):
        logger.info("[INIT] Initializing RAGAgent...")
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(self.embedding_model)
        self.qa_chain = QAChain()

    def build_vector_store(self, texts):
        self.vector_store.add_texts(texts)

    def run_rag(self, pdf_path: str, query: str) -> str:
        logger.info(f"[LOAD] Extracting text from PDF: {pdf_path}")
        texts = extract_text_from_pdf(pdf_path)
        logger.info(f"[LOAD] Text extraction complete. Found {len(texts)} text chunks.")
        self.build_vector_store(texts)
        self.qa_chain.build(self.vector_store)
        return self.qa_chain.run(query)
