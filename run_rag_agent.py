from src.fingpt_agents.agents.rag_agent import RAGAgent
from src.fingpt_agents.utils.logger_utils import logger

def main():
    filings_dir = "data/filings"  # adjust if your filings folder is elsewhere
    agent = RAGAgent(filings_dir=filings_dir)

    query = "What are the main risk factors mentioned in Apple's 10-K reports over the years?"
    logger.info("Starting query to RAG agent...")
    answer = agent.query(query)
    print("\n=== RAG Agent Answer ===\n")
    print(answer)

if __name__ == "__main__":
    main()
