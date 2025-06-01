# run_download_filings.py

from scripts.download_sec_filings import download_apple_10ks
from src.fingpt_agents.utils.logger_utils import logger

if __name__ == "__main__":
    logger.info("[RUN] Downloading Apple 10-K filings as PDFs...")
    download_apple_10ks(years_back=10)
    logger.info("[RUN] Done.")
