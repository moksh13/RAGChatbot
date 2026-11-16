"""Guardrails module for Mutual Fund Facts RAG assistant.

Enforces:
1. PII detection (PAN, Aadhaar, phone numbers, email, folio numbers).
2. Refusal of investment advice, recommendations, and portfolio opinions.
3. Refusal of return predictions or performance forecasting.
4. Refusal of off-topic questions outside mutual fund facts.
5. Grounding check: Returns "I don't know" when retrieved context doesn't answer the question.
"""

import re
from typing import Any, Dict, List, Optional
from src.config import (
    ADVICE_REFUSAL_MESSAGE,
    PII_REFUSAL_MESSAGE,
    OFF_TOPIC_REFUSAL_MESSAGE,
    UNKNOWN_CONTEXT_MESSAGE,
    OFFICIAL_PORTAL_URL,
    SIMILARITY_THRESHOLD,
)

# Regex Patterns for Sensitive Personally Identifiable Information (PII)
PAN_REGEX = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", re.IGNORECASE)
AADHAAR_REGEX = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
PHONE_REGEX = re.compile(r"(?:\+91[-\s]?|0)?[6-9]\d{9}\b")
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
FOLIO_REGEX = re.compile(r"\b(?:folio\s*(?:no|number)?\s*[:=-]?\s*\d{5,12})\b", re.IGNORECASE)

# Patterns for Opinion, Investment Advice & Portfolio Recommendations
ADVICE_PATTERNS = [
    r"\bshould\s+i\s+(?:invest|buy|sell|choose|switch|start|exit|redeem|hold|put\s+money)\b",
    r"\bis\s+it\s+(?:good|safe|better|advisable|worth|the\s+right\s+time)\s+to\s+(?:invest|buy|sell)\b",
    r"\bwhich\s+(?:(?:fund|scheme|one)\s+is\s+(?:the\s+)?|is\s+(?:the\s+)?)(?:best|better|good|ideal|profitable|safest|highest\s+yielding)\b",
    r"\b(?:recommend|suggest)\s+(?:me\s+)?(?:a\s+)?(?:fund|scheme|portfolio|investment)\b",
    r"\bwhere\s+should\s+i\s+(?:invest|put\s+my\s+money)\b",
    r"\bportfolio\s+(?:advice|review|recommendation|allocation|suggestion)\b",
    r"\bhow\s+should\s+i\s+(?:allocate|distribute)\s+my\s+(?:money|funds|savings)\b",
    r"\bwhich\s+(?:fund|scheme)\s+should\s+i\s+(?:pick|select|buy)\b",
    r"\bhelp\s+me\s+choose\s+(?:between|a\s+fund)\b",
    r"\b(?:best|top)\s+(?:mutual\s+fund|scheme|fund)\s+to\s+(?:invest|buy)\b",
]

# Patterns for Performance Claims & Return Speculation
PERFORMANCE_PATTERNS = [
    r"\bwill\s+(?:it|this\s+fund|the\s+fund|hdfc[a-z\s]*)\s+(?:give|generate|reach|beat|deliver|double)\b",
    r"\bpredict\s+(?:returns?|nav|performance|future|market)\b",
    r"\bhow\s+much\s+returns?\s+will\s+i\s+get\b",
    r"\bguaranteed\s+returns?\b",
    r"\bexpected\s+returns?\s+in\s+(?:202[4-9]|next\s+year|future)\b",
    r"\bwill\s+i\s+get\s+\d+%\s+returns?\b",
]

# Patterns for Other Mutual Fund AMCs Outside Scope
OTHER_AMC_PATTERNS = [
    r"\b(?:sbi|icici|axis|nippon|kotak|uti|mirae|tata|quant|parag\s+parikh|dsp|motilal|aditya\s+birla|franklin|bandhan)\s+(?:mutual\s+fund|fund|scheme|bluechip|small\s+cap|large\s+cap|flexi\s+cap|elss)\b",
    r"\b(?:sbi|icici|axis|nippon|kotak|uti|mirae|tata|quant|parag\s+parikh|dsp|motilal|aditya\s+birla|franklin|bandhan)\s+(?:equity|hybrid|advantage)\b",
]

