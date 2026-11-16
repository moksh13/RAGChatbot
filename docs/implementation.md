# Implementation Plan: Mutual Fund Facts-Only RAG Assistant

## Overview
This document outlines the phased implementation roadmap for the Mutual Fund Facts-Only RAG Assistant. The plan is organized into 6 sequential phases. Each phase defines the specific files to create, its operational scope, and concrete verification criteria that must pass before advancing to the next phase.

> [!IMPORTANT]
> **No code is to be written during this planning phase.** All steps and architectural decisions must be verified and approved first.

---

### Phase 1: Project Setup & Environment Configuration

#### 1. Files to Create:
- `.env.example`: Template for environment variables (specifying `GROQ_API_KEY`).
- `.env`: Local secrets file containing the active Groq API key (excluded from Git).
- `.gitignore`: Comprehensive ignore rules for `.env`, Python virtual environments (`venv/`, `.venv/`), `__pycache__/`, `data/chroma_db/`, `.DS_Store`, and temporary artifacts.
- `requirements.txt`: Pinned dependencies:
  - `groq`
  - `sentence-transformers`
  - `chromadb`
  - `streamlit`
  - `python-dotenv`
  - `requests`
  - `beautifulsoup4`
- `Procfile`: Command specification for Render deployment (`web: streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`).
- `src/__init__.py`: Package initialization.
- `src/config.py`: Central configuration constants (file paths, ChromaDB collection name, embedding model name `sentence-transformers/all-MiniLM-L6-v2`, Groq model `llama-3.1-8b-instant`, chunking parameters, and max sentence limit).
- `docs/sources.md`: Curated table of the 5 official HDFC scheme URLs plus statement download guide reference.

#### 2. What This Phase Does:
- Establishes a clean, reproducible virtual environment.
- Configures environment security (preventing API keys from ever being committed).
- Defines global path and model constants in `src/config.py` to eliminate hardcoded strings across the codebase.
- Documents the exact public data sources approved for ingestion.

#### 3. How to Verify Before Moving On:
- **Dependency verification:** Run `pip install -r requirements.txt` in a fresh virtual environment.
- **Import validation test:** Run:
  ```powershell
  python -c "import chromadb, sentence_transformers, groq, streamlit, dotenv; print('Environment Setup Successful')"
  ```
- **Git security check:** Run `git status --ignored` to verify that `.env` and `__pycache__` are actively ignored.
- **Config test:** Run `python -c "from src.config import EMBEDDING_MODEL, GROQ_MODEL; print(EMBEDDING_MODEL, GROQ_MODEL)"` and confirm output matches requirements.

---

### Phase 2: Data Acquisition, Loading & Chunking Strategy

#### 1. Files to Create:
- `data/raw/hdfc_large_cap.json`: Clean, factual attributes of HDFC Large Cap Fund (AUM, expense ratio, exit load, min SIP/lumpsum, riskometer, benchmark, fund manager, URL).
- `data/raw/hdfc_flexi_cap.json`: Factual attributes of HDFC Flexi Cap Fund.
- `data/raw/hdfc_elss_tax_saver.json`: Factual attributes of HDFC ELSS Tax Saver Fund (including 3-year statutory lock-in, Section 80C).
- `data/raw/hdfc_small_cap.json`: Factual attributes of HDFC Small Cap Fund.
- `data/raw/hdfc_balanced_advantage.json`: Factual attributes of HDFC Balanced Advantage Fund (Hybrid).
- `data/raw/statement_guide.json`: Factual guide on downloading mutual fund capital gains statements & account statements via CAMS / KFintech / HDFC MF portal.
- `src/data_loader.py`: Module to parse and normalize the raw scheme data into standardized document representations.
- `src/chunker.py`: Custom chunking engine implementing the defined chunking strategy:
  - Target chunk size: 350–500 characters.
  - Chunk overlap: 50 characters.
  - Preserves atomic facts (does not split numerical tables or compound financial terms).
  - Enriches every chunk with metadata: `chunk_id`, `scheme_name`, `category`, `source_url`, `last_updated`.
- `chunks.txt`: Human-readable export of all generated chunks, IDs, and metadata for inspection.

#### 2. What This Phase Does:
- Collates authoritative public data from the 5 designated Groww/HDFC public scheme URLs.
- Executes the chunking strategy to convert scheme documents into dense, queryable passages.
- Produces the mandatory `chunks.txt` artifact allowing manual audit of every chunk before embedding.

