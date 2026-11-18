"""Vector Store module using ChromaDB and SentenceTransformers.

Handles:
- Persistent vector storage on disk (data/chroma_db/).
- Local embedding generation via sentence-transformers/all-MiniLM-L6-v2 (384 dimensions).
- Adding chunks with full metadata (scheme_name, category, source_url, etc.).
- Cosine similarity search for top-k relevant chunks.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np

from src.config import (
    CHROMA_DB_DIR,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    TOP_K_RESULTS,
)


class VectorStore:
    """Encapsulates ChromaDB persistent storage and SentenceTransformers embeddings."""

    def __init__(
        self,
        persist_dir: Optional[Path] = None,
        collection_name: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        import chromadb
        from chromadb.config import Settings

        self.persist_dir = persist_dir or CHROMA_DB_DIR
        self.collection_name = collection_name or CHROMA_COLLECTION_NAME
        self.model_name = model_name or EMBEDDING_MODEL_NAME
        self._embedding_model = None

        # Ensure persistence directory exists
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        # Initialize persistent ChromaDB client with telemetry disabled to save memory
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def embedding_model(self):
        """Lazy-loads SentenceTransformer only when first needed to save startup RAM."""
        if self._embedding_model is None:
            import gc
            import torch
            from sentence_transformers import SentenceTransformer

            # Cap PyTorch threads to 1 to strictly stay within Render's 512MB RAM
            torch.set_num_threads(1)
            torch.set_num_interop_threads(1)

            self._embedding_model = SentenceTransformer(self.model_name, device="cpu")
            gc.collect()
        return self._embedding_model

    def reset(self) -> None:
        """Clears the collection to allow a fresh re-indexing of chunks."""
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generates 384-dimensional dense vectors for a list of texts."""
        import torch
        import gc
        with torch.inference_mode():
            embeddings = self.embedding_model.encode(
                texts,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True,
                batch_size=16,
            )
        result = embeddings.tolist()
        gc.collect()
        return result

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Embeds and upserts chunks with their metadata into ChromaDB."""
        if not chunks:
            return 0

        ids = [chunk["chunk_id"] for chunk in chunks]
        texts = [chunk["content"] for chunk in chunks]
        metadatas = [
            {
                "chunk_id": chunk["chunk_id"],
                "scheme_id": chunk.get("scheme_id", ""),
                "scheme_name": chunk["scheme_name"],
                "category": chunk["category"],
                "section_title": chunk.get("section_title", ""),
                "source_url": chunk["source_url"],
                "last_updated": chunk.get("last_updated", ""),
                "char_count": chunk.get("char_count", len(chunk["content"])),
            }
            for chunk in chunks
        ]

        # Generate embeddings locally
        embeddings = self.embed_texts(texts)

        # Upsert into ChromaDB
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

        return len(ids)

    def count(self) -> int:
        """Returns the total number of vectors in the collection."""
        return self.collection.count()

    def query(self, query_text: str, k: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
        """Queries the vector store for top-k matching chunks."""
        query_embedding = self.embed_texts([query_text])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        formatted_results: List[Dict[str, Any]] = []
        if not results or not results["documents"]:
            return formatted_results

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, dist in zip(docs, metas, distances):
            formatted_results.append({
                "content": doc,
                "metadata": meta,
                "distance": dist,
                # For cosine distance: similarity = 1 - distance
                "similarity": 1.0 - dist if dist is not None else 1.0,
            })

        import gc
        gc.collect()
        return formatted_results
