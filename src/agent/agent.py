
from src.agent.decision import DecisionEngine

class CreditAgent:

    def __init__(self, rag_service, explainer, model):

        self.rag = rag_service
        self.explainer = explainer
        self.model = model

        # decision engine isolated
        self.decision_engine = DecisionEngine()

        # lightweight memory 
        self.memory = []


    # -------------------------
    # MAIN ORCHESTRATION
    # -------------------------
    def run(self, request, X, risk_score):

        # 1. CONTEXT BUILD
        context = self._build_context(request, risk_score)

        # 2. RAG RETRIEVAL
        policies = self.rag.explain(context["query"], k=3)

        # 3. MODEL EXPLANATION (SHAP)
        explanations = self.explainer.explain(X)

        # 4. POLICY-AWARE DECISION
        decision = self.decision_engine.decide(
            request=request,
            risk_score=risk_score,
            explanations=explanations,
            policies=policies
        )

        # 5. MEMORY UPDATE 
        self._update_memory(request, decision, risk_score)

        # 6. FINAL OUTPUT
        return {
            "decision": {
                "status": decision["decision"],
                "risk_level": decision["risk_level"],
                "reason": decision["reason"]
            },

            "risk_level": decision["risk_level"],
            "triggered_rules": decision["triggered_rules"],
            "matched_policies": decision["matched_policies"],
            "audit": decision,
            "policies": policies,
            "explanations": explanations,
            "confidence": decision["confidence"]
        }
    
    # -------------------------
    # CONTEXT BUILDER
    # -------------------------
    def _build_context(self, request, risk_score):

        return {
            "query":(
                f"credit={request.get('AMT_CREDIT', 0)}, "
                f"income={request.get('AMT_INCOME_TOTAL', 0)}, "
                f"employment={request.get('DAYS_EMPLOYED', 0)}, "
                f"risk={risk_score}"
            )
        }


    # -------------------------
    # MEMORY SYSTEM 
    # -------------------------
    def _update_memory(self, request, decision, risk_score):

        self.memory.append({
            "request": request,
            "decision": decision["decision"],
            "risk_level": decision["risk_level"],
            "risk_score": risk_score
        })

        # keep memory bounded
        if len(self.memory) > 100:
            self.memory.pop(0)

    

  