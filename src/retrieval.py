from __future__ import annotations

import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import ARTIFACTS_DIR, MATCHES_PATH


def match_requests_to_reference_docs(requests_df: pd.DataFrame, refs_df: pd.DataFrame, top_k: int = 3) -> pd.DataFrame:
    query_texts = (requests_df["subject"].fillna("") + " " + requests_df["question"].fillna("")).tolist()
    ref_texts = refs_df["content"].fillna("").tolist()

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    ref_matrix = vectorizer.fit_transform(ref_texts)
    query_matrix = vectorizer.transform(query_texts)
    similarity = cosine_similarity(query_matrix, ref_matrix)

    rows = []
    for req_idx, request_row in requests_df.reset_index(drop=True).iterrows():
        ranked = similarity[req_idx].argsort()[::-1][:top_k]
        for rank, ref_idx in enumerate(ranked, start=1):
            ref_row = refs_df.iloc[ref_idx]
            rows.append(
                {
                    "request_id": request_row["request_id"],
                    "subject": request_row["subject"],
                    "reference_document": ref_row["document_name"],
                    "similarity": round(float(similarity[req_idx, ref_idx]), 4),
                    "rank": rank,
                    "snippet": ref_row["content"][:400],
                }
            )

    matches_df = pd.DataFrame(rows).sort_values(["request_id", "rank"]).reset_index(drop=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    matches_df.to_csv(MATCHES_PATH, index=False)
    return matches_df


def answer_request_question(question: str, requests_df: pd.DataFrame, refs_df: pd.DataFrame, matches_df: pd.DataFrame) -> dict[str, object]:
    normalized = question.lower().strip()
    if not normalized:
        return {"answer": "Digite uma pergunta para consultar as solicitações técnicas.", "evidence": pd.DataFrame()}

    if "prazo" in normalized or "deadline" in normalized:
        ev = matches_df[matches_df["subject"].str.contains("deadline|prazo|model revision", case=False, na=False)].head(5)
        return {
            "answer": "As solicitações técnicas indicam divergência de prazo para revisão do modelo 3D, com referências apontando 10 e 15 dias corridos.",
            "evidence": ev,
        }

    if "qualidade" in normalized or "quality" in normalized or "respons" in normalized:
        ev = matches_df[matches_df["subject"].str.contains("quality|verification|responsibility", case=False, na=False)].head(5)
        return {
            "answer": "A base indica dúvida sobre quem deve executar a verificação de qualidade antes do envio: contratada em um documento e cliente em outro.",
            "evidence": ev,
        }

    if "valve" in normalized or "padr" in normalized or "standard" in normalized:
        ev = matches_df[matches_df["subject"].str.contains("valve|standard", case=False, na=False)].head(5)
        return {
            "answer": "Há conflito de padrão técnico para identificação de válvulas, com referências para ENG-VAL-01 e ENG-VAL-02.",
            "evidence": ev,
        }

    escaped_terms = [re.escape(term) for term in normalized.split()[:3] if term]
    pattern = "|".join(escaped_terms)
    query_df = (
        requests_df[requests_df["question"].str.contains(pattern, case=False, na=False, regex=True)].head(5)
        if pattern
        else requests_df.head(0)
    )
    if query_df.empty:
        return {
            "answer": "Encontrei poucas evidências diretas. Revise os documentos relacionados abaixo.",
            "evidence": matches_df.head(5),
        }
    return {
        "answer": "Encontrei solicitações técnicas relacionadas ao tema consultado.",
        "evidence": query_df[["request_id", "subject", "discipline", "priority", "question"]],
    }
