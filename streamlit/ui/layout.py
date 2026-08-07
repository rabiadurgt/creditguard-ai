# ui/layout.py

import streamlit as st

from components.dashboard import (
    applicant_overview,
    ai_recommendation_card,
    shap_bar_chart,
)

from components.policy import (
    policy_evidence,
)


def render_dashboard(result, payload):

    # ======================================================
    # APPLICANT OVERVIEW
    # ======================================================

    applicant_overview(payload)

    st.divider()

    # ======================================================
    # EXECUTIVE SUMMARY
    # ======================================================

    from components.dashboard import _kpi_card

    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        ai_recommendation_card(result, show_title=False)

    with col2:
        _kpi_card(
            title="Default Probability",
            value=f"{result['risk_score']:.2%}",
            icon="⚠️",
            subtitle="Estimated default risk"
        )

    with col3:

        credit_amount = payload.get("AMT_CREDIT", 0)
        annual_income = payload.get("AMT_INCOME_TOTAL", 0)

        if annual_income > 0:
            dti = (credit_amount / annual_income) * 100
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


    st.divider()

    st.info(
    """
    **Model Validation**

    Predictions are produced by a **LightGBM** model trained on the **Home Credit Default Risk** dataset.

    • Validation Strategy: **5-Fold Cross Validation**

    • ROC-AUC: **0.78**
    
    • Training Samples: **307,511**

    These metrics indicate the model has been evaluated on unseen data and the prediction is not based solely on training performance.
    """
    )
    
    # ======================================================
    # DETAILED ANALYSIS
    # ======================================================

    st.markdown('<div class="section-title">Detailed Analysis</div>', unsafe_allow_html=True)

    left, spacer, right = st.columns([1,0.06,1])

    with left:
        shap_bar_chart(result["explanations"])

    with right:
        st.markdown(
            '<div class="section-title">Policy Validation</div>',
            unsafe_allow_html=True
        )
        with st.container(key="policy_card"):
            policy_evidence(result["policies"])