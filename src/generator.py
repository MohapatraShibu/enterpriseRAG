# generate grounded answers via Ollama (local LLM)
import ollama

MODEL = "llama3"

def generate(query: str, chunks: list[dict]) -> dict:
    # return answer dict with response text and citations
    if not chunks:
        return {
            "answer": "No accessible documents found for your query based on your role permissions.",
            "citations": [],
            "avg_confidence": 0.0,
        }

    context_parts = []
    for i, c in enumerate(chunks, 1):
        context_parts.append(f"[{i}] Source: {c['source']} (confidence: {c['confidence']})\n{c['text']}")
    context = "\n\n".join(context_parts)

    prompt = f"""You are an enterprise AI assistant. Answer the user's question using ONLY the provided context.
- Be factual and concise.
- If the answer is not in the context, say "I don't have enough information in the accessible documents."
- At the end, list the sources you used as citations like: Sources: [1], [2]

Context:
{context}

Question: {query}

Answer:"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1},
    )
    answer_text = response.message.content

    citations = [{"index": i + 1, "source": c["source"], "confidence": c["confidence"]}
                 for i, c in enumerate(chunks)]
    avg_conf = round(sum(c["confidence"] for c in chunks) / len(chunks), 3)

    return {"answer": answer_text, "citations": citations, "avg_confidence": avg_conf}
