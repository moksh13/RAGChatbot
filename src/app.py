"""Streamlit Web Application for Mutual Fund Facts-Only RAG Assistant.

Features:
- Clean chat interface with conversation history.
- Pre-retrieval follow-up rewriting (anaphora resolution) using rolling memory.
- Collapsible "Retrieved Sources" expander under each assistant response.
- One-click sample prompt buttons for quick class demonstration.
- Sidebar with scheme scope inventory, tech stack info, and 'Clear Chat' button.
- Strict compliance disclaimers: 'Facts-only. No investment advice.'
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import streamlit as st

# Ensure repository root is on sys.path so 'src.*' imports work on cloud hosts like Render
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import (
    STANDARD_DISCLAIMER,
    DATA_UPDATE_TAG,
    GROQ_MODEL,
    EMBEDDING_MODEL_NAME,
    CHROMA_COLLECTION_NAME,
)
from src.rag_engine import RAGEngine

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="HDFC Mutual Fund Facts Assistant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner="Initializing Vector DB and Embedding Model...")
def get_rag_engine() -> RAGEngine:
    """Caches the RAG engine instance so it initializes only once on server startup."""
    import gc
    from src.vector_store import VectorStore

    # Self-healing: Check if ChromaDB is populated BEFORE creating the active engine
    vs_check = VectorStore()
    if vs_check.count() == 0:
        from src.ingest import run_ingestion
        run_ingestion()
    del vs_check
    gc.collect()

    rag_engine = RAGEngine()
    # Pre-warm embedding model while showing the initial loading spinner
    try:
        _ = rag_engine.vector_store.embedding_model
    except Exception as e:
        print(f"Warning during model pre-warm: {e}")
    gc.collect()
    return rag_engine


# Initialize Engine and Session State
engine = get_rag_engine()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Navigation and Configuration
with st.sidebar:
    st.title("⚙️ Controls & Scope")

    # Clear Chat Button
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        engine.clear_memory()
        st.rerun()

    st.markdown("---")
    st.subheader("📚 Corpus Scope (HDFC AMC)")
    st.markdown("""
    This assistant is strictly bounded to 5 public schemes and official statement guides:
    - [HDFC Large Cap Fund](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth)
    - [HDFC Flexi Cap Fund](https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth)
    - [HDFC ELSS Tax Saver Fund](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth)
    - [HDFC Small Cap Fund](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth)
    - [HDFC Balanced Advantage Fund](https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth)
    - [HDFC Investor Statements Portal](https://www.hdfcfund.com/investor-services/statements)
    """)

    st.markdown("---")
    st.subheader("🛠️ Tech Stack & Constraints")
    st.caption(f"**LLM:** Groq Cloud (`{GROQ_MODEL}`)")
    st.caption(f"**Embeddings:** `{EMBEDDING_MODEL_NAME}` (384-dim, local CPU)")
    st.caption(f"**Vector DB:** ChromaDB (`{CHROMA_COLLECTION_NAME}`)")
    st.caption(f"**Memory:** Rolling window (last 10 messages)")
    st.caption("**Deployment:** Free-tier local / Render ready")

    st.markdown("---")
    st.warning(f"⚠️ **Disclaimer:** {STANDARD_DISCLAIMER}")

# Main Chat View Header
st.title("📈 HDFC Mutual Fund Facts-Only Assistant")
st.markdown(
    f"**Class Demonstration Prototype** — Answers factual queries using official public pages only. "
    f"*{STANDARD_DISCLAIMER}*"
)

# Quick-Start Example Buttons
st.markdown("##### 💡 Try an Example Question:")
col1, col2, col3 = st.columns(3)
sample_prompt = None

with col1:
    if st.button("📊 Large Cap: Expense & Exit Load", use_container_width=True):
        sample_prompt = "What is the expense ratio and exit load for HDFC Large Cap Fund Direct Growth?"

with col2:
    if st.button("🔒 ELSS: Lock-in Period", use_container_width=True):
        sample_prompt = "What is the lock-in period for HDFC ELSS Tax Saver Fund?"

with col3:
    if st.button("📑 Capital Gains Statement", use_container_width=True):
        sample_prompt = "How can I download my capital gains statement?"

st.divider()


def render_assistant_message(msg: Dict[str, Any]):
    """Renders assistant message with answer, citation, and collapsible sources expander."""
    st.markdown(msg["content"])

    # Show Sources & Retrieved Chunks Expander
    chunks = msg.get("retrieved_chunks", [])
    rewritten_q = msg.get("rewritten_question")
    original_q = msg.get("original_question")
    guardrail_flag = msg.get("guardrail_triggered", False)

    with st.expander("🔍 View Retrieved Sources & Chunks", expanded=False):
        if guardrail_flag:
            st.info(f"🛡️ **Guardrail Active:** {msg.get('guardrail_type')} — {msg.get('guardrail_reason')}")

        if rewritten_q and original_q and rewritten_q != original_q:
            st.markdown(f"**Contextual Query Rewrite:** `{rewritten_q}`")

        if chunks:
            st.markdown(f"**Retrieved {len(chunks)} Context Chunks from ChromaDB:**")
            for i, c in enumerate(chunks, start=1):
                meta = c.get("metadata", {})
                sim = c.get("similarity", 0.0)
                chunk_id = meta.get("chunk_id", "N/A")
                scheme = meta.get("scheme_name", "N/A")
                section = meta.get("section_title", "N/A")
                source_url = meta.get("source_url", "#")

                st.markdown(f"**Passage {i}** — `{chunk_id}` | Similarity: **{sim:.1%}**")
                st.caption(f"**Scheme:** {scheme} | **Section:** {section}")
                st.markdown(f"> *{c.get('content', '')}*")
                st.markdown(f"[Source Link]({source_url})")
                st.markdown("---")
        else:
            if not guardrail_flag:
                st.caption("No vector chunks retrieved.")


# Display Historical Conversation Messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            render_assistant_message(msg)


# Handle Query Input (from input box or clicked sample button)
user_query = st.chat_input("Ask a factual question (e.g. 'What is the exit load for HDFC Large Cap?')...")
active_query = sample_prompt or user_query

if active_query:
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(active_query)

    st.session_state.messages.append({
        "role": "user",
        "content": active_query,
    })

    # 2. Query RAG Engine with Spinner
    with st.chat_message("assistant"):
        with st.spinner("Searching official scheme documents..."):
            result = engine.query(active_query)

        # Assistant Message Payload
        assistant_payload = {
            "role": "assistant",
            "content": result["answer"],
            "source_url": result.get("source_url"),
            "original_question": active_query,
            "rewritten_question": result.get("rewritten_question"),
            "retrieved_chunks": result.get("retrieved_chunks", []),
            "guardrail_triggered": result.get("guardrail_triggered", False),
            "guardrail_type": result.get("guardrail_type"),
            "guardrail_reason": result.get("guardrail_reason"),
        }

        render_assistant_message(assistant_payload)
        st.session_state.messages.append(assistant_payload)
