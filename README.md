# Enterprise RAG Intelligence System

A secure, context-aware RAG system with RBAC enforcement over heterogeneous enterprise data.

## Stack (100% Free & Local)
| Component | Tool |
|---|---|
| LLM | [Ollama](https://ollama.com) — runs locally |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB (persistent, local) |
| PDF parsing | pypdf |
| UI | Streamlit |

---

## Setup

### 1. Install Ollama
Download from https://ollama.com and pull a model:
```bash
ollama pull llama3.2
```

### 2. Create & activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate synthetic data
```bash
python data/generate_data.py
```

### 5. Ingest data into vector store
```bash
python -m src.ingest
```

### 6. Run the app
```bash
streamlit run app.py
```

---

## Demo Users

| Username | Password | Role | Access |
|---|---|---|---|
| alice | alice123 | hr_manager | HR docs, employee records, compliance |
| bob | bob123 | finance_analyst | Finance reports, budget, compliance |
| carol | carol123 | it_admin | IT logs, audit trails, system reports |
| dave | dave123 | executive | All documents |
| eve | eve123 | intern | Public docs only |

---

## Architecture

```
User Query
    ↓
[RBAC Auth] ── role extracted
    ↓
[Retriever] ── semantic search in ChromaDB → filter by role permissions
    ↓
[Generator] ── Ollama LLM with grounded context prompt
    ↓
[Response] ── answer + citations + confidence scores + retrieval trace
```

## Key Features
- **RBAC**: each document tagged with required permissions; chunks filtered before LLM sees them
- **Citations**: every answer includes source filenames and confidence scores
- **Retrieval trace**: expandable view of exact chunks used
- **Hallucination minimisation**: LLM instructed to answer only from context
- **Multi-format**: PDFs, CSVs, JSON logs all ingested and searchable
