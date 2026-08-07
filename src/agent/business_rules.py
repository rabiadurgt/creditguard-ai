from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RuleResult:
    name: str
    score: float
    triggered: bool
    message: str


class BusinessRuleEngine:

    def evaluate(self, request: Dict) -> Dict:

        rules: List[RuleResult] = []

        income = request.get("AMT_INCOME_TOTAL", 0)
        credit = request.get("AMT_CREDIT", 0)
        annuity = request.get("AMT_ANNUITY", 0)

        days_employed = abs(request.get("DAYS_EMPLOYED", 0))
        age_days = abs(request.get("DAYS_BIRTH", 0))

        ext1 = request.get("EXT_SOURCE_1", 0.5)
        ext2 = request.get("EXT_SOURCE_2", 0.5)
        ext3 = request.get("EXT_SOURCE_3", 0.5)

        late_ratio = request.get("late_payment_ratio", 0)
        active_contracts = request.get("active_credit_contracts", 0)

        family = request.get("CNT_FAM_MEMBERS", 1)

        employment_years = days_employed / 365
        age_years = age_days / 365

        credit_income_ratio = (
            credit / income
            if income > 0
            else 99
        )

        payment_ratio = (
            annuity / income
            if income > 0
            else 1
        )

        # -------------------------
        # Income
        # -------------------------

        if income < 100000:
            rules.append(
                RuleResult(
                    "Low Income",
                    20,
                    True,
                    "Annual income is below policy threshold."
                )
            )

        # -------------------------
        # Credit Burden
        # -------------------------

        if credit_income_ratio > 3:
            rules.append(
                RuleResult(
                    "High Credit Exposure",
                    25,
                    True,
                    "Credit amount exceeds three times annual income."
                )
            )

        # -------------------------
        # Payment Burden
        # -------------------------

        if payment_ratio > 0.30:
            rules.append(
                RuleResult(
                    "High Payment Burden",
                    15,
                    True,
                    "Annual payment burden is high."
                )
            )

        # -------------------------
        # Employment
        # -------------------------

        if employment_years < 1:
            rules.append(
                RuleResult(
                    "Insufficient Employment",
                    20,
                    True,
                    "Employment history is shorter than one year."
                )
            )

        # -------------------------
        # Age
        # -------------------------

        if age_years < 25:
            rules.append(
                RuleResult(
                    "Young Applicant",
                    10,
                    True,
                    "Applicant has limited financial history."
                )
            )

        # -------------------------
        # External Credit Scores
        # -------------------------

        ext_mean = (ext1 + ext2 + ext3) / 3

        if ext_mean < 0.30:
            rules.append(
                RuleResult(
                    "Poor External Credit Score",
                    30,
                    True,
                    "External credit score is significantly below average."
                )
            )

        # -------------------------
        # Late Payment
        # -------------------------

        if late_ratio > 0.40:
            rules.append(
                RuleResult(
                    "Late Payment History",
                    25,
                    True,
                    "High late payment ratio detected."
                )
            )

        # -------------------------
        # Active Credits
        # -------------------------

        if active_contracts >= 5:
            rules.append(
                RuleResult(
                    "Multiple Active Credits",
                    15,
                    True,
                    "Applicant has many active credit contracts."
                )
            )

        # -------------------------
        # Family Burden
        # -------------------------

        if family >= 6:
            rules.append(
                RuleResult(
                    "Large Household",
                    5,
                    True,
                    "Large household may increase financial burden."
                )
            )

        total_score = sum(rule.score for rule in rules)

        normalized_score = min(total_score / 100, 1.0)

        return {
            "risk_score": normalized_score,
            "total_points": total_score,
            "rules": rules
        }