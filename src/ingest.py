# ingest all data sources into ChromaDB with source metadata
import json, csv, sys
from pathlib import Path
from pypdf import PdfReader
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

CHROMA_PATH = "chroma_db"
COLLECTION = "enterprise_rag"
CHUNK_SIZE = 600
OVERLAP = 100

emb_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def get_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_collection(reset: bool = False):
    c = get_client()
    if reset:
        try:
            c.delete_collection(COLLECTION)
        except Exception:
            pass
    return c.get_or_create_collection(COLLECTION, embedding_function=emb_fn)

def chunk_text(text: str, source: str) -> list[dict]:
    words = text.split()
    chunks, i, idx = [], 0, 0
    while i < len(words):
        chunk = " ".join(words[i : i + CHUNK_SIZE])
        chunks.append({"text": chunk, "source": source, "chunk_id": idx})
        i += CHUNK_SIZE - OVERLAP
        idx += 1
    return chunks

def ingest_pdfs(col):
    for pdf_path in Path("data/pdfs").glob("*.pdf"):
        reader = PdfReader(str(pdf_path))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
        for c in chunk_text(text, pdf_path.name):
            col.add(
                ids=[f"{pdf_path.name}_{c['chunk_id']}"],
                documents=[c["text"]],
                metadatas=[{"source": c["source"], "type": "pdf"}],
            )
        print(f"  Ingested PDF: {pdf_path.name}")

def ingest_csvs(col):
    for csv_path in Path("data/csv").glob("*.csv"):
        rows = []
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(", ".join(f"{k}: {v}" for k, v in row.items()))
        text = f"File: {csv_path.name}\n" + "\n".join(rows)
        for c in chunk_text(text, csv_path.name):
            col.add(
                ids=[f"{csv_path.name}_{c['chunk_id']}"],
                documents=[c["text"]],
                metadatas=[{"source": c["source"], "type": "csv"}],
            )
        print(f"  Ingested CSV: {csv_path.name}")

def ingest_json_logs(col):
    for json_path in Path("data/json_logs").glob("*.json"):
        data = json.loads(json_path.read_text())
        if isinstance(data, list):
            text = f"File: {json_path.name}\n" + "\n".join(json.dumps(item) for item in data)
        else:
            text = f"File: {json_path.name}\n" + json.dumps(data, indent=2)
        for c in chunk_text(text, json_path.name):
            col.add(
                ids=[f"{json_path.name}_{c['chunk_id']}"],
                documents=[c["text"]],
                metadatas=[{"source": c["source"], "type": "json"}],
            )
        print(f"  Ingested JSON: {json_path.name}")

def run_ingestion():
    print("Starting ingestion (this may take a minute)...")
    col = get_collection(reset=True)
    ingest_pdfs(col)
    ingest_csvs(col)
    ingest_json_logs(col)
    print(f"\nIngestion complete. Total documents in store: {col.count()}")

if __name__ == "__main__":
    run_ingestion()
