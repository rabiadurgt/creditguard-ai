class QueryEnhancer:

    def expand(self, query: str) -> str:
        """
        Expand query with domain keywords
        """

        query = query.lower()

        expansions = []

        if "income" in query:
            expansions += ["salary", "earnings", "annual income"]

        if "credit" in query:
            expansions += ["loan", "debt", "credit score"]

        if "employment" in query:
            expansions += ["job", "work history", "tenure"]

        if "family" in query:
            expansions += ["dependents", "children", "household"]

        return query + " " + " ".join(expansions)