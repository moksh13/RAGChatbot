"""RAG Engine and CLI for Mutual Fund Facts-Only Assistant.

Pipeline:
1. Conversation Memory & Query Rewriting:
   - Maintains the last 10 messages (sliding window).
   - Resolves follow-up pronouns (e.g. "what about its fees?" -> "What are the fees of HDFC Large Cap Fund?").
2. Input Guardrails: Detects PII, advice, return speculation, off-topic questions.
3. Question Embedding: Vectorizes the rewritten query using sentence-transformers/all-MiniLM-L6-v2 (same model as chunks).
4. ChromaDB Retrieval: Retrieves top-k matching chunks with cosine similarity.
5. Grounding Check: Validates retrieval score against similarity threshold.
6. Prompt Assembly: Packages strict rules, retrieved context passages, dialogue history, and query.
7. Generation: Calls Groq LLM (openai/gpt-oss-120b) at temperature 0.0.
8. History Update: Stores user question and assistant answer in conversation memory.
"""

import sys
import re
from typing import Any, Dict, List, Optional

from src.config import TOP_K_RESULTS, MEMORY_WINDOW_SIZE
from src.vector_store import VectorStore
from src.guardrails import validate_user_query, validate_retrieved_context
from src.conversation_memory import ConversationMemory
from src.prompt_templates import (
    SYSTEM_PROMPT,
    QUERY_REWRITE_SYSTEM_PROMPT,
    build_user_prompt,
    build_rewrite_prompt,
)
from src.llm_client import GroqClient


class RAGEngine:
    """Orchestrates end-to-end facts-only retrieval augmented generation with conversation memory."""

    def __init__(self, top_k: int = TOP_K_RESULTS, memory_window: int = MEMORY_WINDOW_SIZE):
        self.top_k = top_k
        self.vector_store = VectorStore()
        self.llm_client = GroqClient()
        self.memory = ConversationMemory(max_messages=memory_window)

    def rewrite_query_if_needed(self, user_question: str) -> str:
        """Rewrites follow-up questions into standalone queries using conversation memory."""
        # If no previous messages exist, no rewriting needed
        if self.memory.is_empty():
            return user_question

        history_str = self.memory.format_history_for_prompt()
        rewrite_prompt = build_rewrite_prompt(user_question, history_str)

        try:
            rewritten = self.llm_client.generate(
                system_prompt=QUERY_REWRITE_SYSTEM_PROMPT,
                user_prompt=rewrite_prompt,
                max_tokens=250,
                temperature=0.0,
            )
            # Clean up response formatting
            cleaned = rewritten.strip().strip('"\'`')
            # If the model added preamble like 'Standalone query: ...', strip it
            cleaned = re.sub(r'^(?:Standalone (?:Search )?Query:\s*)', '', cleaned, flags=re.IGNORECASE).strip()

            if cleaned and len(cleaned) > 3:
                return cleaned

        except Exception as e:
            # Fall back to original user question if rewriting encounters an issue
            pass

        return user_question

    def query(self, user_question: str) -> Dict[str, Any]:
        """Executes the full RAG pipeline for a given user question."""
        cleaned_question = user_question.strip()

        # Step 1: Pre-Retrieval Guardrails on the raw question
        guardrail_result = validate_user_query(cleaned_question)
        if guardrail_result:
            return {
                "question": cleaned_question,
                "rewritten_question": cleaned_question,
                "answer": guardrail_result["response"],
                "source_url": guardrail_result["source_url"],
                "guardrail_triggered": True,
                "guardrail_type": guardrail_result["type"],
                "guardrail_reason": guardrail_result["reason"],
                "retrieved_chunks": [],
            }

        # Step 2: Follow-up Query Rewriting using Conversation Memory
        search_query = self.rewrite_query_if_needed(cleaned_question)

        # Re-check guardrails on rewritten query in case unresolved advice/PII emerged
        if search_query != cleaned_question:
            secondary_guardrail = validate_user_query(search_query)
            if secondary_guardrail:
                return {
                    "question": cleaned_question,
                    "rewritten_question": search_query,
                    "answer": secondary_guardrail["response"],
                    "source_url": secondary_guardrail["source_url"],
                    "guardrail_triggered": True,
                    "guardrail_type": secondary_guardrail["type"],
                    "guardrail_reason": secondary_guardrail["reason"],
                    "retrieved_chunks": [],
                }

        # Step 3: Vector Retrieval using identical embedding model on the search query
        retrieved_chunks = self.vector_store.query(search_query, k=self.top_k)

        # Step 4: Grounding / Similarity Validation ("I don't know" fallback)
        context_validation = validate_retrieved_context(search_query, retrieved_chunks)
        if context_validation:
            return {
                "question": cleaned_question,
                "rewritten_question": search_query,
                "answer": context_validation["response"],
                "source_url": context_validation["source_url"],
                "guardrail_triggered": True,
                "guardrail_type": context_validation["type"],
                "guardrail_reason": context_validation["reason"],
                "retrieved_chunks": retrieved_chunks,
            }

        # Step 5: Prompt Construction with context and recent conversation history
        history_str = self.memory.format_history_for_prompt()
        user_prompt = build_user_prompt(
            query=cleaned_question,
            retrieved_chunks=retrieved_chunks,
            conversation_history=history_str,
        )

        # Step 6: Groq LLM Inference
        raw_answer = self.llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=1000,
        )

        # Extract primary citation URL from top chunk
        primary_source_url = (
            retrieved_chunks[0]["metadata"].get("source_url", "https://www.hdfcfund.com")
            if retrieved_chunks
            else "https://www.hdfcfund.com"
        )

        # Step 7: Update Conversation Memory
        self.memory.add_user_message(cleaned_question)
        self.memory.add_assistant_message(raw_answer)

        return {
            "question": cleaned_question,
            "rewritten_question": search_query,
            "answer": raw_answer,
            "source_url": primary_source_url,
            "guardrail_triggered": False,
            "guardrail_type": None,
            "guardrail_reason": None,
            "retrieved_chunks": retrieved_chunks,
        }

    def clear_memory(self) -> None:
        """Resets the conversation history."""
        self.memory.clear()


