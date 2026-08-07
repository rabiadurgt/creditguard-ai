import faiss
import numpy as np


class FAISSStore:

    def __init__(self, dim: int):

        self.index = faiss.IndexFlatL2(dim)

        # metadata store (production-grade)
        self.texts = []
        self.metadata = []

    def add(self, embeddings, texts, metadata=None):
        """
        embeddings: list[np.array]
        texts: list[str]
        metadata: list[dict]
        """

        embeddings = np.array(embeddings).astype("float32")

        self.index.add(embeddings)

        self.texts.extend(texts)

        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in texts])

    def search(self, query_embedding, k=3):

        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        results = []

        for i in indices[0]:
            results.append({
                "text": self.texts[i],
                "metadata": self.metadata[i]
            })

        return results