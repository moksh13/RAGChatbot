# Product Requirement Document (PRD)

## Project: Mutual Fund Facts-Only RAG Assistant (Class Demo)

---

### 1. Document Control & Overview
- **Project Name:** Mutual Fund Facts-Only FAQ Assistant
- **Target Release:** Class Demonstration Prototype
- **Status:** Draft / Active
- **Author:** AI Engineering Team
- **Deployment Target:** Localhost & Render (Free Tier)

---

### 2. Goal & Vision
The goal of this project is to build a reliable, lightweight, facts-only Retrieval-Augmented Generation (RAG) conversational assistant for mutual fund schemes. Designed specifically for a live class demonstration, the assistant delivers precise, verifiable answers about mutual fund schemes using exclusively official, public documentation.

#### Core Objectives:
1. **Zero Hallucination / Facts-Only Grounding:** Answer factual inquiries (expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, statement guides) using only ingested scheme documents.
2. **Mandatory Citations & Brevity:** Every answer must provide exactly one official source link, stay concise (≤3 sentences), and include a data freshness tag (`Last updated from sources: <date>`).
3. **Strict Boundary Enforcement:** Proactively reject investment advice, buy/sell recommendations, portfolio balancing questions, and performance forecasts with educational disclaimers.
4. **Privacy by Design:** Strictly decline and avoid capturing Personally Identifiable Information (PII) such as PAN, Aadhaar, folio numbers, or contact details.

---

### 3. Target Users
1. **Retail Mutual Fund Investors:** Beginners and self-directed investors seeking quick, unambiguous factual information regarding fund parameters without wading through 50-page Scheme Information Documents (SID).
2. **Support & Operations Teams:** Customer-facing teams seeking consistent, automated retrieval of repetitive scheme facts and compliance-verified links.
3. **Academic Evaluators / Demo Audience:** Class reviewers evaluating end-to-end RAG architecture, retrieval precision, prompt engineering guardrails, chunking strategy transparency, and zero-cost cloud deployment.

---

### 4. Corpus Scope (HDFC AMC Schemes)
The knowledge corpus is strictly bounded to five public direct-growth schemes under **HDFC Mutual Fund**:
1. **Large Cap:** [HDFC Large Cap Fund (Direct - Growth)](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth)
2. **Flexi Cap:** [HDFC Flexi Cap Fund (Direct - Growth)](https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth)
3. **ELSS (Tax Saver):** [HDFC ELSS Tax Saver Fund (Direct - Growth)](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth)
4. **Small Cap:** [HDFC Small Cap Fund (Direct - Growth)](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth)
5. **Balanced Advantage (Hybrid):** [HDFC Balanced Advantage Fund (Direct - Growth)](https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth)

*Supplementary Public Resources:* Official SID/KIM PDFs, AMFI/SEBI fact guides, and official statement download guides.

---

### 5. In-Scope & Out-of-Scope Features

| Area | In-Scope Features | Out-of-Scope (Non-Goals) |
| :--- | :--- | :--- |
| **Domain & Data** | • Fact retrieval across the 5 scoped HDFC schemes.<br>• Extraction of expense ratio, exit load, minimum SIP/lumpsum, lock-in period, riskometer rating, and benchmark.<br>• Guidance on downloading capital-gains and account statements via official portals. | • Any scheme outside the 5 designated HDFC funds.<br>• Unofficial third-party blog posts, speculative news, or forum opinions.<br>• Dynamic web scraping at runtime. |
| **RAG Pipeline** | • Offline ingestion pipeline (Extract → Chunk → Embed → Store).<br>• Local embeddings with `sentence-transformers/all-MiniLM-L6-v2` (384-dim).<br>• Persistent local vector storage via ChromaDB.<br>• Inspection output: Export of all chunks into a readable `chunks.txt` file.<br>• Context-aware retrieval with similarity scoring and top-k filtering. | • Live re-indexing on every query or restart.<br>• Expensive proprietary vector databases (Pinecone, Weaviate Cloud).<br>• Multi-hop complex agent workflows. |
| **Generation & Guardrails** | • Ultra-concise answers (≤ 3 sentences).<br>• Inclusion of exactly one validated source URL per answer.<br>• Inclusion of `Last updated from sources: <date>`.<br>• Refusal of opinionated queries ("Should I buy?", "Best fund?") with standard educational fallback.<br>• PII detector & refusal rule (PAN, Aadhaar, OTP, email, phone).<br>• No performance comparison or return prediction. | • Personalized investment advisory or portfolio optimization.<br>• Complex multi-turn historical chat memory beyond immediate context.<br>• Calculating future returns or simulating SIP values. |
| **User Interface** | • Tiny, responsive UI (e.g., Streamlit / Gradio / FastAPI+HTML).<br>• Prominent welcome banner.<br>• Mandatory disclaimer: *"Facts-only. No investment advice."*<br>• 3 one-click sample query buttons.<br>• Citation links rendered as clickable URLs. | • User authentication, user profiles, or session history persistence.<br>• Payment gateways or direct order placement / transaction routing.<br>• Mobile native apps (iOS / Android). |

---

### 6. Example User Questions & Expected Behaviors

#### In-Scope (Factual Queries)
1. **Query:** *"What is the expense ratio and exit load for HDFC Large Cap Fund Direct Growth?"*
   - **Behavior:** Retrieves relevant scheme chunks, outputs expense ratio and exit load in ≤3 sentences, displays 1 source link to the HDFC Large Cap scheme page, and includes the update date.
