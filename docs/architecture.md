# Architecture Specification

## Mutual Fund Facts-Only RAG Assistant (Class Demo)

---

### 1. Architectural Overview
This document defines the system architecture, component responsibilities, data flow, tech stack, and directory structure for the **Mutual Fund Facts-Only RAG Chatbot**. 

The architecture implements a modular, two-stage Retrieval-Augmented Generation (RAG) system:
1. **Offline Ingestion Pipeline:** Extracts, chunks, embeds, and indexes official scheme documents into a persistent local vector database.
2. **Online Query & Generation Pipeline:** Accepts user queries, filters for advice/PII guardrails, performs vector similarity retrieval, constructs grounded prompts, and generates concise, cited responses via the Groq LLM API.

---

### 2. High-Level Component Architecture

```
+-----------------------------------------------------------------------------------------+
|                                    USER INTERFACE                                       |
|  [ Streamlit / Tiny Web UI ]                                                            |
|  - Welcome banner & "Facts-only. No investment advice." disclaimer                     |
|  - 3 Quick-start sample question buttons                                                |
|  - Chat input box and citation-rich answer display                                      |
+--------------------------------------------+--------------------------------------------+
                                             | User Query
                                             v
+-----------------------------------------------------------------------------------------+
|                                APPLICATION CONTROLLER & GUARDRAILS                       |
|  [ app.py / rag_engine.py ]                                                             |
|  - Input Validation: PII detection (PAN, Aadhaar, phone, email)                         |
|  - Intent Guardrails: Flags advice/portfolio queries ("Should I buy?", "Best return?")   |
+----------------------+-------------------------------------+----------------------------+
                       | Standard Factual Query              | Rejected (Advice/PII)
                       v                                     v
+--------------------------------------+      +-------------------------------------------+
|          RETRIEVAL PIPELINE          |      |             GUARDRAIL FALLBACK            |
|  - Question Embedding (MiniLM-L6-v2) |      | Return polite educational refusal message |
|  - Cosine Similarity Query (Top-K)   |      | + Official Factsheet URL                  |
+----------------------+---------------+      +-------------------------------------------+
                       |
                       | Retrieved Relevant Chunks + Metadata (URL, Scheme Name)
                       v
+-----------------------------------------------------------------------------------------+
|                               PROMPT ASSEMBLY & GENERATION                              |
|  - Strict System Prompt (≤3 sentences, 1 citation link, facts-only constraint)          |
|  - Groq API Client (Llama 3.1 / 3.3 Instant Inference)                                  |
+--------------------------------------------+--------------------------------------------+
                                             |
                                             v
                                  Final Grounded Response
```

---

### 3. Detailed Data Flow

#### Stage 1: Ingestion Pipeline (Run-Once Offline)
```
[ Official Sources ] 
 (5 HDFC Scheme URLs / Factsheets / KIM / SID)
         |
         v
  1. Load & Extract (ingest.py)
     - Reads raw scheme facts, fees, riskometers, benchmarks, exit loads, lock-ins.
     - Strips navigation boilerplate and extracts clean text blocks.
         |
         v
  2. Chunking Engine
     - Splits documents into manageable segments (e.g., 300–500 characters, 50-char overlap).
     - Attaches metadata: `scheme_name`, `category`, `source_url`, `last_updated`.
     - Exports all generated chunks to `chunks.txt` for audit and inspection.
         |
         v
  3. Local Embedding Generator
     - Model: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors).
     - Runs 100% locally on CPU without API keys.
         |
         v
  4. Vector Database Storage
     - Database: `ChromaDB` (persistent file-based mode saved to `./data/chroma_db/`).
     - Stores embeddings, raw text chunks, and metadata for fast nearest-neighbor lookup.
```

#### Stage 2: Query & Generation Pipeline (Online Runtime)
```
[ User Input Query ]
         |
         v
  1. Guardrail & Pre-Check
     - Check 1: Does input contain PII (e.g., PAN regex `[A-Z]{5}[0-9]{4}[A-Z]`, phone, email)?
       -> If yes: Short-circuit with privacy warning.
     - Check 2: Does input request opinion/advice ("should I invest", "predict NAV", "which is best")?
       -> If yes: Short-circuit with educational disclaimer & official factsheet link.
         | (Passes Checks)
         v
  2. Query Vectorization
     - Embed user question using the same `all-MiniLM-L6-v2` model instance.
         |
         v
  3. Vector Similarity Retrieval
     - Query ChromaDB collection with `n_results=3` (or top similarity threshold).
     - Retrieve top-matching text chunks and metadata (Scheme Name, Source URL).
         |
         v
  4. Context & Prompt Construction
     - Populate strict prompt template:
       * Instruction: "Answer the question using ONLY the context provided below. Max 3 sentences. Provide exactly 1 source link. Append 'Last updated from sources: <date>'."
       * Context: Injected top chunks + source URLs.
       * Question: User's original query.
         |
         v
  5. Groq LLM Inference
     - API Call to Groq endpoint (`llama-3.1-8b-instant`).
     - Low latency (typically < 1s), zero cost on free tier.
         |
         v
  6. Response Rendering
     - Formats output with clean Markdown, active clickable hyperlink, and update badge.
     - Displays in web UI.
```

---

### 4. Query Flow Diagram (Text / ASCII)

