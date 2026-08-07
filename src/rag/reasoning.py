class PolicyReasoningEngine:

    def explain(self, query: str, doc: dict) -> str:

        text = doc["text"].lower()
        query = query.lower()

        reasons = []

        if "income" in text:
            reasons.append("Income risk factor evaluated")

        if "employment" in text:
            reasons.append("Employment stability assessed")

        if "credit" in text:
            reasons.append("Credit exposure considered")

        if "family" in text:
            reasons.append("Family burden impact included")

        if "collateral" in text:
            reasons.append("Collateral mitigation factor applied")

        return " | ".join(reasons) if reasons else "Semantic match"