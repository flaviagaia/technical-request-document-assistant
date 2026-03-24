# Technical Request Document Assistant

## PT-BR

Projeto em Python para reproduzir, de forma pública e segura, um fluxo integrado de leitura de solicitações técnicas, extração estruturada de informações e recuperação de documentos de referência.

### Objetivo

Simular um ambiente em que usuários consigam:

- consultar solicitações técnicas em um único front;
- extrair campos importantes de PDFs automaticamente;
- localizar documentos de referência relacionados;
- responder dúvidas operacionais a partir do conteúdo documental.

### Para que serve

Este projeto serve para apoiar usuários que lidam com solicitações técnicas e precisam entender rapidamente o contexto do pedido, os documentos relacionados e os principais pontos da dúvida. Ele ajuda a:

- transformar PDFs de solicitações em dados estruturados;
- encontrar documentos de referência mais relevantes para cada caso;
- responder perguntas operacionais de forma mais rápida;
- concentrar consulta e navegação documental em um único aplicativo.

### O que foi reproduzido

Esta versão pública reproduz o padrão técnico de uma solução corporativa sem usar nomes, documentos ou dados sensíveis. Em vez disso, ela usa:

- solicitações técnicas sintéticas em PDF;
- documentos de referência sintéticos;
- extração estruturada com regras;
- matching semântico com `TF-IDF`.

### Arquitetura

```mermaid
flowchart LR
    A["Synthetic technical requests (PDF)"] --> B["PDF ingestion"]
    C["Synthetic reference docs (PDF)"] --> D["Reference extraction"]
    B --> E["Structured request fields"]
    D --> F["Reference text base"]
    E --> G["Semantic matching"]
    F --> G
    G --> H["Integrated Streamlit assistant"]
```

### Técnicas usadas

- geração de PDFs sintéticos com `reportlab`
- leitura de PDFs com `pypdf`
- extração de campos com `regex`
- matching entre solicitações e referências com `TF-IDF + cosine similarity`
- consulta guiada em `Streamlit`

### Bibliotecas e frameworks

- `reportlab`
- `pypdf`
- `pandas`
- `scikit-learn`
- `streamlit`

### Estrutura

- [main.py](./main.py)
- [app.py](./app.py)
- [src/generate_documents.py](./src/generate_documents.py)
- [src/extraction.py](./src/extraction.py)
- [src/retrieval.py](./src/retrieval.py)

### Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
streamlit run app.py
```

Observação:
- se os artefatos ainda não existirem, o `Streamlit` gera automaticamente a base demo no primeiro acesso.

---

## EN

Python project designed to publicly and safely reproduce an integrated workflow for technical request ingestion, structured extraction, and reference document retrieval.

### Goal

The application allows users to:

- browse technical requests in a single front-end;
- extract important fields from PDFs automatically;
- retrieve related reference documents;
- answer operational questions from document content.

### What it is for

This project is designed to help users who handle technical requests and need to quickly understand the request context, the related reference documents, and the key operational question behind it. It helps users:

- transform request PDFs into structured data;
- find the most relevant supporting documents for each request;
- answer operational questions faster;
- centralize document consultation in a single application.

### What was reproduced

This public version mirrors the technical pattern of an enterprise solution without using any original names or sensitive content. Instead, it uses:

- synthetic technical request PDFs;
- synthetic reference PDFs;
- rule-based structured extraction;
- semantic matching with `TF-IDF`.

### Architecture

```mermaid
flowchart LR
    A["Synthetic technical requests (PDF)"] --> B["PDF ingestion"]
    C["Synthetic reference docs (PDF)"] --> D["Reference extraction"]
    B --> E["Structured request fields"]
    D --> F["Reference text base"]
    E --> G["Semantic matching"]
    F --> G
    G --> H["Integrated Streamlit assistant"]
```

### First run note

- if the processed artifacts do not exist yet, the `Streamlit` app automatically generates the demo dataset on first load.