def format_cli_output(result: Dict[str, Any]) -> str:
    """Formats the query result and retrieved chunks for readable CLI display."""
    lines: List[str] = [
        "\n" + "=" * 80,
        f"QUESTION: {result['question']}",
    ]

    # Show rewritten query if anaphora resolution occurred
    if result.get("rewritten_question") and result["rewritten_question"] != result["question"]:
        lines.append(f"REWRITTEN STANDALONE QUERY: {result['rewritten_question']}")

    lines.append("=" * 80)

    # Display Guardrail notification if triggered
    if result["guardrail_triggered"]:
        lines.append(f"[GUARDRAIL ACTIVATED: {result['guardrail_type']}]")
        lines.append(f"Reason: {result['guardrail_reason']}")
        lines.append("-" * 80)

    # Display Retrieved Chunks
    chunks = result.get("retrieved_chunks", [])
    if chunks:
        lines.append(f"RETRIEVED CONTEXT CHUNKS ({len(chunks)} Chunks):")
        for i, c in enumerate(chunks, start=1):
            meta = c.get("metadata", {})
            sim = c.get("similarity", 0.0)
            chunk_id = meta.get("chunk_id", "N/A")
            scheme = meta.get("scheme_name", "N/A")
            section = meta.get("section_title", "N/A")
            lines.append(
                f"  [{i}] ID: {chunk_id} | Similarity: {sim:.2%} | Scheme: {scheme} | Section: {section}"
            )
            lines.append(f"      Snippet: {c['content'][:110]}...")
        lines.append("-" * 80)
    else:
        lines.append("RETRIEVED CONTEXT CHUNKS: None (Direct Guardrail Refusal)")
        lines.append("-" * 80)

    # Display Final Answer
    lines.append("ASSISTANT ANSWER:")
    lines.append(result["answer"])
    lines.append(f"Citation Source: {result['source_url']}")
    lines.append("=" * 80 + "\n")

    return "\n".join(lines)


def run_interactive_cli():
    """Runs interactive terminal loop for testing user questions."""
    print("=" * 80)
    print("MUTUAL FUND FACTS-ONLY RAG ASSISTANT (CLI TEST CONSOLE)")
    print("Model: Groq Cloud LLM | Embeddings: sentence-transformers/all-MiniLM-L6-v2")
    print(f"Conversation Memory: Active (Sliding window of last {MEMORY_WINDOW_SIZE} messages)")
    print("Commands: type 'clear' to reset memory, 'exit' to quit.")
    print("Disclaimer: Facts-only. No investment advice.")
    print("=" * 80)

    engine = RAGEngine()

    while True:
        try:
            user_input = input("\nEnter Question: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting RAG CLI. Goodbye!")
                break
            if user_input.lower() in ["clear", "reset"]:
                engine.clear_memory()
                print("Conversation memory cleared successfully.")
                continue

            result = engine.query(user_input)
            print(format_cli_output(result))

        except (KeyboardInterrupt, EOFError):
            print("\nExiting RAG CLI. Goodbye!")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query_text = " ".join(sys.argv[1:])
        engine = RAGEngine()
        output = engine.query(query_text)
        print(format_cli_output(output))
    else:
        run_interactive_cli()
