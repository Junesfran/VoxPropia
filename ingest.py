import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# CONFIG
DATA_PATH = "data"

modelo = SentenceTransformer("all-MiniLM-L6-v2")

def leer_txt(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

def dividir_texto(texto, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(texto):
        end = start + chunk_size
        chunk = texto[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def main():
    todos_chunks = []

    for archivo in os.listdir(DATA_PATH):
        if archivo.endswith(".txt"):
            ruta = os.path.join(DATA_PATH, archivo)
            print(f"Procesando: {archivo}")

            texto = leer_txt(ruta)
            chunks = dividir_texto(texto)

            for chunk in chunks:
                todos_chunks.append({
                    "texto": chunk,
                    "fuente": archivo
                })

    textos = [c["texto"] for c in todos_chunks]
    embeddings = modelo.encode(textos)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, "index.faiss")

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=2)

    print("✅ Ingesta completada")

if __name__ == "__main__":
    main()