# Patterns for Common Off-Topic Questions
OFF_TOPIC_PATTERNS = [
    r"\b(?:cricket|ipl|football|soccer|weather|recipe|cooking|dinner|pasta|pizza)\b",
    r"\b(?:movie|actor|actress|cinema|song|lyrics|poem|story|joke)\b",
    r"\b(?:president|prime\s+minister|election|politics|government\s+policy)\b",
    r"\bwrite\s+(?:a\s+|me\s+)?(?:python\s+)?(?:code|script|program|app|html|poem|essay|story)\b",
    r"\bcapital\s+of\s+[a-z\s]+\b",
    r"\bwho\s+won\s+the\s+[a-z\s]+\b",
]


def check_pii(text: str) -> Optional[Dict[str, Any]]:
    """Detects Indian PAN, Aadhaar, phone numbers, emails, and account/folio numbers."""
    if PAN_REGEX.search(text):
        return {
            "passed": False,
            "type": "PII",
            "reason": "PAN card number detected",
            "response": PII_REFUSAL_MESSAGE,
            "source_url": OFFICIAL_PORTAL_URL,
        }
    if AADHAAR_REGEX.search(text):
        return {
            "passed": False,
            "type": "PII",
            "reason": "Aadhaar number sequence detected",
            "response": PII_REFUSAL_MESSAGE,
            "source_url": OFFICIAL_PORTAL_URL,
        }
    if PHONE_REGEX.search(text):
        return {
            "passed": False,
            "type": "PII",
            "reason": "Phone number detected",
            "response": PII_REFUSAL_MESSAGE,
            "source_url": OFFICIAL_PORTAL_URL,
        }
    if EMAIL_REGEX.search(text):
        return {
            "passed": False,
            "type": "PII",
            "reason": "Email address detected",
            "response": PII_REFUSAL_MESSAGE,
            "source_url": OFFICIAL_PORTAL_URL,
        }
    if FOLIO_REGEX.search(text):
        return {
            "passed": False,
            "type": "PII",
            "reason": "Account or folio number detected",
            "response": PII_REFUSAL_MESSAGE,
            "source_url": OFFICIAL_PORTAL_URL,
        }
    return None


def check_investment_advice(text: str) -> Optional[Dict[str, Any]]:
    """Detects requests for investment advice, scheme recommendations, or portfolio decisions."""
    clean_text = text.lower().strip()
    for pattern in ADVICE_PATTERNS:
        if re.search(pattern, clean_text):
            return {
                "passed": False,
                "type": "ADVICE",
                "reason": "Investment advice or opinion requested",
                "response": f"{ADVICE_REFUSAL_MESSAGE} You can review official scheme factsheets at {OFFICIAL_PORTAL_URL}.",
                "source_url": OFFICIAL_PORTAL_URL,
            }
    return None


def check_performance_predictions(text: str) -> Optional[Dict[str, Any]]:
    """Detects requests to forecast or compute future returns and NAVs."""
    clean_text = text.lower().strip()
    for pattern in PERFORMANCE_PATTERNS:
        if re.search(pattern, clean_text):
            return {
                "passed": False,
                "type": "PERFORMANCE_CLAIM",
                "reason": "Future return prediction requested",
                "response": (
                    "I cannot predict or guarantee future mutual fund returns. Past performance does not guarantee future results. "
                    f"Please refer to the official factsheet at {OFFICIAL_PORTAL_URL} for historical facts."
                ),
                "source_url": OFFICIAL_PORTAL_URL,
            }
    return None


def check_other_amc(text: str) -> Optional[Dict[str, Any]]:
    """Detects inquiries regarding non-HDFC fund houses (e.g. SBI, ICICI, Axis)."""
    clean_text = text.lower().strip()
    for pattern in OTHER_AMC_PATTERNS:
        if re.search(pattern, clean_text):
            return {
                "passed": False,
                "type": "OUT_OF_SCOPE_AMC",
                "reason": "Query asks about an AMC outside the scoped 5 HDFC schemes",
                "response": (
                    "I am a facts-only assistant scoped exclusively to 5 designated HDFC Mutual Fund schemes and "
                    f"official statement guides. I do not have verified documents for other AMCs. Official HDFC portal: {OFFICIAL_PORTAL_URL}."
                ),
                "source_url": OFFICIAL_PORTAL_URL,
            }
    return None


def check_off_topic(text: str) -> Optional[Dict[str, Any]]:
    """Detects questions entirely outside the scope of mutual funds and scheme facts."""
    clean_text = text.lower().strip()
    for pattern in OFF_TOPIC_PATTERNS:
        if re.search(pattern, clean_text):
            return {
                "passed": False,
                "type": "OFF_TOPIC",
                "reason": "Question is outside mutual fund scope",
                "response": OFF_TOPIC_REFUSAL_MESSAGE,
                "source_url": OFFICIAL_PORTAL_URL,
            }
    return None


