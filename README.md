
# 🧠 Fingpt Agents — Financial Research Assistant using Local LLMs

Fingpt Agents is a modular, agent-based financial research assistant that leverages Retrieval-Augmented Generation (RAG) using 10-K filings and local LLMs. It enables users to ask natural-language questions about a company's filings and get intelligent, contextual answers — all running **fully locally**.

---

## 🚀 Features

- 🔍 Extracts and indexes 10-K filings (PDFs) using text extraction + OCR fallback
- 🧠 Embeds text using local Ollama models (`llama3`, etc.)
- 📦 Stores vector embeddings in FAISS for efficient retrieval
- 🤖 Uses RetrievalQA from LangChain to generate insights
- 📁 Modular agent system (e.g. RAGAgent, DataIngestionAgent, etc.)
- 📉 Designed for analyzing companies like AAPL using real filings

---

## 📁 Project Structure

```
ffingpt-agents/
├── data/
│   ├── filings/                   # Apple 10-K PDFs stored here
│   └── stocks/                    # Stock CSVs (AAPL, MSFT, GOOGL)
├── run_data_ingestion_agent.py   # Script to run DataIngestionAgent
├── run_processing_agent.py       # Script to run DataProcessingAgent
├── run_rag_agent.py              # Script to run RAGAgent
├── run_multi_agent.py            # Script to run all agents together
├── src/
│   └── fingpt_agents/
│       ├── agents/
│       │   ├── base_agent.py
│       │   ├── data_ingestion_agent.py
│       │   ├── data_processing_agent.py
│       │   ├── insights_agent.py
│       │   ├── rag_agent.py
│       │   └── multi_agent_controller.py
│       ├── utils/
│       │   ├── logger_utils.py
│       │   └── rag_utils.py
├── scripts/
│   └── download_10k_filings.py   # Downloads Apple 10-K filings (PDF)
├── requirements.txt              # Python dependencies
├── README.md                     # ← This file
```

---

## 🛠️ Setup Instructions

### 1. 🐍 Clone and Setup Virtual Environment

```bash
git clone https://github.com/KrishnanshSood/fingpt-agents.git
cd fingpt-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. 📦 Install Required System Dependencies

#### ✅ Tesseract OCR (for image-based PDFs)

- **Windows**: Download installer from [here](https://github.com/tesseract-ocr/tesseract). Add installation path (e.g., `C:\Program Files\Tesseract-OCR`) to your system `PATH`.
- **Linux**:
  ```bash
  sudo apt install tesseract-ocr
  ```
- **macOS**:
  ```bash
  brew install tesseract
  ```

#### ✅ Poppler (required by `pdf2image`)

- **Windows**: [Download Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) and add `bin/` directory to PATH.
- **Linux**:
  ```bash
  sudo apt install poppler-utils
  ```
- **macOS**:
  ```bash
  brew install poppler
  ```

---

### 3. 🤖 Install and Run Ollama

Ollama is required to run local LLMs like `llama3`.

- Download Ollama from: https://ollama.com/
- Pull the model used:
  ```bash
  ollama pull llama3
  ```
- Start the Ollama server:
  ```bash
  ollama run llama3
  ```

Make sure it's running at `http://localhost:11434`.

---

## 📥 Add Data

Place all AAPL 10-K PDFs in the following folder:

```
data/filings/
├── AAPL_10K_2024.pdf
├── AAPL_10K_2023.pdf
├── ...
```

> Filenames must follow the format `AAPL_10K_<year>.pdf`.

---

## ▶️ Run the RAG Agent

Once setup is complete, run:

```bash
python run_rag_agent.py
```

You will see logs indicating PDF text extraction, embedding generation, and a QA chain running. Then you'll be prompted with a question answered using 10-K filings.

---

## 🧩 Coming Soon / Ideas

- 📊 Visualization agent for charts/graphs
- 🗂️ Support other formats (HTML, DOCX)
- 🌐 Web UI using Streamlit
- 🕵️‍♂️ Trend and sentiment analysis agent

---

## 📄 License

MIT License

---

## 🙋‍♂️ Author

[Krishnansh Sood](https://github.com/KrishnanshSood)
