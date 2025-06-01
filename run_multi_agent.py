from src.fingpt_agents.utils.logger_utils import logger
from src.fingpt_agents.agents.data_agent import DataIngestionAgent
from src.fingpt_agents.agents.rag_agent import RAGAgent

def main():
    logger.info("[MAIN] Starting multi-agent pipeline...")

    # Step 1: Fetch stock data
    logger.info("[STEP 1] Running DataIngestionAgent...")
    tickers = ["AAPL"]
    data_agent = DataIngestionAgent(tickers, start="2022-01-01", end="2022-12-31")
    data_agent.fetch_stock_data()
    data_agent.save_to_csv()
    logger.info("[STEP 1] Data fetching and saving complete.")

    # Step 2: Run RAG on Apple 10-K PDF
    logger.info("[STEP 2] Running RAGAgent for Q&A on 10-K document...")
    pdf_path = "data/filings/APPLE_10K_2022.pdf"
    query = "What are the main risk factors mentioned in Apple's 2022 10-K report?"

    rag_agent = RAGAgent()
    answer = rag_agent.run_rag(pdf_path, query)

    logger.info(f"[STEP 2] RAGAgent Answer: {answer}")

    logger.info("[MAIN] Pipeline complete.")

if __name__ == "__main__":
    main()
