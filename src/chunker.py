"""Chunking module for Mutual Fund Facts RAG assistant.

Implements a Section-Aware Semantic Chunking Strategy tailored for financial facts:
- Groups cohesive scheme attributes together (Fees & Loads, Investment Terms & Lock-in,
  Riskometer & Benchmark, Taxation, and Statement Download Procedures).
- Preserves atomic facts (never splits numbers, percentages, or conditions mid-sentence).
- Attaches source URL, scheme name, category, and update timestamp metadata to each chunk.
- Emits formatted chunks to data/chunks/chunks.txt (numbered, with source & character count).
"""

from pathlib import Path
from typing import Any, Dict, List
from src.config import (
    CHUNKS_DIR,
    CHUNKS_FILE_PATH,
    ROOT_CHUNKS_FILE_PATH,
    DATA_UPDATE_TAG,
)
from src.data_loader import load_all_documents


class SchemeChunker:
    """Chunks mutual fund documents into dense, semantically coherent passages."""

    def __init__(self, target_chunk_size: int = 400, overlap: int = 50):
        self.target_chunk_size = target_chunk_size
        self.overlap = overlap

    def create_chunks_for_scheme(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Creates semantic chunks for a mutual fund scheme or statement guide."""
        scheme_id = doc["id"]
        scheme_name = doc["scheme_name"]
        category = doc["category"]
        source_url = doc["source_url"]
        last_updated = doc.get("last_updated", DATA_UPDATE_TAG)
        facts = doc["facts"]

        chunks: List[Dict[str, Any]] = []

        if scheme_id == "statement_guide":
            # Statement guide sections
            sections = [
                {
                    "title": "HDFC Mutual Fund Website Statement Download",
                    "content": (
                        f"How to Download Capital Gains Statement from HDFC Mutual Fund Portal: "
                        f"Visit official portal ({source_url}) -> Go to 'Investor Services' -> "
                        f"Click 'Statements & Certificates' -> Select 'Capital Gain Statement' -> "
                        f"Enter registered Folio Number or PAN -> Authenticate via OTP sent to registered mobile/email -> "
                        f"Select Financial Year -> Download statement as PDF or Excel. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "CAMS Portal Capital Gains & CAS Download",
                    "content": (
                        f"How to Download Capital Gains Statement and Consolidated Account Statement (CAS) via CAMS Portal: "
                        f"Go to CAMS Online (www.camsonline.com) -> 'Investor Services' -> 'Statements' -> "
                        f"'Capital Gains / Consolidated Account Statement (CAS)'. "
                        f"Provide registered email address and PAN, then select the financial year. "
                        f"A password-protected encrypted PDF is emailed to your registered address. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "Groww App Capital Gains Statement Download",
                    "content": (
                        f"How to Download Capital Gains Statement on Groww: "
                        f"Open the Groww application or website -> Click your Profile picture -> "
                        f"Navigate to 'Reports' section -> Select 'Capital Gains Statement' and choose 'Mutual Funds' -> "
                        f"Select the desired Financial Year -> Click 'Download PDF' or 'Send to Email'. "
                        f"The report categorizes Short Term and Long Term capital gains. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "Mutual Fund Statements Overview & Security",
                    "content": (
                        f"Consolidated Account Statement (CAS) and Capital Gains Statements Overview: "
                        f"CAS aggregates all mutual fund holdings across all fund houses (AMCs) linked to a single PAN. "
                        f"All tax statements segregate Short Term Capital Gains (STCG) and Long Term Capital Gains (LTCG) "
                        f"for income tax filing. Statements are password-encrypted using your PAN in uppercase or DOB. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
            ]
        else:
            # Scheme specific sections
            sections = [
                {
                    "title": "Expense Ratio, Exit Load & NAV",
                    "content": (
                        f"Scheme: {scheme_name} ({category}). "
                        f"Net Asset Value (NAV): {facts.get('nav', 'N/A')}. "
                        f"Expense Ratio: {facts.get('expense_ratio')}. "
                        f"Exit Load: {facts.get('exit_load')}. "
                        f"Stamp Duty: {facts.get('stamp_duty', '0.005%')}. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "Investment Minimums & Lock-in Period",
                    "content": (
                        f"Scheme: {scheme_name} ({category}). "
                        f"Minimum SIP Investment: {facts.get('min_sip_investment')}. "
                        f"Minimum Lumpsum Purchase: {facts.get('min_lumpsum_investment')}. "
                        f"Lock-in Period: {facts.get('lock_in_period')}. "
                        f"{'Tax deduction eligible up to ₹1.5 Lakh under Section 80C.' if 'ELSS' in scheme_name else ''} "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "Riskometer Rating & Benchmark",
                    "content": (
                        f"Scheme: {scheme_name} ({category}). "
                        f"Riskometer Classification: {facts.get('riskometer')}. "
                        f"Benchmark Index: {facts.get('benchmark')}. "
                        f"Category: {facts.get('fund_category')}. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "Capital Gains Taxation & Rules",
                    "content": (
                        f"Scheme: {scheme_name} ({category}). "
                        f"Taxation Details: {facts.get('taxation')}. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "Fund Administration, AUM & RTA",
                    "content": (
                        f"Scheme: {scheme_name} ({category}). "
                        f"Fund House: HDFC Mutual Fund. "
                        f"Fund Manager: {facts.get('fund_manager')}. "
                        f"Total AUM: {facts.get('aum')}. "
                        f"Inception Date: {facts.get('launch_date')}. "
                        f"Registrar (RTA): {facts.get('rta_details')}. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
                {
                    "title": "Net Asset Value (NAV) & Daily Pricing",
                    "content": (
                        f"Scheme: {scheme_name} ({category}). "
                        f"Net Asset Value (NAV): {facts.get('nav', 'N/A')}. "
                        f"NAV Details & Valuation: The Net Asset Value represents the per-unit market price of the fund. "
                        f"NAV fluctuates daily on business days based on market performance of underlying holdings and is published at the end of each trading day. "
                        f"Official source: {source_url}. {last_updated}."
                    ),
                },
            ]

        for idx, sec in enumerate(sections, start=1):
            chunk_content = sec["content"].strip()
            chunk_id = f"{scheme_id}_chunk_{idx:02d}"
            chunks.append({
                "chunk_id": chunk_id,
                "scheme_id": scheme_id,
                "scheme_name": scheme_name,
                "category": category,
                "section_title": sec["title"],
                "source_url": source_url,
                "last_updated": last_updated,
                "char_count": len(chunk_content),
                "content": chunk_content,
            })

        return chunks

    def chunk_all(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes all documents and outputs structured chunks."""
        all_chunks: List[Dict[str, Any]] = []
        for doc in docs:
            chunks = self.create_chunks_for_scheme(doc)
            all_chunks.extend(chunks)
        return all_chunks

    def export_chunks_to_file(self, chunks: List[Dict[str, Any]]) -> Path:
        """Writes all chunks in numbered, human-readable format with character count."""
        CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
        lines: List[str] = []

        total_chunks = len(chunks)
        lines.append("=" * 80)
        lines.append(f"MUTUAL FUND RAG CHUNKS AUDIT REPOSITORY ({total_chunks} TOTAL CHUNKS)")
        lines.append(f"Generated for: Class Demonstration & Inspection")
        lines.append("=" * 80)
        lines.append("")

        for i, chunk in enumerate(chunks, start=1):
            lines.append("-" * 80)
            lines.append(f"[Chunk {i} of {total_chunks}] | ID: {chunk['chunk_id']}")
            lines.append(f"Scheme: {chunk['scheme_name']}")
            lines.append(f"Category: {chunk['category']}")
            lines.append(f"Section: {chunk['section_title']}")
            lines.append(f"Source URL: {chunk['source_url']}")
            lines.append(f"Character Count: {chunk['char_count']} chars")
            lines.append("-" * 80)
            lines.append(chunk["content"])
            lines.append("")

        content_str = "\n".join(lines)

        # Write to data/chunks/chunks.txt
        with open(CHUNKS_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(content_str)

        # Also write to root chunks.txt for backwards-compatibility
        with open(ROOT_CHUNKS_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(content_str)

        return CHUNKS_FILE_PATH


def run_loading_and_chunking() -> List[Dict[str, Any]]:
    """Loads documents, splits into chunks, and saves inspection file."""
    docs = load_all_documents()
    chunker = SchemeChunker(target_chunk_size=400, overlap=50)
    chunks = chunker.chunk_all(docs)
    saved_path = chunker.export_chunks_to_file(chunks)
    return chunks


if __name__ == "__main__":
    chunks = run_loading_and_chunking()
    print(f"Total chunks created: {len(chunks)}")
    print(f"Inspection file written to: {CHUNKS_FILE_PATH}")
