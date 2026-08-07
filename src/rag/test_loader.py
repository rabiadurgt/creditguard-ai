from src.rag.policy_loader import load_policies

documents = load_policies()

print(f"\nToplam policy sayısı: {len(documents)}\n")

for i, doc in enumerate(documents, start=1):
    print(f"------ Policy {i} ------")
    print(doc[:200])   # İlk 200 karakteri göster
    print()