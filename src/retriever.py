# semantic retrieval with RBAC filtering
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from src.rbac import can_access

CHROMA_PATH = "chroma_db"
COLLECTION  = "enterprise_rag"

emb_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def retrieve(query: str, role: str, top_k: int = 6) -> list[dict]:
    # return top_k chunks the role is authorised to see
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    col = client.get_or_create_collection(COLLECTION, embedding_function=emb_fn)
    results = col.query(query_texts=[query], n_results=min(top_k * 3, col.count() or 1))

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    allowed = []
    for doc, meta, dist in zip(docs, metadatas, distances):
        if can_access(role, meta["source"]):
            confidence = round(1 - dist / 2, 3)   # cosine distance → 0-1 score
            allowed.append({
                "text": doc,
                "source": meta["source"],
                "type": meta["type"],
                "confidence": max(0.0, confidence),
            })
        if len(allowed) == top_k:
            break

    return allowed
