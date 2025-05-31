import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Setup logging with simple format
logging.basicConfig(level=logging.INFO, format="%(message)s")

class DataIngestionAgent:
    def __init__(self, tickers, start="2010-01-01", end=None):
        self.tickers = [t.upper() for t in tickers]
        self.start = start
        self.end = end or datetime.today().strftime("%Y-%m-%d")
        self.dataframes = {}

        logging.info(f"{Fore.GREEN}[INIT]{Style.RESET_ALL} Initialized for tickers: {', '.join(self.tickers)}")

    def fetch_stock_data(self):
        logging.info(f"{Fore.BLUE}[FETCH]{Style.RESET_ALL} Fetching data from {self.start} to {self.end}")
        for ticker in self.tickers:
            logging.info(f"{Fore.CYAN}[FETCH]{Style.RESET_ALL} Downloading {ticker}...")
            df = yf.download(ticker, start=self.start, end=self.end)
            if df.empty:
                logging.warning(f"{Fore.RED}[WARN]{Style.RESET_ALL} No data fetched for {ticker}")
            else:
                df.reset_index(inplace=True)
                self.dataframes[ticker] = df
                logging.info(f"{Fore.GREEN}[DONE]{Style.RESET_ALL} Fetched {len(df)} rows for {ticker}")

    def save_to_csv(self, path="data/processed/"):
        Path(path).mkdir(parents=True, exist_ok=True)
        for ticker, df in self.dataframes.items():
            # Flatten multi-index columns if any
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() for col in df.columns.values]

            file_path = Path(path) / f"{ticker}_stock_data.csv"
            df.to_csv(file_path, index=True)
            logging.info(f"{Fore.MAGENTA}[SAVE]{Style.RESET_ALL} Saved {ticker} data to {file_path}")

