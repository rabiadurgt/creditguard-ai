class ToolBox:

    def __init__(self, rag_service, explainer):
        self.rag = rag_service
        self.explainer = explainer

    def run_rag(self, query):
        return self.rag.retrieve(query, k=3)

    def run_explain(self, X):
        return self.explainer.explain(X, top_k=5)