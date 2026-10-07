"""Exercise 4: minimal RAG over a folder of .md files.
Setup: pip install anthropic sentence-transformers numpy python-dotenv
Run:   python exercises/04_mini_rag.py ./docs "What is X?"
(Anthropic has no embeddings endpoint, so we embed locally with sentence-transformers.)
TODO: try chunk sizes, add citations, swap numpy for Chroma, add "I don't know" evals.
"""
import sys
from pathlib import Path
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import anthropic

load_dotenv()
embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = anthropic.Anthropic()


def chunk(text: str, size: int = 500, overlap: int = 50):
    step = size - overlap
    return [text[i : i + size] for i in range(0, max(len(text), 1), step)]


def build_index(folder: str):
    chunks, sources = [], []
    for p in Path(folder).glob("**/*.md"):
        for c in chunk(p.read_text()):
            chunks.append(c)
            sources.append(p.name)
    vecs = embedder.encode(chunks, normalize_embeddings=True)
    return chunks, sources, vecs


def answer(question: str, chunks, sources, vecs, k: int = 4) -> str:
    q = embedder.encode([question], normalize_embeddings=True)[0]
    top = np.argsort(vecs @ q)[::-1][:k]  # cosine similarity (vectors are normalized)
    context = "\n\n".join(f"[{sources[i]}] {chunks[i]}" for i in top)
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=600,
        system="Answer ONLY from the provided context and cite sources like [file.md]. "
        "If the answer is not in the context, say you don't know.",
        messages=[{"role": "user", "content": f"<context>\n{context}\n</context>\n\nQuestion: {question}"}],
    )
    return msg.content[0].text


if __name__ == "__main__":
    folder, question = sys.argv[1], sys.argv[2]
    print(answer(question, *build_index(folder)))