#### 3. How to Verify Before Moving On:
- **Execution test:** Run `python -m src.chunker` to generate `chunks.txt`.
- **Chunk inspection:** Open `chunks.txt` and verify:
  1. No chunk has missing `source_url` or `scheme_name` metadata.
  2. Numbers (e.g. exit load `1% if redeemed within 1 year`, lock-in `3 years`, expense ratio) remain intact and contextual within their chunk.
  3. Total chunk count is reasonable (e.g., 25–40 chunks across all 5 schemes and statement guide).
- **Format assertion:** Assert that every chunk separator has readable headers:
  ```text
  --- CHUNK ID: hdfc_elss_002 ---
  Scheme: HDFC ELSS Tax Saver Fund
  Source URL: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth
  Content:
  HDFC ELSS Tax Saver Fund has a mandatory lock-in period of 3 years under Section 80C of the Income Tax Act...
  ```

---

### Phase 3: Local Embedding & Persistent Vector Store (ChromaDB)

#### 1. Files to Create:
- `src/vector_store.py`: Vector database manager wrapping ChromaDB:
  - Local embedding function wrapper loading `sentence-transformers/all-MiniLM-L6-v2`.
  - Collection creation, persistent disk access (`data/chroma_db/`), and batch document addition.
  - Vector similarity query method returning top-k matching documents with distance scores and metadata.
- `src/ingest.py`: Standalone CLI script orchestrating Phase 2 and Phase 3:
  - Reads loaded documents $\rightarrow$ Chunks via `chunker.py` $\rightarrow$ Writes `chunks.txt` $\rightarrow$ Generates embeddings $\rightarrow$ Persists to `./data/chroma_db/`.

#### 2. What This Phase Does:
- Initializes the CPU-friendly `sentence-transformers/all-MiniLM-L6-v2` model locally (384-dimensional dense vectors, zero API cost).
- Creates an offline, durable ChromaDB database on disk.
- Ensures ingestion is strictly run-once offline so the web application loads instantly without re-embedding on startup.

#### 3. How to Verify Before Moving On:
- **Ingestion test:** Run `python -m src.ingest`.
- **Database persistence check:** Verify that `./data/chroma_db/` exists, contains `chroma.sqlite3`, and is populated.
- **Retrieval verification query:** Run a standalone verification test:
  ```powershell
  python -c "from src.vector_store import VectorStore; vs = VectorStore(); results = vs.query('What is the lock-in period for ELSS?', k=2); print(results[0]['metadata']['scheme_name']); print(results[0]['content'])"
  ```
- **Assertion:** The top result must explicitly mention `HDFC ELSS Tax Saver Fund` and the `3-year lock-in` with similarity score indicating high relevance.

---

### Phase 4: Guardrails & Defensive Intent Filters

#### 1. Files to Create:
- `src/guardrails.py`: Core guardrail module implementing two defensive layers:
  1. `check_pii(text) -> Optional[str]`: Regex detector targeting Indian PAN cards (`[A-Z]{5}[0-9]{4}[A-Z]`), 12-digit Aadhaar sequences, phone numbers (`(\+91|0)?[6-9]\d{9}`), email addresses, and account/folio numbers.
  2. `check_advice_intent(text) -> Optional[str]`: Pattern and keyword filter intercepting opinionated, portfolio, or speculative queries (e.g., *"should I buy"*, *"which fund is best"*, *"predict returns"*, *"will it beat"*, *"recommend a fund"*).
  3. Predefined, polite refusal responses accompanied by official educational links and factsheet URLs.

#### 2. What This Phase Does:
- Enforces statutory and project safety requirements before any query touches the vector store or LLM.
- Prevents storage or processing of user PII.
- Upholds the "Facts-Only, No Investment Advice" mandate with polite, informative fallback responses.

#### 3. How to Verify Before Moving On:
- **Automated test script:** Run a test suite `python -m src.guardrails` evaluating test cases:
  - *Test 1 (PII - PAN):* Query `"My PAN is ABCDE1234F, show my funds"` $\rightarrow$ Returns privacy rejection warning.
  - *Test 2 (PII - Phone):* Query `"Call me at 9876543210 about ELSS"` $\rightarrow$ Returns privacy rejection warning.
  - *Test 3 (Advice):* Query `"Should I invest in HDFC Small Cap or Flexi Cap?"` $\rightarrow$ Returns investment advice disclaimer + factsheet URL.
  - *Test 4 (Speculation):* Query `"What returns will HDFC Large Cap give next year?"` $\rightarrow$ Returns performance disclaimer + factsheet URL.
  - *Test 5 (Valid factual query):* Query `"What is the exit load for HDFC Large Cap?"` $\rightarrow$ Returns `None` (passes through to retrieval).

---

### Phase 5: Retrieval + Grounded Groq LLM Answer Generation

