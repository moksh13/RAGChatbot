"""Conversation memory module for Mutual Fund Facts RAG Assistant.

Maintains a sliding window of the last N messages (default 10) to support:
- Multi-turn conversation tracking.
- Anaphora resolution and follow-up query rewriting.
- Context-aware dialogue history.
"""

from typing import Dict, List, Optional
from src.config import MEMORY_WINDOW_SIZE


class ConversationMemory:
    """Stores and manages sliding window of recent chat messages."""

    def __init__(self, max_messages: int = MEMORY_WINDOW_SIZE):
        self.max_messages = max_messages
        self.messages: List[Dict[str, str]] = []

    def add_user_message(self, content: str) -> None:
        """Appends a user message to the memory."""
        self.messages.append({"role": "user", "content": content.strip()})
        self._trim()

    def add_assistant_message(self, content: str) -> None:
        """Appends an assistant message to the memory."""
        self.messages.append({"role": "assistant", "content": content.strip()})
        self._trim()

    def get_messages(self) -> List[Dict[str, str]]:
        """Returns the current list of messages within the window limit."""
        return list(self.messages)

    def format_history_for_prompt(self) -> str:
        """Formats the conversation history as a readable string for prompts."""
        if not self.messages:
            return ""

        formatted_turns: List[str] = []
        for msg in self.messages:
            role_label = "User" if msg["role"] == "user" else "Assistant"
            formatted_turns.append(f"{role_label}: {msg['content']}")

        return "\n".join(formatted_turns)

    def is_empty(self) -> bool:
        """Returns True if there is no chat history."""
        return len(self.messages) == 0

    def clear(self) -> None:
        """Clears all conversation history."""
        self.messages.clear()

    def _trim(self) -> None:
        """Ensures the message history does not exceed max_messages."""
        if len(self.messages) > self.max_messages:
            # Keep only the most recent max_messages
            self.messages = self.messages[-self.max_messages:]
