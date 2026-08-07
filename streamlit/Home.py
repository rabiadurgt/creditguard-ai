import streamlit as st
from styles import load_css

st.set_page_config(
    page_title="CreditGuard AI",
    page_icon="🏦",
    layout="wide"
)

st.markdown(
    load_css(),
    unsafe_allow_html=True
)

# ======================================================
# HEADER
# ======================================================

st.title("🏦 CreditGuard AI")

st.caption(
    """
AI-powered Credit Risk Decision Support Platform

**LightGBM • SHAP • RAG • FastAPI • Streamlit**
"""
)

st.markdown("---")

# ======================================================
# INTRODUCTION
# ======================================================

st.markdown(
    """
## 👋 Welcome

CreditGuard AI is an end-to-end AI-powered decision support platform for
credit risk assessment.

The platform combines:

- 🤖 LightGBM Risk Prediction
- 🔍 SHAP Explainability
- 📚 Retrieval-Augmented Generation (RAG)
- 🧠 AI Decision Engine
- 📋 Policy-Aware Reasoning

Use the navigation menu on the left to explore each module.
"""
)

# ======================================================
# TECHNOLOGY STACK
# ======================================================

st.markdown("---")

st.subheader("🛠️ Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        """
### 🤖 Machine Learning

- LightGBM
- Optuna
- Feature Engineering
"""
    )

with col2:
    st.info(
        """
### 🧠 Explainable AI

- SHAP
- Feature Importance
- Natural Language Explanations
"""
    )

with col3:
    st.info(
        """
### 📚 AI Decision Support

- FAISS
- MiniLM
- RAG
- Decision Agent
"""
    )

# ======================================================
# ARCHITECTURE
# ======================================================

st.markdown("---")

st.subheader("🏗️ System Architecture")

st.success(
    """
📥 Application

⬇️

⚙️ Feature Engineering

⬇️

🤖 LightGBM Prediction

⬇️

🔍 SHAP Explainability

⬇️

📚 RAG Policy Retrieval

⬇️

🧠 AI Decision Engine

⬇️

✅ Credit Recommendation
"""
)

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "CreditGuard AI v1.0 • AI Decision Support Platform"
)