# FinGPT-Agents

A multi-agent RAG system for extracting financial insights from SEC 10-K filings. Built to test whether specialist agents with structured handoffs outperform a single-agent baseline on long, noisy financial documents.

**TL;DR:** 3 specialist agents (Ingestion → RAG → Insights) over 500+ 10-K filings, fully local stack (Ollama + FAISS), with a multi-agent controller for orchestration.

---

## Why this exists

Single-agent RAG over financial filings has two failure modes I kept hitting:

1. **Context dilution** — stuffing a 200-page 10-K into one prompt destroys retrieval precision on specific questions (revenue breakdown, risk factors, segment data).
2. **No separation of concerns** — extraction, retrieval, and reasoning all happen in one pass, so when an answer is wrong, you can't tell which stage failed.

This project splits the problem across specialist agents with structured JSON handoffs, so each stage is independently testable and the failure point is always identifiable.

---

## Architecture

```
   ┌─────────────────────┐
   │  Raw 10-K PDFs      │
   └──────────┬──────────┘
              │
   ┌──────────▼──────────┐
   │ DataIngestionAgent  │  PDF parsing + OCR fallback (Tesseract)
   └──────────┬──────────┘
              │
   ┌──────────▼──────────┐
   │ DataProcessingAgent │  Chunking, embedding (Ollama),
   │                     │  FAISS index construction
   └──────────┬──────────┘
              │
   ┌──────────▼──────────┐
   │     RAGAgent        │  Retrieval + grounded QA
   └──────────┬──────────┘
              │
   ┌──────────▼──────────┐
   │   InsightsAgent     │  Synthesis across retrieved chunks,
   │                     │  trend reasoning
   └──────────┬──────────┘
              │
   ┌──────────▼──────────┐
   │MultiAgentController │  Orchestrates the pipeline,
   │                     │  handles agent-to-agent handoffs
   └─────────────────────┘
```

**Key design choices:**
- **Local-first stack** (Ollama + FAISS) — no API costs, no data leaving the machine. Important for financial filings where some users won't send data to external APIs.
- **Structured JSON between agents** — every agent input/output is schema-validated, so I can swap any agent without breaking the pipeline.
- **Separate retrieval and synthesis** — retrieval is judged on chunk relevance, synthesis on answer quality. Decoupled metrics = easier debugging.

---

## Results

Evaluated on a held-out set of [N] questions across [X] companies' filings:

| Metric                | Single-agent baseline | Multi-agent | Δ      |
|-----------------------|-----------------------|-------------|--------|
| Answer accuracy*      | XX%                   | XX%         | +XX%   |
| Avg latency / query   | XXs                   | XXs         | -XX%   |
| Hallucination rate    | XX%                   | XX%         | -XX%   |

*Accuracy judged against ground-truth answers manually extracted from filings.

**What worked:**
- [Specific finding 1 — e.g., "Separating retrieval from synthesis cut hallucinations on numeric questions by Xx"]
- [Specific finding 2]

**What didn't:**
- [Honest limitation — e.g., "Multi-hop questions across multiple filings still fail because the controller doesn't carry retrieved context across agent calls"]

---

## Stack
- **LLM:** Llama 3 via Ollama (local)
- **Vector store:** FAISS
- **Orchestration:** Custom multi-agent controller (LangChain RetrievalQA for the RAG stage)
- **PDF parsing:** pdf2image + Tesseract OCR fallback
- **Language:** Python 3.10+

---

## Run it

```bash
git clone https://github.com/KrishnanshSood/fingpt-agents
cd fingpt-agents
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3 && ollama serve

# Drop 10-K PDFs in data/filings/ as AAPL_10K_<year>.pdf
python run_multi_agent.py
```

Full setup (Tesseract, Poppler) in [SETUP.md](./SETUP.md).

---

## What's next
- Adding a skeptic-validation agent (similar to the one I use in a separate research project) to flag low-confidence answers before they're returned
- Cross-filing reasoning (comparing year-over-year segments)

---

**Author:** [Krishnansh Sood](https://github.com/KrishnanshSood) · BITS Pilani · [LinkedIn](your-link)