def validate_user_query(query: str) -> Optional[Dict[str, Any]]:
    """Runs all pre-retrieval guardrail checks.

    Returns:
        A refusal dict if any guardrail is violated, or None if the query is valid.
    """
    if not query or not query.strip():
        return {
            "passed": False,
            "type": "EMPTY_QUERY",
            "reason": "Query string is empty",
            "response": "Please enter a question about one of the 5 HDFC mutual fund schemes or statement guides.",
            "source_url": OFFICIAL_PORTAL_URL,
        }

    # Check 1: PII
    pii_violation = check_pii(query)
    if pii_violation:
        return pii_violation

    # Check 2: Investment Advice & Opinions
    advice_violation = check_investment_advice(query)
    if advice_violation:
        return advice_violation

    # Check 3: Performance Forecasting
    performance_violation = check_performance_predictions(query)
    if performance_violation:
        return performance_violation

    # Check 4: Out-of-scope AMCs
    amc_violation = check_other_amc(query)
    if amc_violation:
        return amc_violation

    # Check 5: Off-topic detection
    off_topic_violation = check_off_topic(query)
    if off_topic_violation:
        return off_topic_violation

    return None


def validate_retrieved_context(
    query: str,
    retrieved_chunks: List[Dict[str, Any]],
    similarity_threshold: float = SIMILARITY_THRESHOLD,
) -> Optional[Dict[str, Any]]:
    """Evaluates whether retrieved chunks contain sufficient context to answer the question.

    If similarity is below threshold or no chunks exist, returns a standardized 'I don't know' fallback.
    """
    if not retrieved_chunks:
        return {
            "passed": False,
            "type": "NO_CONTEXT",
            "reason": "No relevant documents found in knowledge base",
            "response": UNKNOWN_CONTEXT_MESSAGE,
            "source_url": OFFICIAL_PORTAL_URL,
        }

    best_chunk = retrieved_chunks[0]
    best_similarity = best_chunk.get("similarity", 0.0)

    # If the semantic similarity is too low, the question is likely unanswerable from the corpus
    if best_similarity < similarity_threshold:
        return {
            "passed": False,
            "type": "LOW_SIMILARITY",
            "reason": f"Best similarity score ({best_similarity:.3f}) below threshold ({similarity_threshold})",
            "response": UNKNOWN_CONTEXT_MESSAGE,
            "source_url": OFFICIAL_PORTAL_URL,
        }

    return None


if __name__ == "__main__":
    # Test suite for guardrails verification
    test_cases = [
        ("My PAN is ABCDE1234F, show my funds", "PII"),
        ("Call me at 9876543210 about ELSS", "PII"),
        ("Send statements to investor@example.com", "PII"),
        ("Should I invest in HDFC Small Cap or Flexi Cap?", "ADVICE"),
        ("Which is the best fund to buy right now?", "ADVICE"),
        ("Will HDFC Large Cap give 20% return next year?", "PERFORMANCE_CLAIM"),
        ("Who won the cricket match yesterday?", "OFF_TOPIC"),
        ("Write a python script to calculate compound interest", "OFF_TOPIC"),
        ("What is the exit load for HDFC Large Cap Fund?", None),
        ("What is the lock-in period for HDFC ELSS?", None),
        ("How to download capital gains statement?", None),
    ]

    print("Running Guardrails Verification Suite...\n" + "=" * 60)
    passed_all = True
    for q, expected in test_cases:
        res = validate_user_query(q)
        actual = res["type"] if res else None
        status = "PASSED" if actual == expected else "FAILED"
        if status == "FAILED":
            passed_all = False
        print(f"[{status}] Query: '{q}'\n  Expected: {expected} | Actual: {actual}")
        if res:
            print(f"  Refusal Response: {res['response'][:90]}...")
        print("-" * 60)

    # Test context check with mock empty or low similarity chunks
    low_sim_check = validate_retrieved_context("What is the CEO favorite color?", [{"similarity": 0.10, "content": "mock"}])
    print(f"\nLow similarity test result: {low_sim_check['type']} -> {low_sim_check['response']}")

    print("\nGuardrail test suite result:", "ALL TESTS PASSED" if passed_all else "SOME TESTS FAILED")
