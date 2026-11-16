# Mutual Fund Facts-Only RAG Assistant (Class Demo)

A facts-only, retrieval-augmented conversational assistant that answers factual questions about 5 specific HDFC Mutual Fund schemes and official statement download guides. Built with zero-cost free-tier components, local dense embeddings, persistent ChromaDB, and Groq LLM inference.

---

## 🌟 Key Features
- **Strictly Facts-Only Grounding:** Generates concise answers (≤ 3 sentences) exclusively using official public pages. Zero hallucinations.
- **Mandatory Verified Citations:** Every answer includes the direct official source URL for the scheme or service.
- **Rolling Conversation Memory:** Maintains a sliding window of the last 10 messages and uses an LLM query rewriter to resolve anaphora / follow-up pronouns (e.g. *"what about its fees?"* $\rightarrow$ *"What are the fees for HDFC Large Cap Fund?"*).
- **Two-Tier Guardrail Shield:**
  - Blocks Personally Identifiable Information (PAN, Aadhaar, phone, email, folio numbers).
  - Intercepts investment advice, buy/sell recommendations, and portfolio allocations.
  - Rejects speculative performance claims and future return forecasts.
  - Refuses off-topic questions (sports, weather, recipes, non-scoped AMCs).
  - Falls back to *"I don't know based on the provided official documents"* when context is insufficient.
- **Streamlit Web Interface:** Interactive chat interface featuring:
  - Collapsible **"Retrieved Sources"** expander displaying passage IDs, similarity scores, and content snippets.
  - One-click sample prompt buttons.
  - Sidebar scope inventory and a **Clear Chat** button.

---

## 📚 Scoped Corpus (5 HDFC Schemes + Statement Guide)

| Scheme / Topic | Category | Official Source |
|---|---|---|
| **HDFC Large Cap Fund** (Direct - Growth) | Equity: Large Cap | [Groww Scheme Page](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth) |
| **HDFC Flexi Cap Fund** (Direct - Growth) | Equity: Flexi Cap | [Groww Scheme Page](https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth) |
| **HDFC ELSS Tax Saver Fund** (Direct Plan - Growth) | Equity: ELSS / Tax Saver | [Groww Scheme Page](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth) |
| **HDFC Small Cap Fund** (Direct - Growth) | Equity: Small Cap | [Groww Scheme Page](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth) |
| **HDFC Balanced Advantage Fund** (Direct - Growth) | Hybrid: Dynamic Asset Allocation | [Groww Scheme Page](https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth) |
| **Statement Download Guide** | Capital Gains & CAS Guide | [HDFC Investor Portal](https://www.hdfcfund.com/investor-services/statements) |

---

## 🛠️ Technology Stack
- **Language & Runtime:** Python 3.10+
- **Local Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors, CPU-only, 0 API cost)
- **Vector Database:** `ChromaDB` (embedded, file-based persistence at `data/chroma_db/`)
- **LLM Engine:** Groq Cloud API (`openai/gpt-oss-120b`, `llama-3.3-70b-versatile`, or `openai/gpt-oss-20b` with `temperature=0.0`)
- **Web Interface:** `Streamlit`
- **Environment Management:** `python-dotenv`

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Set Up Environment
```powershell
# Navigate to project directory
cd c:\Users\moksh\Desktop\groww

# Create and activate virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` and add your free Groq API key:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Build & Ingest Vector Database (Run-Once Offline)
```powershell
python -m src.ingest
```
This parses the raw documents, executes the semantic chunking strategy, saves `data/chunks/chunks.txt` (29 chunks), generates 384-dim embeddings, and persists the vector index into `data/chroma_db/`.

---

## 💻 Running the Assistant

### Option 1: Streamlit Web UI (Recommended for Demo)
To launch the interactive chat UI in your browser:
```powershell
streamlit run src/app.py
```
The browser will automatically open at `http://localhost:8501`.

### Option 2: Interactive Terminal / CLI Console
```powershell
python -m src.rag_engine
```
Type any question and press Enter. Type `clear` to reset conversation memory, or `exit` to quit.

### Option 3: Single-Query CLI Mode
```powershell
python -m src.rag_engine "What is the exit load for HDFC Large Cap Fund?"
```

---

## ☁️ Deploying to Render (Free Tier)
This repository is configured for direct deployment on Render:
1. Connect your GitHub repository to [Render](https://render.com).
2. Create a new **Web Service**.
3. Configure the service:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt && python -m src.ingest`
   - **Start Command:** `streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
4. Add Environment Variable:
   - `GROQ_API_KEY`: `<your_groq_api_key>`
   - `GROQ_MODEL`: `openai/gpt-oss-120b`
5. Deploy. The app fits comfortably within Render's 512 MB RAM free limit (< 300 MB peak usage).

---

## 📁 Repository Structure
```text
groww/
├── .env.example                 # Template for environment variables
├── .gitignore                   # Excludes .env, venv, cache, and chroma_db
├── requirements.txt             # Pinned Python package dependencies
├── Procfile                     # Deployment entrypoint for Render
├── README.md                    # Project documentation
├── chunks.txt                   # Exported text chunks for inspection
│
├── docs/                        # Project documentation
│   ├── ProblemStatement.txt     # Original milestone requirements
│   ├── PRD.md                   # Product Requirements Document
│   ├── architecture.md          # End-to-end system architecture
│   ├── implementation.md        # 6-phase implementation roadmap
│   ├── sources.md               # Catalog of official scheme URLs
│   └── sample_qa.md             # Benchmark Q&A evaluation suite
│
├── data/                        # Persistent data directory
│   ├── raw/                     # Authoritative scheme texts (JSON + TXT)
│   ├── chunks/                  # Chunk audit file (data/chunks/chunks.txt)
│   ├── embeddings_preview.txt   # Vector dimensions preview
│   └── chroma_db/               # Persistent ChromaDB vector index
│
└── src/                         # Core Python modules
    ├── __init__.py
    ├── config.py                # Global settings and constants
    ├── data_loader.py           # Loads official scheme documents
    ├── chunker.py               # Section-aware semantic chunking
    ├── vector_store.py          # ChromaDB and SentenceTransformer wrapper
    ├── ingest.py                # Standalone ingestion orchestration script
    ├── guardrails.py            # PII and advice validation filters
    ├── conversation_memory.py   # Rolling conversation history manager
    ├── prompt_templates.py      # Grounded prompt & query rewriter templates
    ├── llm_client.py            # Groq API client
    ├── rag_engine.py            # End-to-end RAG coordinator & CLI
    └── app.py                   # Streamlit web chat UI
```

---

## ⚖️ Compliance & Disclaimer
> **Facts-only. No investment advice.**  
> This application is created strictly for academic and demonstration purposes. It does not provide financial planning, portfolio advisory, or buy/sell recommendations. Mutual fund investments are subject to market risks; please read all scheme-related documents carefully.
