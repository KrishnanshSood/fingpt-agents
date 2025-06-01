import json
from src.fingpt_agents.agents.data_agent import DataIngestionAgent
from src.fingpt_agents.utils.logger_utils import logger  # <-- use this

def load_tickers_from_config(config_path="tickers_config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("tickers", [])
    except Exception as e:
        logger.warning(f"[CONFIG] Failed to load tickers config: {e}. Using defaults.")
        return []

def main():
    logger.info("[MAIN] Running DataIngestionAgent...")
    tickers = load_tickers_from_config()
    data_agent = DataIngestionAgent(tickers=tickers)
    data_agent.fetch_stock_data()
    logger.info("[DONE] Data fetching completed.")

if __name__ == "__main__":
    main()