#### 1. Files to Create:
- `src/prompt_templates.py`: Strict system prompt template enforcing:
  - Grounding exclusively on provided context chunks.
  - Hard constraint: Maximum 3 sentences.
  - Hard constraint: Exactly 1 valid citation link matching the scheme URL.
  - Inclusion of freshness indicator: `"Last updated from sources: <date>"`.
  - Fallback rule: If the information is not present in the context, explicitly state: *"This factual information is not available in the official scheme documents."*
- `src/llm_client.py`: Groq API wrapper:
  - Connects using `GROQ_API_KEY`.
  - Defaults to `llama-3.1-8b-instant`.
  - Sets `temperature=0.0` for deterministic, factual adherence.
  - Handles network timeouts and rate-limit retries gracefully.
- `src/rag_engine.py`: Orchestration coordinator:
  - Connects Guardrails $\rightarrow$ Query Embedding $\rightarrow$ ChromaDB Retrieval $\rightarrow$ Prompt Formatting $\rightarrow$ Groq Completion.
- `docs/sample_qa.md`: Verification artifact containing 5–10 real test questions, retrieved chunk summaries, generated responses, and source links.

#### 2. What This Phase Does:
- Synthesizes the retrieved vector context into natural language answers strictly abiding by all constraints (≤3 sentences, 1 citation link, facts-only).
- Generates the benchmark `sample_qa.md` file required for milestone submission.

#### 3. How to Verify Before Moving On:
- **CLI query tests:** Run `python -m src.rag_engine "What is the exit load for HDFC Large Cap Fund?"`.
- **Response checks:** Verify the output:
  1. Contains accurate exit load details.
  2. Sentence count is $\le 3$.
  3. Includes exact URL: `https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth`.
  4. Ends with `"Last updated from sources: [Date]"`.
- **Out-of-domain test:** Run `python -m src.rag_engine "Who won the cricket world cup?"` $\rightarrow$ Asserts refusal or "Information not found in scheme documents."
- **Generation of `docs/sample_qa.md`:** Run a test harness that executes 8 standard queries and saves the formatted results to `docs/sample_qa.md`.

---

### Phase 6: User Interface (UI), Documentation & Deployment Readiness

#### 1. Files to Create:
- `src/app.py`: Streamlit web interface featuring:
  - Clean title & welcome banner.
  - Prominent disclaimer box: *"Facts-only. No investment advice."*
  - 3 clickable quick-question buttons:
    1. *"What is the expense ratio & exit load of HDFC Large Cap Fund?"*
    2. *"What is the lock-in period for HDFC ELSS Tax Saver Fund?"*
    3. *"How can I download my capital gains statement?"*
  - Chat input box and conversation view with formatted Markdown and clickable hyperlinks.
- `README.md`: Comprehensive project documentation:
  - Project summary & demo link/video.
  - Architecture diagram and RAG pipeline explanation.
  - Step-by-step local setup instructions.
  - Scope details (5 HDFC schemes and source links).
  - Known limits and guardrail policies.
  - Render deployment walkthrough.

#### 2. What This Phase Does:
- Delivers an intuitive, clean graphical user interface for live class demonstration.
- Packages the entire project for 1-click execution locally and deployment to Render free tier.
- Verifies that memory usage remains strictly under Render's 512 MB RAM ceiling.

#### 3. How to Verify Before Moving On:
- **Local UI execution:** Run `streamlit run src/app.py` in browser.
- **Button interaction test:** Click each of the 3 sample question buttons and verify immediate, correctly rendered answers with working links.
- **Custom input test:** Type both valid and invalid queries (PII, advice, unanswerable) and ensure appropriate responses.
- **Memory profiling:** Measure peak RAM usage under load using:
  ```powershell
  Get-Process -Name python | Select-Object ProcessName, @{Name="RAM (MB)"; Expression={[math]::round($_.WorkingSet64 / 1MB, 2)}}
  ```
  Ensure total RAM stays well below 350 MB.
- **Render build check:** Verify `requirements.txt` and `Procfile` are complete and can be built cleanly in a headless environment.

---

### Phase Execution Dependency Matrix

```
[ Phase 1: Setup & Env ]
          |
          v
[ Phase 2: Data & Chunking ]  --> Outputs: chunks.txt
          |
          v
[ Phase 3: Vector Store ]     --> Outputs: data/chroma_db/
          |
          v
[ Phase 4: Guardrails ]       --> Outputs: PII & Advice Filters
          |
          v
[ Phase 5: RAG Engine ]       --> Outputs: docs/sample_qa.md
          |
          v
[ Phase 6: UI & Deployment ]  --> Outputs: src/app.py & README.md
```
