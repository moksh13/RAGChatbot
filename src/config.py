import os
from pathlib import Path

# Base Paths
SRC_DIR = Path(__file__).resolve().parent
BASE_DIR = SRC_DIR.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CHUNKS_DIR = DATA_DIR / "chunks"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"
DOCS_DIR = BASE_DIR / "docs"
CHUNKS_FILE_PATH = CHUNKS_DIR / "chunks.txt"
ROOT_CHUNKS_FILE_PATH = BASE_DIR / "chunks.txt"

# Load environment variables from .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# LLM Configuration (Current production models on GroqCloud: qwen/qwen3.8-27b, openai/gpt-oss-120b, openai/gpt-oss-20b)
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
LLM_TEMPERATURE = 0.0
MAX_RESPONSE_SENTENCES = 3

# Embedding Configuration
LOCAL_MODEL_DIR = BASE_DIR / "models" / "all-MiniLM-L6-v2"
if LOCAL_MODEL_DIR.exists():
    EMBEDDING_MODEL_NAME = str(LOCAL_MODEL_DIR)
else:
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Vector DB Configuration
CHROMA_COLLECTION_NAME = "hdfc_mutual_funds"
TOP_K_RESULTS = 4

# Conversation Memory Configuration
MEMORY_WINDOW_SIZE = 10

# Chunking Strategy Configuration
CHUNK_SIZE = 450
CHUNK_OVERLAP = 50

# Standard Compliance Disclaimers
STANDARD_DISCLAIMER = "Facts-only. No investment advice."
OFFICIAL_PORTAL_URL = "https://www.hdfcfund.com"
ADVICE_REFUSAL_MESSAGE = (
    "I provide factual information only and do not give investment advice, buy/sell recommendations, "
    "or portfolio suggestions. Please consult a SEBI-registered financial advisor or refer to the official factsheet."
)
PII_REFUSAL_MESSAGE = (
    "For your privacy and security, please do not share personal details such as PAN, Aadhaar, folio numbers, "
    "email addresses, or phone numbers. I cannot access or manage personal investor accounts."
)
OFF_TOPIC_REFUSAL_MESSAGE = (
    "I am a facts-only assistant scoped to 5 HDFC mutual fund schemes and statement download guides. "
    "I cannot answer questions outside this topic."
)
UNKNOWN_CONTEXT_MESSAGE = (
    "I don't know based on the provided official documents. The available documents do not contain information "
    "to answer this question. Please refer to the official scheme literature at https://www.hdfcfund.com."
)
DATA_UPDATE_TAG = "Last updated from sources: November 2026"
SIMILARITY_THRESHOLD = 0.25
