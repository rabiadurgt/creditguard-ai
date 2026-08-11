import streamlit as st

from styles import load_css
from components import (
    shap_chart,
    feature_importance_table,
    top_risk_cards,
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
        "📊 Feature Impact",
        "⚠️ Risk Drivers",
        "📋 Feature Details",
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.markdown(
        '<div class="section-title">Top Feature Impact</div>',
        unsafe_allow_html=True
    )

    shap_chart(
        result["explanations"]
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    left, right = st.columns(2)


    with left:

        st.markdown(
            '<div class="section-title">🟢 Positive Factors</div>',
            unsafe_allow_html=True
        )


        top_risk_cards(
            [
                exp for exp in result["explanations"]
                if float(exp.split(": impact")[1]) < 0
            ]
        )


    with right:

        st.markdown(
            '<div class="section-title">🔴 Negative Factors</div>',
            unsafe_allow_html=True
        )


        top_risk_cards(
            [
                exp for exp in result["explanations"]
                if float(exp.split(": impact")[1]) >= 0
            ]
        )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.markdown(
        '<div class="section-title">Feature Impact Details</div>',
        unsafe_allow_html=True
    )


    feature_importance_table(
        result["explanations"]
    )