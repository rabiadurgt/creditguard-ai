# src/rag/rag_service.py

from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSStore
from src.rag.policy_loader import load_policies

class RAGService:

    def __init__(self):

        self.embedder = Embedder()

        self.policies = load_policies("data/policies/credit_policy.txt")

        embeddings = self.embedder.encode(self.policies)

        self.store = FAISSStore(dim=embeddings.shape[1])
        self.store.add(embeddings, self.policies)

    def retrieve(self, query: str):

        query_emb = self.embedder.encode([query])[0]

        return self.store.search(query_emb, k=3)