# src/fingpt_agents/filing_downloader/filing_scraper.py

import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from urllib.parse import urljoin
from src.fingpt_agents.utils.logger_utils import logger
from pathlib import Path
import pdfkit  # for HTML -> PDF fallback

BASE_URL = "https://www.sec.gov"
CIK = "0000320193"  # Apple's CIK

HEADERS = {
    "User-Agent": "fingpt-agent-bot (krish@yourdomain.com)",
}

def get_10k_urls(years_back=10):
    logger.info("Fetching 10-K filing URLs for Apple...")
    url = f"https://data.sec.gov/submissions/CIK{CIK}.json"
    resp = requests.get(url, headers=HEADERS)
    data = resp.json()

    ten_ks = []
    filings = data["filings"]["recent"]
    for i, form in enumerate(filings["form"]):
        if form == "10-K":
            acc_no = filings["accessionNumber"][i].replace("-", "")
            year = filings["filingDate"][i][:4]
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{acc_no}/index.json"
            ten_ks.append((year, filing_url))
            if len(ten_ks) >= years_back:
                break
    return ten_ks

def get_pdf_or_html_url(filing_json_url):
    resp = requests.get(filing_json_url, headers=HEADERS)
    data = resp.json()

    for file in data.get("directory", {}).get("item", []):
        name = file["name"]
        if name.endswith(".pdf") and "10-k" in name.lower():
            return ("pdf", urljoin(BASE_URL, filing_json_url.replace("index.json", name)))
        elif name.endswith(".htm") and "10-k" in name.lower():
            return ("html", urljoin(BASE_URL, filing_json_url.replace("index.json", name)))
    return (None, None)

def download_and_save(filing_type, url, year, output_dir="data/filings"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(output_dir, f"AAPL_10K_{year}.pdf")

    if filing_type == "pdf":
        logger.info(f"Downloading native PDF for {year}...")
        resp = requests.get(url, headers=HEADERS)
        with open(filename, "wb") as f:
            f.write(resp.content)
    elif filing_type == "html":
        logger.info(f"Converting HTML to PDF for {year}...")
        pdfkit.from_url(url, filename)
    else:
        logger.warning(f"No suitable 10-K document found for {year}. Skipping.")
        return

    logger.info(f"Saved: {filename}")

def download_apple_10ks(years_back=10):
    filings = get_10k_urls(years_back)
    for year, filing_json_url in tqdm(filings):
        filing_type, download_url = get_pdf_or_html_url(filing_json_url)
        if download_url:
            try:
                download_and_save(filing_type, download_url, year)
                sleep(0.5)
            except Exception as e:
                logger.error(f"Failed to process filing for {year}: {e}")
