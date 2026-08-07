from typing import Dict, List


class PolicyEngine:

    """
    Evaluates applicant information against retrieved
    policy documents.

    Returns

    score:
        overall policy risk score

    matches:
        policy evaluation details
    """

    def evaluate(

        self,

        request: Dict,

        policies: List[dict]

    ):

        matches = []

        score = 0.0

        income = request.get(
            "AMT_INCOME_TOTAL",
            0
        )

        credit = request.get(
            "AMT_CREDIT",
            0
        )

        employment_years = abs(
            request.get(
                "DAYS_EMPLOYED",
                0
            )
        ) / 365

        family = request.get(
            "CNT_FAM_MEMBERS",
            1
        )

        owns_realty = (
            request.get("FLAG_OWN_REALTY") == "Y"
        )

        for policy in policies:

            source = policy.get(
                "source",
                policy.get("policy", "")
            )

            # -----------------------
            # Income Policy
            # -----------------------

            if source == "policy_income":

                if income >= 150000:

                    matches.append({

                        "policy": "Income Policy",
                        "status": "PASS",
                        "message":
                        "Income satisfies policy."

                    })

                else:

                    score += 0.20

                    matches.append({

                        "policy": "Income Policy",
                        "status": "WARNING",
                        "message":
                        "Income below preferred threshold."

                    })

            # -----------------------
            # Employment Policy
            # -----------------------

            elif source == "policy_employment":

                if employment_years >= 2:

                    matches.append({

                        "policy": "Employment Policy",
                        "status": "PASS",
                        "message":
                        "Employment history acceptable."

                    })

                else:

                    score += 0.20

                    matches.append({

                        "policy": "Employment Policy",
                        "status": "FAIL",
                        "message":
                        "Employment history too short."

                    })

            # -----------------------
            # Credit Policy
            # -----------------------

            elif source == "policy_credit":

                ratio = credit / max(income, 1)

                if ratio <= 3:

                    matches.append({

                        "policy": "Credit Policy",
                        "status": "PASS",
                        "message":
                        "Debt burden acceptable."

                    })

                else:

                    score += 0.30

                    matches.append({

                        "policy": "Credit Policy",
                        "status": "FAIL",
                        "message":
                        "Credit exposure exceeds policy."

                    })

            # -----------------------
            # Family Policy
            # -----------------------

            elif source == "policy_family":

                if family <= 5:

                    matches.append({

                        "policy": "Family Policy",
                        "status": "PASS",
                        "message":
                        "Family size acceptable."

                    })

                else:

                    score += 0.10

                    matches.append({

                        "policy": "Family Policy",
                        "status": "WARNING",
                        "message":
                        "Large household increases financial burden."

                    })

            # -----------------------
            # Collateral Policy
            # -----------------------

            elif source == "policy_collateral":

                if owns_realty:

                    matches.append({

                        "policy": "Collateral Policy",
                        "status": "PASS",
                        "message":
                        "Property ownership strengthens application."

                    })

                else:

                    score += 0.05

                    matches.append({

                        "policy": "Collateral Policy",
                        "status": "INFO",
                        "message":
                        "No collateral provided."

                    })

        return {

            "score": min(score, 1.0),

            "matches": matches

        }