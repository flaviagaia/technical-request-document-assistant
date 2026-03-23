from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
REQUESTS_DIR = DATA_DIR / "requests"
REFERENCE_DOCS_DIR = DATA_DIR / "reference_docs"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

REQUESTS_PATH = ARTIFACTS_DIR / "technical_requests.csv"
REFERENCES_PATH = ARTIFACTS_DIR / "reference_documents.csv"
MATCHES_PATH = ARTIFACTS_DIR / "request_reference_matches.csv"

