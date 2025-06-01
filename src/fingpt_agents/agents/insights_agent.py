# src/fingpt_agents/agents/insights_agent.py

from pathlib import Path
import pandas as pd
from src.fingpt_agents.utils.logger_utils import logger  # Correct import

class InsightsAgent:
    def __init__(self, processed_data_path: str = "data/processed_data/"):
        self.processed_data_path = Path(processed_data_path)
        self.dataframes = {}
        logger.info("[INIT] InsightsAgent initialized.")

    def load_processed_data(self):
        logger.info("[LOAD] Loading processed stock data...")
        for file in self.processed_data_path.glob("*_processed.csv"):
            ticker = file.stem.split('_')[0]
            df = pd.read_csv(file, parse_dates=True, index_col=0)
            self.dataframes[ticker] = df
            logger.info(f"[LOAD] Loaded {ticker} with {len(df)} rows.")

    def generate_summary(self):
        logger.info("[INSIGHT] Generating summary from stock data...")
        summaries = []
        for ticker, df in self.dataframes.items():
            avg_return = df[f"Return_{ticker}"].mean() * 100
            volatility = df[f"Return_{ticker}"].std() * 100
            summaries.append(
                f"{ticker}: Avg Return = {avg_return:.2f}%, Volatility = {volatility:.2f}%"
            )
        return summaries
