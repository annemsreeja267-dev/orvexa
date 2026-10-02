# Enterprise Knowledge Assistant (Role-Aware RAG)

A local-first enterprise document assistant that implements secure Retrieval-Augmented Generation (RAG) with role-based access control (RBAC), metadata-aware retrieval, and source-grounded responses.

---

## Overview

This project delivers an end-to-end RAG pipeline for querying enterprise documents in a secure and structured manner. Documents are organized by domain and sensitivity level, enabling controlled access and realistic enterprise knowledge retrieval.

Key capabilities:

* Recursive ingestion of domain-structured documents
* Metadata-aware chunking with source and page tracking
* Persistent vector storage using ChromaDB
* Role-based retrieval filtering (RBAC enforcement)
* Local LLM-based answer generation via Ollama
* FastAPI backend for authenticated querying
* Streamlit frontend for interactive user access
* Source attribution for explainable responses

---

## Architecture

```
Documents (data/WorldBank/domain/classification)
        ↓
Ingestion & Metadata Extraction
        ↓
Text Chunking
        ↓
Embedding Generation (Sentence Transformers)
        ↓
Vector Storage (ChromaDB)
        ↓
User Authentication (FastAPI)
        ↓
Role-Based Retrieval Filtering
        ↓
Semantic Search
        ↓
LLM Response Generation (Ollama)
        ↓
Answer with Source Citations
```

---

## Project Structure

```
.
├── api/
│   └── main.py                    # FastAPI application (auth + query endpoints)
├── data/
│   ├── users.json                # User credentials and roles
│   └── WorldBank/
│       ├── govt_policy/
│       │   ├── public/
│       │   ├── internal/
│       │   └── confidential/
│       ├── hr1/
│       │   ├── public/
│       │   ├── internal/
│       │   └── confidential/
│       ├── procurement_operations/
│       │   ├── public/
│       │   ├── internal/
│       │   └── confidential/
│       └── finance_budget/
│           ├── public/
│           ├── internal/
│           └── confidential/
├── scripts/
│   ├── scan_documents.py
│   ├── show_registry_changes.py
│   └── test_pipeline.py
├── src/
│   ├── auth/
│   │   └── auth_service.py
│   ├── config/
│   │   └── settings.py
│   ├── embeddings/
│   │   └── embedder.py
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   └── document_registry.py
│   ├── llm/
│   │   └── llm_client.py
│   ├── pipeline/
│   │   └── rag_pipeline.py
│   ├── processing/
│   │   └── text_splitter.py
│   ├── retrieval/
│   │   └── retriever.py
│   └── vectorstore/
│       └── chroma_store.py
├── tests/
│   ├── test_rag_pipeline.py
│   └── test_text_splitter.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Dataset Organization

```
data/WorldBank/<domain>/<classification>/<file>
```

Domains:

* govt_policy
* hr1
* procurement_operations
* finance_budget

Classifications:

* public
* internal
* confidential

This structure enables automatic metadata extraction for secure retrieval.

---

## Access Model

| Role     | Access Scope                                                 |
| -------- | ------------------------------------------------------------ |
| Admin    | Full access to all domains and classifications               |
| Employee | Public documents + internal documents within assigned domain |
| Client   | Public documents only                                        |

Access control is enforced during retrieval prior to LLM invocation.

---

## Technology Stack

* Backend API: FastAPI
* Frontend UI: Streamlit
* Embeddings: Sentence Transformers
* Vector Database: ChromaDB
* LLM Runtime: Ollama (qwen2.5:7b, llama3)
* PDF Processing: pdfplumber
* DOCX Processing: python-docx

---

## Setup and Execution

### Install Dependencies

```
pip install -r requirements.txt
```

### Start Ollama

```
ollama serve
ollama pull qwen2.5:7b
```

### Run Backend (FastAPI)

```
PYTHONPATH=. python -m uvicorn api.main:app --reload
```

### Run Frontend (Streamlit)

```
PYTHONPATH=. streamlit run streamlit_app.py
```

### Access Application

```
http://localhost:8501
```

---

## API Endpoints

### Health Check

```
GET /health
```

### User Authentication

```
POST /login
```

### Query Endpoint

```
POST /query
```

Example Request:

```
{
  "username": "admin1",
  "password": "admin123",
  "question": "What is the code of ethics?"
}
```

---

## Retrieval Workflow

```
User → Authentication → Role Validation → Metadata Filtering
→ Vector Search → Context Retrieval → LLM Generation → Response + Sources
```

---

## Testing

```
python -m unittest tests.test_rag_pipeline
python -m unittest tests.test_text_splitter
```

---

## Limitations

* Initial query latency due to system warm-up
* Basic authentication using JSON-based user store
* Limited vector update/delete lifecycle
* Retrieval noise in ambiguous or poorly structured queries

---

## Future Enhancements

* Query rewriting and semantic reranking
* Token-based authentication and session management
* Incremental indexing and vector synchronization
* Improved UI with source visualization
* Deployment-ready containerization
* Multi-model implementation for better reasoning,response time .

---

## Summary

This project demonstrates a secure, enterprise-oriented RAG system that integrates semantic retrieval, metadata-driven filtering, and role-based access control. It provides a strong foundation for building scalable and secure knowledge assistants in real-world organizational environments.