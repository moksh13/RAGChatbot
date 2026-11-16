"""Prompt templates for Mutual Fund Facts RAG assistant.

Enforces:
- Strict facts-only answering using exclusively the provided context.
- Hard constraint: Maximum 3 sentences.
- Hard constraint: Exactly 1 official source citation link.
- Inclusion of the source freshness timestamp.
- Strict refusal to guess or hallucinate when facts are missing.
"""

from typing import Any, Dict, List
from src.config import (
    MAX_RESPONSE_SENTENCES,
    DATA_UPDATE_TAG,
    STANDARD_DISCLAIMER,
)

SYSTEM_PROMPT = f"""You are a mutual fund factual assistant for a class demonstration.
Your sole job is to answer factual questions about 5 specific HDFC mutual fund schemes and mutual fund statement download guides using ONLY the retrieved context provided.

CRITICAL RULES:
1. FACTS-ONLY: Use ONLY the provided context below. Do NOT use any external knowledge, assumptions, or extrapolations.
2. BREVITY: Keep your entire response to at most {MAX_RESPONSE_SENTENCES} sentences. Be clear, concise, and direct.
3. CITATION LINK: Every answer MUST include the official source URL matching the scheme or document discussed (provide 1 link, or 2 links if comparing two distinct schemes). Format as clean markdown link(s): [Official Scheme Page](URL).
4. FRESHNESS TAG: Every response must conclude with '{DATA_UPDATE_TAG}'.
5. NO INVESTMENT ADVICE: Never advise the user to buy, sell, hold, or choose any scheme. Never predict or promise returns.
6. MISSING INFORMATION / "I DON'T KNOW": If the answer cannot be found in the provided context, respond strictly with:
   "I don't know based on the provided official documents. The available documents do not contain information to answer this question. Please refer to official scheme documents at https://www.hdfcfund.com."
   Do NOT attempt to invent an answer or cite unverified facts.
"""


QUERY_REWRITE_SYSTEM_PROMPT = """You are a search query contextualizer for a mutual fund facts assistant.
Your task is to rewrite a user's follow-up question into a standalone, unambiguous search query using the recent conversation history.

Rules:
1. If the user's question contains pronouns (e.g., "its", "it", "that", "this", "their") or implicit references (e.g., "what about fees?", "and lock-in?", "how much is minimum SIP?"), resolve them to the specific scheme name or topic from the recent conversation.
2. If the user's question is already complete, standalone, or starts a new topic, return it unchanged.
3. Output ONLY the rewritten standalone question. Do NOT add any preamble, conversational fluff, explanations, or quotes.
4. Do NOT answer the question. Only rewrite it."""


def build_rewrite_prompt(query: str, history_str: str) -> str:
    """Builds user prompt for rewriting follow-up question."""
    return f"""Recent Conversation History:
{history_str}

Follow-up Question: {query}

Standalone Search Query:"""


def build_user_prompt(
    query: str,
    retrieved_chunks: List[Dict[str, Any]],
    conversation_history: str = "",
) -> str:
    """Constructs the prompt containing the retrieved context chunks, conversation history, and user's question."""
    context_blocks: List[str] = []

    for idx, chunk in enumerate(retrieved_chunks, start=1):
        scheme_name = chunk.get("metadata", {}).get("scheme_name", "Unknown Scheme")
        source_url = chunk.get("metadata", {}).get("source_url", "")
        content = chunk.get("content", "").strip()

        context_blocks.append(
            f"--- Context Passage {idx} ---\n"
            f"Scheme/Document: {scheme_name}\n"
            f"Source URL: {source_url}\n"
            f"Content: {content}"
        )

    context_str = "\n\n".join(context_blocks)

    history_section = ""
    if conversation_history.strip():
        history_section = f"\nRecent Conversation Context:\n{conversation_history.strip()}\n"

    return f"""Context from official documents:
{context_str}
{history_section}
User Question: {query}

Instructions:
Answer the question using ONLY the context above. Maximum {MAX_RESPONSE_SENTENCES} sentences. Include relevant official source link(s). End with '{DATA_UPDATE_TAG}'."""
