from pathlib import Path
from datetime import datetime
import yfinance as yf
import pandas as pd

from src.fingpt_agents.utils.logger_utils import logger  # import your configured logger

class DataIngestionAgent:
    def __init__(self, tickers, start="2010-01-01", end=None):
        self.tickers = [t.upper() for t in tickers]
        self.start = start
        self.end = end or datetime.today().strftime("%Y-%m-%d")
        self.dataframes = {}

        logger.info(f"[INIT] Initialized for tickers: {', '.join(self.tickers)}")

    def fetch_stock_data(self):
        logger.info(f"[FETCH] Fetching data from {self.start} to {self.end}")
        for ticker in self.tickers:
            logger.info(f"[FETCH] Downloading {ticker}...")
            df = yf.download(ticker, start=self.start, end=self.end)
            if df.empty:
                logger.warning(f"[WARN] No data fetched for {ticker}")
            else:
                df.reset_index(inplace=True)
                self.dataframes[ticker] = df
                logger.info(f"[DONE] Fetched {len(df)} rows for {ticker}")

    def save_to_csv(self, path="data/processed/"):
        Path(path).mkdir(parents=True, exist_ok=True)
        for ticker, df in self.dataframes.items():
            # Flatten multi-index columns if any
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() for col in df.columns.values]

            file_path = Path(path) / f"{ticker}_stock_data.csv"
            df.to_csv(file_path, index=True)
            logger.info(f"[SAVE] Saved {ticker} data to {file_path}")
