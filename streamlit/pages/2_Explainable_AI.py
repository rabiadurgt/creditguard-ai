import streamlit as st

from styles import load_css
from components import (
    shap_chart,
    natural_language_explanations,
    feature_importance_table,
    top_risk_cards,
    prediction_breakdown
)

st.set_page_config(
    page_title="Explainable AI",
    page_icon="🔍",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

st.title("🔍 Explainable AI")

st.caption(
    "Understand how the AI model reached its prediction."
)

# ---------------------------------------
# Check whether an analysis exists
# ---------------------------------------

if "result" not in st.session_state:

    st.warning(
        "Please run an analysis from Executive Dashboard first."
    )

    st.stop()

# ---------------------------------------
# Load result
# ---------------------------------------

result = st.session_state["result"]


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Summary Dashboard",
        "📈 Feature Analysis",
        "📋 Data Details",
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    left, right = st.columns([2.2, 1], gap="large")

    with left:

        st.markdown(
            '<div class="section-title">Top Feature Impact</div>',
            unsafe_allow_html=True
        )

        shap_chart(result["explanations"])

    with right:

        st.markdown(
            '<div class="section-title">Top Risk Drivers</div>',
            unsafe_allow_html=True
        )

        top_risk_cards(result["explanations"])

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">Model Reasoning Insights</div>',
            unsafe_allow_html=True
        )

        natural_language_explanations(
            result["explanations"],
            compact=True
        )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.markdown(
        '<div class="section-title">Prediction Breakdown</div>',
        unsafe_allow_html=True
    )

    prediction_breakdown(
        result["explanations"]
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.markdown(
        '<div class="section-title">Feature Impact Ranking</div>',
        unsafe_allow_html=True
    )

    feature_importance_table(
        result["explanations"]
    )

    st.divider()

    st.markdown(
        '<div class="section-title">Natural Language Explanation</div>',
        unsafe_allow_html=True
    )

    natural_language_explanations(
        result["explanations"]
    )