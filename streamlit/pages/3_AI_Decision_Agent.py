import streamlit as st

from styles import load_css

from components import (
    executive_recommendation,
    reasoning_chain,
    policy_evidence,
    audit_trail
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Decision",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# =====================================================
# SESSION CHECK
# =====================================================

if "result" not in st.session_state:

    st.warning(
        "Please run a credit risk analysis from the Executive Dashboard first."
    )

    st.stop()

result = st.session_state["result"]

# =====================================================
# HEADER
# =====================================================

st.title("🤖 AI Decision")

st.caption(
    "Policy-aware AI decision support powered by "
    "LightGBM, SHAP, RAG and Decision Engine."
)

st.divider()

# =====================================================
# EXECUTIVE RECOMMENDATION
# =====================================================

st.subheader("🧠 Executive Decision")
executive_recommendation(result)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧠 AI Reasoning Process")
    reasoning_chain(result)

with col2:
    st.subheader("📚 Retrieved Policy Evidence")
    policy_evidence(result["policies"])

st.divider()

st.subheader("🛡️ Audit Trail")
audit_trail(result)