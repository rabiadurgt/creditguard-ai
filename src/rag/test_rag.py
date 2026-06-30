from src.rag.rag_service import RAGService

# 1. RAG system'i başlat
rag = RAGService()

# 2. Test query
query = """
high risk customer low income unstable employment multiple children
"""

# 3. Policy retrieval
results = rag.retrieve(query)

# 4. Sonuçlar
print("\n🔍 TOP MATCHING POLICIES:\n")

for i, r in enumerate(results):
    print(f"{i+1}. {r}")