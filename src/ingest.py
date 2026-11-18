"""Ingestion script for Mutual Fund Facts RAG assistant.

Orchestrates:
1. Loading raw scheme facts and statement guide.
2. Chunking with Section-Aware Semantic Strategy.
3. Writing data/chunks/chunks.txt for transparency.
4. Embedding chunks locally using sentence-transformers/all-MiniLM-L6-v2 (384 dimensions).
5. Persisting vectors and metadata into local ChromaDB (data/chroma_db/).
6. Exporting a preview of the first 5 embeddings (first 10 dimensions each)
   to data/embeddings_preview.txt as required.
"""

from pathlib import Path
from typing import List, Dict, Any
from src.config import DATA_DIR, CHROMA_DB_DIR
from src.chunker import run_loading_and_chunking
from src.vector_store import VectorStore


def export_embeddings_preview(
    vector_store: VectorStore,
    chunks: List[Dict[str, Any]],
    output_path: Path,
    num_samples: int = 5,
    num_dims: int = 10,
) -> Path:
    """Writes a human-readable preview of the first N embeddings and their first K dimensions."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample_chunks = chunks[:num_samples]
    sample_texts = [c["content"] for c in sample_chunks]
    embeddings = vector_store.embed_texts(sample_texts)

    lines: List[str] = [
        "=" * 80,
        f"EMBEDDINGS PREVIEW (First {num_samples} Chunks, First {num_dims} Dimensions of 384)",
        f"Model: {vector_store.model_name}",
        f"Full Dimension: 384",
        "=" * 80,
        "",
    ]

    for idx, (chunk, emb) in enumerate(zip(sample_chunks, embeddings), start=1):
        truncated_vector = [round(val, 6) for val in emb[:num_dims]]
        lines.append(f"--- Chunk {idx}: {chunk['chunk_id']} ---")
        lines.append(f"Scheme: {chunk['scheme_name']}")
        lines.append(f"Section: {chunk['section_title']}")
        lines.append(f"Total Vector Dimensions: {len(emb)}")
        lines.append(f"First {num_dims} Dimensions:")
        lines.append(f"  {truncated_vector}")
        lines.append(f"Text Snippet: {chunk['content'][:120]}...")
        lines.append("")

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


def run_ingestion() -> int:
    """Executes the complete ingestion and embedding pipeline."""
    print("Step 1: Loading raw documents and generating chunks...")
    chunks = run_loading_and_chunking()
    print(f"Generated {len(chunks)} chunks.")

    print("\nStep 2: Initializing ChromaDB and local embedding model...")
    vs = VectorStore()
    vs.reset()

    print("\nStep 3: Generating embeddings and storing in persistent ChromaDB...")
    num_stored = vs.add_chunks(chunks)
    total_in_db = vs.count()
    print(f"Successfully embedded and stored {num_stored} vectors (Total in DB: {total_in_db}).")

    print("\nStep 4: Writing embeddings preview to data/embeddings_preview.txt...")
    preview_path = DATA_DIR / "embeddings_preview.txt"
    export_embeddings_preview(vs, chunks, preview_path, num_samples=5, num_dims=10)
    print(f"Embeddings preview saved to {preview_path}")

    import gc
    del vs
    gc.collect()

    return total_in_db


if __name__ == "__main__":
    count = run_ingestion()
    print(f"\nIngestion complete! Total vectors in persistent ChromaDB: {count}")
