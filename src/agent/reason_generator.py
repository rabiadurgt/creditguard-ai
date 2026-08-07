from typing import Dict


class ReasonGenerator:

    def generate(
        self,
        decision: str,
        risk_score: float,
        business_result: Dict,
        policy_result: Dict
    ) -> str:

        sections = []

        # ==================================================
        # Recommendation
        # ==================================================

        if decision == "APPROVE":

            sections.append(
                f"The application is recommended for approval with an estimated default probability of {risk_score:.2%}."
            )

        elif decision == "REVIEW":

            sections.append(
                f"The application requires manual review because the estimated default probability is {risk_score:.2%}."
            )

        else:

            sections.append(
                f"The application is recommended for rejection due to an estimated default probability of {risk_score:.2%}."
            )

        # ==================================================
        # Positive Findings
        # ==================================================

        positive = []

        for rule in business_result.get("rules", []):

            text = rule.message.lower()

            if any(
                keyword in text
                for keyword in [
                    "good",
                    "stable",
                    "low",
                    "acceptable",
                    "property",
                    "employment",
                    "income"
                ]
            ):
                positive.append(rule.message)

        if positive:

            sections.append("")
            sections.append("Positive Findings:")

            for item in positive:
                sections.append(f"• {item}")

        # ==================================================
        # Risk Factors
        # ==================================================

        negative = []

        for rule in business_result.get("rules", []):

            text = rule.message.lower()

            if any(
                keyword in text
                for keyword in [
                    "high",
                    "late",
                    "overdue",
                    "low credit",
                    "large",
                    "many",
                    "risk"
                ]
            ):
                negative.append(rule)

        if negative:

            sections.append("")
            sections.append("Risk Factors:")

            for item in negative:
                sections.append(f"• {item}")

        # ==================================================
        # Policy Evaluation
        # ==================================================

        matches = policy_result.get("matches", [])

        if matches:

            sections.append("")
            sections.append("Policy Assessment:")

            for match in matches:

                policy = match.get("policy", "Unknown Policy")
                message = match.get("message", "")

                sections.append(
                    f"• {policy}: {message}"
                )

        # ==================================================
        # Final Recommendation
        # ==================================================

        sections.append("")
        sections.append("Final Recommendation:")

        if decision == "APPROVE":

            sections.append(
                "The applicant satisfies the current business and policy requirements for credit approval."
            )

        elif decision == "REVIEW":

            sections.append(
                "Additional underwriting assessment is recommended before a final lending decision."
            )

        else:

            sections.append(
                "The applicant exceeds the institution's acceptable credit risk threshold."
            )

        return "\n".join(sections)