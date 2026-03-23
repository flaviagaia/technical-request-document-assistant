from __future__ import annotations

import re

import pandas as pd
from pypdf import PdfReader

from .config import ARTIFACTS_DIR, REFERENCES_PATH, REFERENCE_DOCS_DIR, REQUESTS_DIR, REQUESTS_PATH


FIELD_PATTERNS = {
    "request_id": re.compile(r"Technical Request ID:\s*(.+)", re.IGNORECASE),
    "discipline": re.compile(r"Discipline:\s*(.+)", re.IGNORECASE),
    "requester": re.compile(r"Requester:\s*(.+)", re.IGNORECASE),
    "issue_date": re.compile(r"Issue Date:\s*(.+)", re.IGNORECASE),
    "priority": re.compile(r"Priority:\s*(.+)", re.IGNORECASE),
    "subject": re.compile(r"Subject:\s*(.+)", re.IGNORECASE),
    "question": re.compile(r"Question:\s*(.+)", re.IGNORECASE),
    "referenced_documents": re.compile(r"Referenced Documents:\s*(.+)", re.IGNORECASE),
}


def _read_pdf_text(path) -> str:
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def extract_requests() -> pd.DataFrame:
    rows = []
    for path in sorted(REQUESTS_DIR.glob("*.pdf")):
        text = _read_pdf_text(path)
        record = {"file_name": path.name, "raw_text": text}
        for field, pattern in FIELD_PATTERNS.items():
            match = pattern.search(text)
            record[field] = match.group(1).strip() if match else ""
        rows.append(record)

    df = pd.DataFrame(rows)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(REQUESTS_PATH, index=False)
    return df


def extract_reference_documents() -> pd.DataFrame:
    rows = []
    for path in sorted(REFERENCE_DOCS_DIR.glob("*.pdf")):
        text = _read_pdf_text(path)
        rows.append(
            {
                "file_name": path.name,
                "document_name": path.stem,
                "content": text,
            }
        )
    df = pd.DataFrame(rows)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(REFERENCES_PATH, index=False)
    return df

