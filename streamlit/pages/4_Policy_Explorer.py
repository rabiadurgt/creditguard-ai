import streamlit as st

from styles import load_css

from components import (
    policy_summary_cards,
    show_retrieved_policies,
    show_policy_reasoning,
    policy_similarity_chart,
    policy_matrix
)

st.set_page_config(
    page_title="Policy Explorer",
    page_icon="📚",
    layout="wide"
)

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# ==================================================
# PAGE HEADER
# ==================================================

st.title("📚 Policy Explorer")

st.caption(
    "Review the internal credit policies retrieved by the AI during the decision-making process."
)

# ==================================================
# SESSION CHECK
# ==================================================

if "result" not in st.session_state:

    st.warning(
        "Please run a credit analysis from the Executive Dashboard first."
    )

    st.stop()

result = st.session_state["result"]
policies = result.get("policies", [])

if not policies:

    st.info(
        "No relevant policies were retrieved for this application."
    )

    st.stop()

# ==================================================
# POLICY OVERVIEW
# ==================================================

policy_summary_cards(policies)

st.divider()

# ==================================================
# RETRIEVED POLICIES
# ==================================================

left, right = st.columns(
    [2, 1],
    gap="large"
)

with left:

    st.subheader("📄 Retrieved Internal Policies")

    show_retrieved_policies(policies)

with right:

    st.subheader("🧠 Retrieval Reasoning")

    show_policy_reasoning(policies)

# ==================================================
# POLICY SIMILARITY
# ==================================================

st.divider()

st.subheader("📈 Policy Retrieval Similarity")

policy_similarity_chart(policies)

# ==================================================
# POLICY COMPLIANCE MATRIX
# ==================================================

st.divider()

st.subheader("📋 Policy Compliance Matrix")

policy_matrix(policies)