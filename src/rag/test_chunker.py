from src.rag.policy_loader import load_policies
from src.rag.chunker import chunk_documents

# Policy dosyalarını yükle
documents = load_policies()

print(f"\nToplam policy: {len(documents)}")

# Chunk oluştur
chunks = chunk_documents(documents)

print(f"Toplam chunk: {len(chunks)}\n")

# İlk 5 chunk'ı göster
for i, chunk in enumerate(chunks[:5], start=1):
    print("=" * 60)
    print(f"Chunk {i}")
    print("=" * 60)
    print(chunk)
    print()