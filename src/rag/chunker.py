from typing import List


def chunk_documents(
    documents: List[str],
    chunk_size: int = 300,
    overlap: int = 50,
) -> List[str]:
    """
    Split documents into overlapping chunks.
    """

    chunks = []

    for document in documents:

        start = 0

        while start < len(document):

            end = start + chunk_size

            chunks.append(document[start:end])

            start += chunk_size - overlap

    return chunks