from __future__ import annotations

from .extraction import extract_reference_documents, extract_requests
from .generate_documents import generate_sample_pdfs
from .retrieval import match_requests_to_reference_docs


def run_pipeline() -> dict[str, int]:
    generated = generate_sample_pdfs()
    requests_df = extract_requests()
    refs_df = extract_reference_documents()
    matches_df = match_requests_to_reference_docs(requests_df, refs_df)
    return {
        "request_documents": generated["requests"],
        "reference_documents": generated["reference_docs"],
        "requests_extracted": len(requests_df),
        "reference_matches": len(matches_df),
    }

