from typing import Dict


class RiskFusionEngine:
    """
    Combines multiple risk signals into a single decision score.

    Sources:
        - ML Model
        - Business Rules
        - Policy Engine
    """

    def __init__(self):

        self.weights = {
            "model": 0.55,
            "business": 0.30,
            "policy": 0.15
        }

    # ----------------------------------------------------
    # MAIN
    # ----------------------------------------------------

    def fuse(
        self,
        model_score: float,
        business_score: float,
        policy_score: float
    ) -> Dict:

        final_score = (
            self.weights["model"] * model_score +
            self.weights["business"] * business_score +
            self.weights["policy"] * policy_score
        )

        final_score = max(0.0, min(1.0, final_score))

        confidence = self._confidence(
            model_score,
            business_score,
            policy_score
        )

        return {
            "final_score": round(final_score, 4),
            "confidence": confidence,
            "weights": self.weights
        }

    # ----------------------------------------------------
    # CONFIDENCE
    # ----------------------------------------------------

    def _confidence(
        self,
        model: float,
        business: float,
        policy: float
    ) -> float:

        scores = [
            model,
            business,
            policy
        ]

        mean = sum(scores) / len(scores)

        variance = sum(
            (x - mean) ** 2
            for x in scores
        ) / len(scores)

        agreement = 1 - variance

        return round(
            max(0.30, min(1.0, agreement)),
            3
        )