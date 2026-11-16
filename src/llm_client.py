"""LLM client wrapper for Groq Cloud API.

Provides:
- Connection handling using GROQ_API_KEY.
- Temperature=0.0 for deterministic factual fidelity.
- Compatible token budget for reasoning and standard models.
- Graceful exception handling and retry guidance.
"""

from typing import Optional
from groq import Groq
from src.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    LLM_TEMPERATURE,
)


class GroqClient:
    """Wrapper around the official Groq client."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or GROQ_API_KEY
        self.model = model or GROQ_MODEL

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Please add your Groq API key to .env "
                "or set the GROQ_API_KEY environment variable."
            )

        self.client = Groq(api_key=self.api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 500,
        temperature: float = LLM_TEMPERATURE,
    ) -> str:
        """Calls Groq API to generate a chat completion."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            choice = response.choices[0]
            content = choice.message.content

            # Some reasoning models return text in message.content
            if content and content.strip():
                return content.strip()

            # Fallback if content was empty
            return "Unable to generate response from model."

        except Exception as e:
            return f"Error communicating with Groq API ({self.model}): {str(e)}"
