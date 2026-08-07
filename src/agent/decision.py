from typing import Dict, List

from src.agent.business_rules import BusinessRuleEngine
from src.agent.policy_engine import PolicyEngine
from src.agent.reason_generator import ReasonGenerator
from src.agent.risk_fusion import RiskFusionEngine


class DecisionEngine:

    def __init__(self):

        self.business_engine = BusinessRuleEngine()
        self.policy_engine = PolicyEngine()
        self.fusion_engine = RiskFusionEngine()
        self.reason_generator = ReasonGenerator()

        self.audit_log = []

    # ==================================================
    # MAIN DECISION
    # ==================================================

    def decide(
        self,
        request: Dict,
        risk_score: float,
        explanations: List[str],
        policies: List[dict]
    ) -> Dict:

        # -----------------------------------------
        # 1. Business Rules
        # -----------------------------------------

        business = self.business_engine.evaluate(request)

        
        # -----------------------------------------
        # 2. Policy Evaluation
        # -----------------------------------------

        policy_result = self.policy_engine.evaluate(
            request=request,
            policies=policies
        )

        policy_score = policy_result["score"]

        # -----------------------------------------
        # 3. Risk Fusion
        # -----------------------------------------

        fusion = self.fusion_engine.fuse(
            model_score=risk_score,
            business_score=business["risk_score"],
            policy_score=policy_score
        )

        final_score = fusion["final_score"]

        # -----------------------------------------
        # 4. Decision
        # -----------------------------------------

        decision = self._decision_matrix(risk_score)
        risk_level = self._risk_level(risk_score)

        # -----------------------------------------
        # 5. Confidence
        # -----------------------------------------

        confidence = self._compute_confidence(
            model_score=risk_score,
            business_score=business["risk_score"],
            policy_score=policy_score,
            final_score=final_score
        )

        # -----------------------------------------
        # 6. Natural Language Reason
        # -----------------------------------------

        reason = self.reason_generator.generate(
            decision=decision,
            risk_score=risk_score,
            business_result=business,
            policy_result=policy_result
        )

        # -----------------------------------------
        # 7. Audit Object
        # -----------------------------------------

        audit = {

            "model_score": risk_score,
            "business_score": business["risk_score"],
            "policy_score": policy_score,
            
            "fusion": fusion,
            "fusion_details": {
                "model_score": risk_score,
                "business_score": business["risk_score"],
                "policy_score": policy_score
            },

            "final_score": final_score,
            "confidence": confidence,

            "decision": decision,
            "risk_level": risk_level,
            "reason": reason,

            "triggered_rules": business["rules"],

            "business_result": business,
            "policy_result": policy_result,
            "matched_policies": policy_result["matches"]
        }

        self.audit_log.append(audit)

        if len(self.audit_log) > 500:
            self.audit_log.pop(0)

        return audit



    # ==================================================
    # DECISION MATRIX
    # ==================================================

    def _decision_matrix(self, score: float) -> str:

        if score >= 0.25:
            return "REJECT"

        if score >= 0.10:
            return "REVIEW"

        return "APPROVE"

    # ==================================================
    # RISK LEVEL
    # ==================================================

    def _risk_level(self, score: float) -> str:

        if score >= 0.25:
            return "HIGH"

        if score >= 0.10:
            return "MEDIUM"

        return "LOW"

    # ==================================================
    # CONFIDENCE
    # ==================================================

    def _compute_confidence(
        self,
        model_score: float,
        business_score: float,
        policy_score: float,
        final_score: float
    ) -> float:

        agreement = 1.0 - abs(model_score - final_score)

        business_strength = 1.0 - abs(business_score - final_score)

        policy_strength = 1.0 - abs(policy_score - final_score)

        confidence = (
            0.50 * agreement +
            0.25 * business_strength +
            0.25 * policy_strength 
        )

        return round(max(0.30, min(confidence, 0.99)), 4)