import streamlit as st

from styles import load_css

from components import (
    policy_summary_cards,
    policy_knowledge_base,
    show_retrieved_policies,
    policy_ranking_chart,
    policy_matrix
)

st.set_page_config(
    page_title="Policy Explorer",
    page_icon="📚",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

# =====================================================
# PAGE HEADER
# =====================================================

st.title("📚 Policy Explorer")

st.caption(
    "Explore the credit policies available to the RAG system "
    "and the policies retrieved for the current application."
)

# =====================================================
# SESSION CHECK
# =====================================================

if "result" not in st.session_state:
    st.warning("Please run a credit analysis from the Executive Dashboard first.")
    st.stop()

result = st.session_state["result"]
policies = result.get("policies", [])

# =====================================================
# POLICY SUMMARY
# =====================================================

policy_summary_cards(policies, total_policies=5)

st.divider()

# =====================================================
# POLICY KNOWLEDGE BASE
# =====================================================

with st.container(key="policy_explorer_page"):

    st.subheader("📚 Policy Knowledge Base")
    st.caption("Internal credit policies available to the RAG system.")

    policy_knowledge_base()

    st.divider()

# =====================================================
# RETRIEVED POLICY EVIDENCE / RETRIEVAL RANKING
# =====================================================
    if not policies:
        st.info("No relevant policies were retrieved for this application.")
        st.stop()

    col_evidence, col_ranking = st.columns(2)


    with col_evidence:
        st.subheader("📄 Retrieved Policy Evidence")
        st.caption("Policies retrieved and ranked for the current application.")
        show_retrieved_policies(policies)

    with col_ranking:
        st.subheader("📈 Retrieved Policy Ranking")
        st.caption("Ranking scores produced by the policy retrieval and reranking pipeline.")
        policy_ranking_chart(policies)

    st.divider()


# =====================================================
# POLICY EVALUATION
# =====================================================

st.subheader("📋 Policy Evaluation")
st.caption("Overview of all five policies and whether they were retrieved for this application.")

policy_matrix(policies)