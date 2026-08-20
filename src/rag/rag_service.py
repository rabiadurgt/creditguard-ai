# src/rag/rag_service.py

from src.rag.embedder import Embedder
from src.rag.vector_store import FAISSStore
from src.rag.policy_loader import load_policies
from src.rag.query_enhancer import QueryEnhancer
from src.rag.llm_reranker import LLMReranker
from src.rag.reasoning import PolicyReasoningEngine


class RAGService:

    def __init__(self):

        # 1. core components
        self.embedder = Embedder()
        self.enhancer = QueryEnhancer()
        self.llm_reranker = LLMReranker()
        self.reasoning = PolicyReasoningEngine()

        # 2. load docs once
        self.documents = load_policies()
        self.chunks = self._prepare_chunks(self.documents)

        # 3. build index ONCE
        self.vector_store = self._build_index(self.chunks)


    # -------------------------
    # CHUNK PREPARATION
    # -------------------------
    def _prepare_chunks(self, documents):

        return [
            {
                "text": doc["text"],
                "metadata": {
                    "source": doc["source"]
                }
            }
            for doc in documents
        ]


    # -------------------------
    # INDEX BUILDING
    # -------------------------
    def _build_index(self, chunks):

        texts = [c["text"] for c in chunks]

        # batch embedding 
        embeddings = self.embedder.embed_batch(texts)

        dim = len(embeddings[0])

        store = FAISSStore(dim)

        store.add(
            embeddings=embeddings,
            texts=texts,
            metadata=[c["metadata"] for c in chunks]
        )

        return store


    # -------------------------
    # RETRIEVAL PIPELINE
    # -------------------------
    def retrieve(self, query: str, k: int = 3):

        # 1. query enhancement
        expanded_query = self.enhancer.expand(query)

        # 2. embedding
        query_embedding = self.embedder.embed(expanded_query)

        # 3. vector search
        results = self.vector_store.search(query_embedding, k=10)

        # 4. reranking
        reranked = self.llm_reranker.rank(query, results)

        top_k = reranked[:k]

        # 5. reasoning layer
        for doc in top_k:
            doc["reason"] = self.reasoning.explain(query, doc)

        return top_k


    # -------------------------
    # PUBLIC API
    # -------------------------
    def explain(self, query: str, k: int = 3):

        results = self.retrieve(query, k)

        return [
            {
                "policy": r["metadata"]["source"],
                "text": r["text"],
                "reason": r["reason"],
                "score": r.get("score", 0)
            }
            for r in results
        ]