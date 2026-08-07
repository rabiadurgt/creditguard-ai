import streamlit as st

from styles import load_css

from components import (
    executive_recommendation,
    confidence_gauge,
    reasoning_chain,
    policy_evidence,
    decision_justification,
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

left, right = st.columns(
    [2, 1],
    gap="large"
)

with left:

    executive_recommendation(result)

with right:

    confidence_gauge(
        result["confidence"]
    )

# =====================================================
# AI REASONING
# =====================================================

st.divider()

st.subheader("🧠 AI Reasoning Process")

reasoning_chain(result)

# =====================================================
# POLICY EVIDENCE
# =====================================================

st.divider()

st.subheader("📚 Policy Evidence")

policy_evidence(
    result["policies"]
)

# =====================================================
# DECISION JUSTIFICATION
# =====================================================

st.divider()

st.subheader("📝 Decision Justification")

decision_justification(result)

# =====================================================
# AUDIT TRAIL
# =====================================================

st.divider()

st.subheader("🛡️ Audit Trail")

audit_trail(result)