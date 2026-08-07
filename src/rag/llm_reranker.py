class LLMReranker:

    def rank(self, query: str, docs: list[dict]) -> list[dict]:

        scored = []

        for doc in docs:

            text = doc["text"].lower()
            query_l = query.lower()

            score = 0

            # semantic alignment
            if any(word in text for word in query_l.split()):
                score += 2

            # policy strength signals
            if "high risk" in text:
                score += 3

            if "default" in text:
                score += 2

            if "income" in text and "income" in query_l:
                score += 3

            if "employment" in text and "employment" in query_l:
                score += 3

            doc["score"] = score
            scored.append(doc)

        return sorted(scored, key=lambda x: x["score"], reverse=True)