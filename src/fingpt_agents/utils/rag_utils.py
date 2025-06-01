import os
from typing import List
from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_path
from src.fingpt_agents.utils.logger_utils import logger

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """
    Extract text from PDF using PyPDF2, and if that fails or no text is found,
    fallback to OCR using pytesseract.
    Returns a list of text chunks (one per page or image).
    """
    logger.info(f"[LOAD] Extracting text from {pdf_path}")
    # Try PyPDF2 text extraction first
    try:
        reader = PdfReader(pdf_path)
        texts = []
        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                texts.append(text)
        if texts:
            logger.info(f"[LOAD] Extracted text using PyPDF2 from {pdf_path}, {len(texts)} pages")
            return texts
        else:
            logger.info(f"[LOAD] No text found via PyPDF2 in {pdf_path}, falling back to OCR")
    except Exception as e:
        logger.error(f"[LOAD] PyPDF2 extraction failed for {pdf_path}: {e}")

    # OCR fallback using pytesseract
    try:
        images = convert_from_path(pdf_path)
        texts = []
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)
            if text and text.strip():
                texts.append(text)
            else:
                logger.warning(f"[LOAD] OCR page {i+1} empty in {pdf_path}")
        logger.info(f"[LOAD] Extracted text using OCR from {pdf_path}, {len(texts)} pages")
        return texts
    except Exception as e:
        logger.error(f"[LOAD] OCR extraction failed for {pdf_path}: {e}")
        return []
