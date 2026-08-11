# ui/layout.py

import streamlit as st

from components.dashboard import (
    applicant_overview,
    ai_recommendation_card,
    _kpi_card,
)

from components.shared import explain_shap


def render_dashboard(result, payload):

    # ======================================================
    # APPLICANT OVERVIEW
    # ======================================================

    applicant_overview(payload)

    st.divider()

    # ======================================================
    # EXECUTIVE SUMMARY
    # ======================================================

    st.markdown(
        '<div class="section-title">Executive Summary</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        ai_recommendation_card(
            result,
            show_title=False
        )


    with col2:

        _kpi_card(
            title="Default Probability",
            value=f"{result['risk_score']:.2%}",
            icon="⚠️",
            subtitle="Estimated default risk"
        )


    with col3:

        credit_amount = payload.get(
            "AMT_CREDIT",
            0
        )

        annual_income = payload.get(
            "AMT_INCOME_TOTAL",
            0
        )


        if annual_income > 0:

            dti = (
                credit_amount / annual_income
            ) * 100

        else:

            dti = 0.0


        _kpi_card(
            title="Debt to Income (DTI)",
            value=f"{dti:.1f}%",
            icon="💳",
            subtitle="Credit-to-income ratio",
            progress=dti
        )


    with col4:

        _kpi_card(
            title="Model Confidence",
            value=f"{result['confidence']:.2%}",
            icon="🎯",
            subtitle="Prediction certainty"
        )


    # ======================================================
    # RISK SUMMARY
    # ======================================================

    st.divider()


    st.markdown(
        '<div class="section-title">⚠️ Risk Summary</div>',
        unsafe_allow_html=True
    )


    positive_factors = []
    negative_factors = []


    for exp in result.get("explanations",[]):

        try:
            feature = exp.split(": impact")[0].strip()


            impact = float(
                exp.split(": impact")[1]
            )


            explanation = explain_shap(
                feature,
                impact
            )


            if impact < 0:

                positive_factors.append(explanation)

            else:

                negative_factors.append(explanation)


        except Exception:

            continue



    col1, col2 = st.columns(2)


    # ------------------------------
    # Positive Factors
    # ------------------------------

    with col1:

        st.markdown("### 🟢 Positive Factors")

        if positive_factors:

            for item in positive_factors[:3]:

                st.markdown(
                    f"""
<div class="driver-positive">

🟢 {item}

</div>
""",
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No strong positive risk drivers detected."
            )


    # ------------------------------
    # Risk Factors
    # ------------------------------

    with col2:

        st.markdown("### 🔴 Risk Factors")

        if negative_factors:

            for item in negative_factors[:3]:

                st.markdown(
                    f"""
<div class="driver-negative">

🔴 {item}

</div>
""",
                    unsafe_allow_html=True
                )

        else:

            st.success("No significant risk drivers detected.")