from __future__ import annotations

import pandas as pd
import streamlit as st

from src.config import MATCHES_PATH, REFERENCES_PATH, REQUESTS_PATH
from src.pipeline import run_pipeline
from src.retrieval import answer_request_question


st.set_page_config(page_title="Technical Request Document Assistant", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(14, 165, 233, 0.16), transparent 30%),
            radial-gradient(circle at top right, rgba(59, 130, 246, 0.14), transparent 28%),
            #06080d;
        color: #e5eefb;
    }
    .hero-card {
        background: rgba(10, 14, 23, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 20px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 18px 40px rgba(2, 6, 23, 0.45);
    }
    .hero-card h1, .hero-card p {
        color: #f8fbff;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #f8fbff;
    }
    [data-testid="stTabs"] button {
        color: #d7e3f7;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #7dd3fc;
    }
    [data-testid="stSidebar"], .stAlert, .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
        color: #e5eefb;
    }
    .stDataFrame, [data-testid="stMarkdownContainer"], .stCaption {
        color: #dbe7f5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h1>Technical Request Document Assistant</h1>
        <p>Consulte solicitações técnicas, extraia campos estruturados e encontre documentos de referência relacionados em um único ambiente.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("Atualizar base de solicitações e referências", use_container_width=True):
    run_pipeline()

try:
    requests_df = pd.read_csv(REQUESTS_PATH)
    refs_df = pd.read_csv(REFERENCES_PATH)
    matches_df = pd.read_csv(MATCHES_PATH)
except FileNotFoundError:
    run_pipeline()
    requests_df = pd.read_csv(REQUESTS_PATH)
    refs_df = pd.read_csv(REFERENCES_PATH)
    matches_df = pd.read_csv(MATCHES_PATH)
    st.info("A base demo foi gerada automaticamente para facilitar o primeiro uso.")

m1, m2, m3 = st.columns(3)
m1.metric("Solicitações", len(requests_df))
m2.metric("Documentos de referência", len(refs_df))
m3.metric("Correspondências", len(matches_df))

tab_assistant, tab_requests, tab_matches, tab_details = st.tabs(
    ["Assistente", "Solicitações Técnicas", "Documentos Relacionados", "Detalhes Técnicos"]
)

with tab_assistant:
    st.subheader("Faça uma pergunta")
    st.caption("Exemplos: 'Qual é o conflito de prazo?' ou 'Quem faz a verificação de qualidade?'")
    question = st.text_input("Pergunta", value="Qual é o conflito de prazo?")
    if question.strip():
        result = answer_request_question(question, requests_df, refs_df, matches_df)
        st.write(result["answer"])
        if isinstance(result["evidence"], pd.DataFrame) and not result["evidence"].empty:
            st.markdown("**Evidências**")
            st.dataframe(result["evidence"], use_container_width=True, hide_index=True)

with tab_requests:
    st.subheader("Solicitações técnicas extraídas")
    selected_request = st.selectbox("Escolha uma solicitação", requests_df["request_id"].tolist())
    row = requests_df[requests_df["request_id"] == selected_request].iloc[0]
    left, right = st.columns(2)
    with left:
        st.markdown(f"**Assunto**")
        st.write(row["subject"])
        st.markdown("**Pergunta**")
        st.write(row["question"])
    with right:
        st.markdown("**Metadados**")
        st.write(f"Disciplina: {row['discipline']}")
        st.write(f"Solicitante: {row['requester']}")
        st.write(f"Data: {row['issue_date']}")
        st.write(f"Prioridade: {row['priority']}")
        st.write(f"Referências declaradas: {row['referenced_documents']}")

with tab_matches:
    st.subheader("Documentos de referência mais relacionados")
    selected_request_for_matches = st.selectbox("Filtrar por solicitação", requests_df["request_id"].tolist(), key="match_request")
    view = matches_df[matches_df["request_id"] == selected_request_for_matches].copy()
    for match in view.itertuples():
        with st.container(border=True):
            st.markdown(f"**{match.reference_document}**")
            st.caption(f"Similaridade: {match.similarity:.3f} | Ranking: {match.rank}")
            st.write(match.snippet)

with tab_details:
    st.subheader("Camada técnica")
    st.markdown("**Solicitações extraídas**")
    st.dataframe(requests_df, use_container_width=True, hide_index=True)
    st.markdown("**Base de referência**")
    st.dataframe(refs_df, use_container_width=True, hide_index=True)
    st.markdown("**Correspondências request -> reference**")
    st.dataframe(matches_df, use_container_width=True, hide_index=True)
