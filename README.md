# FinGPT-Agents

A multi-agent RAG system for asking questions about SEC 10-K filings using local LLMs.

Built as a study in **grounded financial Q&A** — answering questions about long, dense regulatory documents without hallucinating, using a fully local stack (no API costs, no data leakage).

## The problem with single-shot LLM analysis of 10-Ks

A single Apple 10-K is 100–200 pages. You cannot stuff all of it into one LLM call:

- **Context dilution** — even with long context windows, retrieval precision drops sharply when the model has to find a specific fact in a sea of unrelated content.
- **Cost / latency** — long contexts are expensive on commercial APIs and slow on local models.
- **No source attribution** — when the model answers, you can't tell which page or section it pulled from.

FinGPT-Agents splits the work across specialist agents with structured handoffs.

## Architecture

```
Raw 10-K PDFs
    ↓
[DataIngestionAgent]   → Extract text (pdfplumber + OCR fallback for scans)
    ↓
[DataProcessingAgent]  → Chunk text, embed with Ollama, build FAISS index
    ↓
[RAGAgent]             → For each question:
                          1. Embed the question
                          2. Retrieve top-k relevant chunks from FAISS
                          3. Send chunks + question to local LLM
                          4. Return grounded answer
    ↓
Answer + retrieved source chunks
```

**Key design choices:**

- **Local-first stack** (Ollama + FAISS). No API costs, no data leaving the machine. Important for financial filings in a production setting where firms can't send their analysis queries to external APIs.
- **Separate ingestion, processing, and retrieval** as distinct agents — each is independently testable and swappable. Want a different embedding model? Replace one agent.
- **FAISS for vector storage** — fast similarity search at scale. A single 10-K produces thousands of chunks; linear search would kill latency.
- **Retrieval before generation** — the LLM only sees the chunks most relevant to the question, not the whole filing. This is what keeps the answers grounded and cheap.

## Stack

Python 3.10+ · Ollama (local LLM, default `llama3`) · FAISS (vector store) · LangChain (RAG orchestration) · pdfplumber (PDF text extraction)

## Quick start

```bash
git clone https://github.com/KrishnanshSood/fingpt-agents
cd fingpt-agents

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Install Ollama from https://ollama.com and pull a model
ollama pull llama3

# Drop 10-K PDFs in data/filings/, named AAPL_10K_<year>.pdf
python run_rag_agent.py
```

Full setup (Tesseract, Poppler for OCR fallback on scanned PDFs) in [SETUP.md](./SETUP.md).

## Example session

After ingesting Apple's 2023 10-K, you can ask:

```
Q: What were Apple's top risk factors mentioned in the 2023 10-K?

A: Based on the retrieved sections, Apple identified the following key risk factors:
1. Macroeconomic conditions affecting consumer spending on premium devices
2. Supply chain concentration in specific geographic regions
3. Foreign exchange volatility (a majority of revenue is non-USD)
4. Intense competition in services and wearables categories
5. Regulatory scrutiny around App Store practices

[Retrieved from Item 1A — Risk Factors, pages 6–18]
```

The answer is grounded in retrieved chunks rather than the model's training-data memory of Apple, which is critical for financial accuracy (training cutoffs differ from filing dates).

## Limitations (honest ones)

- **Tested on AAPL filings.** The system is architecture-agnostic, but every new ticker requires placing PDFs in `data/filings/` and re-indexing.
- **No cross-filing reasoning yet.** The RAG retrieval is per-question; comparing "How did Apple's R&D spend change from 2020 to 2023?" still relies on the LLM stitching together separately-retrieved chunks.
- **No automatic eval.** Quality is currently judged by spot-checking answers against source PDFs. A real eval set with ground-truth Q&A pairs is on the roadmap.

## What's next

- **Cross-filing comparison agent** — for year-over-year and multi-company queries
- **Skeptic-validation agent** that flags low-confidence answers before returning them (drawing on the verifier pattern from a separate research project)
- **Web UI** (Streamlit) so non-technical users can ingest filings and ask questions without setting up Ollama themselves
- **Quantitative eval set** — 50 questions with ground-truth answers from real 10-Ks, measuring per-question accuracy and citation quality

## Author

[Krishnansh Sood](https://github.com/KrishnanshSood) · BITS Pilani · AI/ML