```text
========================================================================================
                                    ONLINE QUERY FLOW
========================================================================================

    [ User Question ]
           |
           v
   +---------------+
   | Guardrail Check |
   +---------------+
           |
           +----> [Triggered: Advice / PII] ----> Output Predefined Rejection + Source Link
           |
           | (Passed: Factual Query)
           v
   +-------------------------------------------------------+
   | Embed Question (sentence-transformers/all-MiniLM-L6-v2) |
   +-------------------------------------------------------+
           |
           v [384-dim vector]
   +-------------------------------------------------------+
   | ChromaDB Query (Nearest Neighbors: Top-k Chunks)      |
   +-------------------------------------------------------+
           |
           v [Top 3 Chunks + Metadata + Source URLs]
   +-------------------------------------------------------+
   | System Prompt Assembler                               |
   | - Constraints: Facts-only, <=3 sentences, 1 URL       |
   | - Injected Retrieved Context                          |
   | - User Question                                       |
   +-------------------------------------------------------+
           |
           v
   +-------------------------------------------------------+
   | Groq Cloud API (Llama 3.1 8B Instant)                 |
   +-------------------------------------------------------+
           |
           v [Generated Fact-Grounded Response]
   +-------------------------------------------------------+
   | UI Response Renderer (Markdown + Clickable Link)       |
   +-------------------------------------------------------+
           |
           v
    [ User Screen ]

========================================================================================
```

---

### 5. Technology Stack & Rationale

| Layer | Component / Tool | Version / Spec | Why Chosen |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.10+ | Standard ecosystem for AI/RAG, native ChromaDB and HuggingFace support. |
| **Local Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` | PyTorch / ONNX | Runs completely locally on CPU; produces compact 384-dim vectors; fast, accurate, 0 API cost. |
| **Vector Database** | `ChromaDB` | Embedded (`chromadb`) | Zero server management; persists directly to local directory (`./data/chroma_db`); low RAM footprint. |
| **LLM Inference** | `Groq API` | `llama-3.1-8b-instant` | Ultra-fast inference (< 1 sec TTFT); generous free tier; reliable instruction-following for guardrails. |
| **UI Framework** | `Streamlit` | Lightweight Web App | Rapid prototyping, interactive quick-prompt buttons, minimal frontend boilerplate. |
| **Environment Mgmt** | `python-dotenv` | Standard | Keeps Groq API keys secure and outside version control (`.env`). |
| **Deployment Target**| `Render` (Free Tier) | Web Service | Python runtime, git-push deployment, pre-built index support fitting within 512MB RAM. |

---

### 6. Project Directory & Folder Structure

```text
groww/
│
├── .env.example                 # Template for environment variables (GROQ_API_KEY)
├── .gitignore                   # Ignores .env, virtualenvs, __pycache__, chroma_db/
├── requirements.txt             # Locked Python dependencies
├── Procfile                     # Deployment entrypoint for Render
├── README.md                    # Project overview, setup steps, and usage guide
├── chunks.txt                   # Exported text chunks for evaluation & transparency
│
├── docs/                        # Project documentation
│   ├── ProblemStatement.txt     # Original milestone brief & requirements
│   ├── PRD.md                   # Product Requirements Document
│   ├── architecture.md          # System architecture specification (this file)
│   ├── sources.md               # Catalog of 5 official HDFC scheme URLs
│   └── sample_qa.md             # Benchmark Q&A pairs used for testing & verification
│
├── data/                        # Data directory (persisted locally)
│   ├── raw/                     # Raw scheme facts/texts gathered from official sources
│   │   ├── hdfc_large_cap.json
│   │   ├── hdfc_flexi_cap.json
│   │   ├── hdfc_elss_tax_saver.json
│   │   ├── hdfc_small_cap.json
│   │   └── hdfc_balanced_advantage.json
│   └── chroma_db/               # Persistent ChromaDB vector store directory
│
└── src/                         # Application source code
    ├── __init__.py
    ├── config.py                # Configuration (paths, model names, Groq API settings)
    ├── ingest.py                # Ingestion script: reads data, chunks, embeds, saves to ChromaDB & chunks.txt
    ├── chunker.py               # Custom chunking strategy implementation and metadata tagger
    ├── vector_store.py          # ChromaDB client wrapper for adding and querying vectors
    ├── guardrails.py            # PII check regex and advice intent rejection filters
    ├── rag_engine.py            # RAG pipeline coordinator: embed query, retrieve, format prompt, call Groq
    └── app.py                   # Streamlit user interface with sample buttons and disclaimer
```

---

### 7. Key Architecture Design Principles & Guardrails

1. **Deterministic Indexing:**
   - Ingestion (`ingest.py`) is run as a standalone offline script.
   - It populates `data/chroma_db/` once and writes out `chunks.txt`. The web app (`app.py`) only opens ChromaDB in read-only retrieval mode, eliminating runtime indexing latency and saving memory.
2. **Identical Embedding Symmetric Space:**
   - The same embedding model (`sentence-transformers/all-MiniLM-L6-v2`) is used for chunk indexing and user query vectorization to guarantee vector space alignment.
3. **Explicit Metadata Attribution:**
   - Every stored vector chunk contains `source_url`, `scheme_name`, and `last_updated`. During generation, this metadata is injected into the context so the LLM outputs the exact citation URL.
4. **Defensive Prompting & Token Budget:**
   - System prompt instructs the model to refuse speculative answering if the retrieved context does not contain the answer.
   - Restricts output length to ≤ 3 sentences, matching the constraints in the problem statement.
5. **Render Free-Tier RAM Optimization:**
   - Avoids loading heavy language models into container RAM. Only the lightweight 384-dim MiniLM model runs in memory (~90 MB RAM), and LLM text generation is offloaded via Groq API, easily remaining under Render's 512 MB memory threshold.
