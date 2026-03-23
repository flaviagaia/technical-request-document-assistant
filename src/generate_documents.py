from __future__ import annotations

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .config import REFERENCE_DOCS_DIR, REQUESTS_DIR


REQUEST_DOCUMENTS = {
    "TR_001_model_review.pdf": [
        "Technical Request ID: TR-001",
        "Discipline: Piping",
        "Requester: Ana Martins",
        "Issue Date: 2026-02-10",
        "Priority: High",
        "Subject: Clarification on 3D model revision deadline",
        "Question: Please confirm whether the 3D model review package must be delivered within 10 calendar days or 15 calendar days after kickoff.",
        "Referenced Documents: baseline_scope_contract, technical_memorial_rev_a",
    ],
    "TR_002_quality_owner.pdf": [
        "Technical Request ID: TR-002",
        "Discipline: Quality",
        "Requester: Bruno Lima",
        "Issue Date: 2026-02-12",
        "Priority: Medium",
        "Subject: Responsibility for quality verification before submission",
        "Question: We need to confirm whether quality verification before document submission is performed by the contractor or by the client.",
        "Referenced Documents: baseline_scope_contract, inspection_plan_rev_b",
    ],
    "TR_003_valve_standard.pdf": [
        "Technical Request ID: TR-003",
        "Discipline: Instrumentation",
        "Requester: Carla Souza",
        "Issue Date: 2026-02-14",
        "Priority: High",
        "Subject: Valve tagging standard conflict",
        "Question: There is a doubt regarding the correct valve tagging standard. Please clarify if ENG-VAL-01 or ENG-VAL-02 is the valid coding reference.",
        "Referenced Documents: technical_memorial_rev_a, inspection_plan_rev_b",
    ],
}

REFERENCE_DOCUMENTS = {
    "baseline_scope_contract.pdf": [
        "Document Name: baseline_scope_contract",
        "Section 1.1 - The contractor shall deliver the 3D model revision within 10 calendar days after kickoff.",
        "Section 1.2 - Quality verification shall be performed by the contractor before submission.",
        "Section 1.3 - Measurement shall be based on approved isometric sheets.",
    ],
    "technical_memorial_rev_a.pdf": [
        "Document Name: technical_memorial_rev_a",
        "Section 1.1 - The contractor shall deliver the 3D model revision within 15 calendar days after kickoff.",
        "Section 1.2 - Quality verification shall be performed by the contractor before submission.",
        "Section 2.1 - Valve tagging shall follow the project coding standard ENG-VAL-01.",
    ],
    "inspection_plan_rev_b.pdf": [
        "Document Name: inspection_plan_rev_b",
        "Section 1.2 - Quality verification shall be performed by the client before submission.",
        "Section 2.1 - Valve tagging shall follow the project coding standard ENG-VAL-02.",
        "Section 2.2 - Technical clarification requests shall be answered within 3 business days.",
    ],
    "execution_guideline.pdf": [
        "Document Name: execution_guideline",
        "Section 1.1 - The contractor shall deliver the 3D model revision within 10 calendar days after kickoff.",
        "Section 3.1 - The client shall review all submissions within 7 business days.",
        "Section 4.1 - Engineering interfaces shall be recorded in the coordination log.",
    ],
}


def _write_pdf(path, lines: list[str]) -> None:
    pdf = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    y = height - 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(45, y, path.stem.replace("_", " ").title())
    y -= 30
    pdf.setFont("Helvetica", 10)
    for line in lines:
        if y < 70:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)
        pdf.drawString(45, y, line)
        y -= 20
    pdf.save()


def generate_sample_pdfs() -> dict[str, int]:
    REQUESTS_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, lines in REQUEST_DOCUMENTS.items():
        _write_pdf(REQUESTS_DIR / filename, lines)

    for filename, lines in REFERENCE_DOCUMENTS.items():
        _write_pdf(REFERENCE_DOCS_DIR / filename, lines)

    return {"requests": len(REQUEST_DOCUMENTS), "reference_docs": len(REFERENCE_DOCUMENTS)}

