from src.fingpt_agents.agents.rag_agent import RAGAgent
from src.fingpt_agents.utils.logger_utils import setup_logging, logger

def main():
    setup_logging()
    logger.info("[MAIN] Starting RAG pipeline...")
    rag_agent = RAGAgent()
    pdf_path = "data/filings/APPLE_10K_2022.pdf"
    query = "What are the major risk factors Apple mentions in the 10-K report?"
    answer = rag_agent.run_rag(pdf_path, query)
    print(f"Answer:\n{answer}")

if __name__ == "__main__":
    main()
