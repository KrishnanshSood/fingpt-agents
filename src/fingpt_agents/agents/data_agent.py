import os
from typing import List
import yfinance as yf
from src.fingpt_agents.utils.logger_utils import logger  # <-- use this

DEFAULT_TICKERS = [
    "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA",
    "NVDA", "META", "NFLX", "INTC", "CSCO"
]

class DataIngestionAgent:
    def __init__(
        self,
        tickers: List[str] = None,
        start_date: str = "2022-01-01",
        end_date: str = "2022-12-31",
        save_dir: str = "data/stock_data"
    ):
        self.tickers = tickers or DEFAULT_TICKERS
        self.start_date = start_date
        self.end_date = end_date
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

        logger.info(f"[INIT] DataIngestionAgent initialized with {len(self.tickers)} tickers.")

    def fetch_stock_data(self):
        logger.info(f"[FETCH] Downloading stock data from {self.start_date} to {self.end_date}...")
        for ticker in self.tickers:
            try:
                logger.info(f"[FETCH] Downloading data for {ticker}")
                data = yf.download(ticker, start=self.start_date, end=self.end_date)
                if data.empty:
                    logger.warning(f"[WARN] No data found for {ticker}. Skipping.")
                    continue
                filepath = os.path.join(self.save_dir, f"{ticker}.csv")
                data.to_csv(filepath)
                logger.info(f"[SAVE] {ticker} data saved to {filepath}")
            except Exception as e:
                logger.error(f"[ERROR] Failed to download {ticker}: {e}")