2. **Query:** *"Does HDFC ELSS Tax Saver Fund have any lock-in period?"*
   - **Behavior:** States the statutory 3-year lock-in period under Section 80C, provides the direct source link, and completes within 3 sentences.
3. **Query:** *"What is the minimum SIP investment for HDFC Small Cap Fund?"*
   - **Behavior:** Returns minimum SIP amount (e.g., ₹100 or ₹500 as documented) with citation.
4. **Query:** *"What is the benchmark and riskometer level of HDFC Balanced Advantage Fund?"*
   - **Behavior:** Outputs the benchmark index (e.g., NIFTY 50 Hybrid Composite Debt 50:50 Index) and risk classification (e.g., Very High Risk) with official link.
5. **Query:** *"How do I download my mutual fund capital gains statement?"*
   - **Behavior:** Provides concise instructions to download statements from CAMS/KFintech or AMC portal with the direct link.

#### Out-of-Scope (Refusal & Guardrail Queries)
1. **Query:** *"Should I invest in HDFC Small Cap or HDFC Flexi Cap for higher returns this year?"*
   - **Behavior:** **Refused.** Responds with: *"I provide factual information only and do not give investment advice or return projections. Please consult a SEBI-registered financial advisor."* Includes a link to the official factsheet.
2. **Query:** *"My PAN is ABCDE1234F. Can you check my folio balance?"*
   - **Behavior:** **Refused.** Responds with: *"For your security, please do not share personal details like PAN, Aadhaar, or folio numbers. I cannot access personal investor accounts."*
3. **Query:** *"Will HDFC Large Cap Fund beat the NIFTY 50 index next quarter?"*
   - **Behavior:** **Refused.** Refuses speculative predictions and points to historical factsheet facts only.

---

### 7. Constraints & Technical Architecture

#### Free-Tier & Zero-Cost Budget Constraints
- **Zero API Spend:** All components must operate within standard free-tier allocations or local computation.
- **LLM Engine:** Groq API using free-tier models (`llama-3.1-8b-instant` or `llama-3.3-70b-versatile`) offering sub-second response times without billing requirements. API keys stored strictly in `.env` and excluded via `.gitignore`.
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`:
  - 384-dimensional dense vectors.
  - Runs 100% locally on CPU without requiring an external API key or network calls.
- **Vector Database:** `ChromaDB` (embedded file-based storage):
  - Pre-ingested vector index saved directly to disk (`./chroma_db`).
  - Read-only queries during runtime to conserve memory and avoid re-indexing overhead on container boots.
- **Chunk Inspection File:** Export of all generated text chunks with metadata into `chunks.txt` for auditability before vector indexing.

#### Execution & Deployment Constraints
- **Local Execution:**
  - Runs on standard developer workstations (Windows/Linux/macOS) with Python 3.10+.
  - CPU-only footprint without CUDA dependency.
- **Deployable to Render (Free Web Service):**
  - **Memory Limit:** Must fit within Render's 512 MB RAM limit.
  - **Mitigation Strategy:** Pre-build the Chroma vector database locally or during build time; load the lightweight MiniLM-L6-v2 model using ONNX or optimized PyTorch CPU runtime; avoid heavy in-memory operations.
  - **Packaging:** Standard `requirements.txt` with locked versions and a root `Procfile` / start command (e.g., `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` or `uvicorn main:app --host 0.0.0.0 --port $PORT`).

---

### 8. Success Criteria & Evaluation Metrics

| Metric | Target | Verification Method |
| :--- | :--- | :--- |
| **Factual Accuracy** | 100% grounded in provided documents | Manual review against the 5 source URLs for 10 benchmark factual questions. |
| **Hallucination Rate** | 0% ungrounded assertions | Adversarial testing with unanswerable or absent scheme queries (must answer "Information not found in official source"). |
| **Citation Adherence** | 100% of factual responses have 1 source URL | Automated unit check verifying URL presence and validity in output string. |
| **Response Brevity** | ≤ 3 sentences per response | Automated length and sentence boundary validation. |
| **Guardrail Triggering** | 100% rejection on advice / PII / performance | Evaluation suite testing 5 advice prompts and 3 PII prompts. |
| **Query Latency** | < 3.0 seconds end-to-end | Measured from query input to completed response stream on Groq API. |
| **Resource Footprint** | Peak RAM < 500 MB | Monitored locally and verified on Render free tier deployment. |
| **Demo Readiness** | Clean UI with 3 clickable prompts | Live demonstration with instant answers on sample queries. |

---

### 9. Deliverables Checklist
- [ ] `docs/PRD.md`: This comprehensive requirements specification.
- [ ] `docs/sources.md` / `sources.csv`: Curated inventory of official URLs used for ingestion.
- [ ] `chunks.txt`: Human-readable export of all text chunks, chunk IDs, and associated metadata.
- [ ] Ingestion script (`ingest.py`): Crawler/cleaner, chunker, and ChromaDB indexer.
- [ ] RAG Query Engine (`rag.py`): Vector retrieval, Groq prompt template with guardrails.
- [ ] UI Application (`app.py`): Tiny frontend featuring welcome line, disclaimer, 3 sample questions, and response viewer.
- [ ] `sample_qa.md`: 5–10 sample test queries with verified outputs and source citations.
- [ ] `README.md`: End-to-end local setup instructions, architectural diagram, and Render deployment guide.
