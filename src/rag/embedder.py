from sentence_transformers import SentenceTransformer
from typing import List


class Embedder:

    def __init__(self):

        # load once at init 
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    # -------------------------
    # SINGLE EMBEDDING
    # -------------------------
    def embed(self, text: str) -> List[float]:

        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()

    # -------------------------
    # BATCH EMBEDDING (IMPORTANT FIX)
    # -------------------------
    def embed_batch(self, texts: List[str]) -> List[List[float]]:

        return self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=False
        ).tolist()