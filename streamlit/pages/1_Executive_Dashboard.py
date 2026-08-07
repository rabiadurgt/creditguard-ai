import streamlit as st

from datetime import datetime

from styles import load_css
from api_client import predict_credit

from ui.sidebar import render_sidebar
from ui.applicant_form import render_applicant_form
from ui.layout import render_dashboard
from ui.top_tabs import render_top_tabs

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)


# ==========================================================
# SESSION STATE
# ==========================================================

if "result" not in st.session_state:
    st.session_state["result"] = None


if "last_payload" not in st.session_state:
    st.session_state["last_payload"] = None

if "prediction_count" not in st.session_state:
    st.session_state["prediction_count"] = 0

# ==========================================================
# HEADER
# ==========================================================

st.title("🏦 Executive Credit Decision Dashboard")

st.caption(
        "AI-powered credit risk assessment combining "
        "Machine Learning, Explainable AI and Policy Intelligence."
    )


# ==========================================================
# SIDEBAR
# ==========================================================

render_sidebar()

# ==========================================================
# TOP TABS
# ==========================================================

active_tab = render_top_tabs()

if active_tab == "input":

    submitted, reset, payload = render_applicant_form()

    if reset:
        st.session_state["result"] = None
        st.session_state["last_payload"] = None
        st.session_state["active_tab"] = "📋 Input & Analysis"
        st.rerun()

    if submitted:

        with st.spinner("Analyzing applicant..."):

            result = predict_credit(payload)

        if result:

            result["prediction_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state.result = result
            st.session_state["prediction_count"] += 1
            
            st.session_state.last_payload = payload

            st.session_state.active_tab = "result"

            st.toast(
                "Credit risk analysis completed.",
                icon="✅",
            )

            st.rerun()

        else:

            st.error(
                "Prediction service is unavailable."
            )

else:

    if st.session_state.result:

        render_dashboard(
            st.session_state.result,
            st.session_state.last_payload,
        )

    else:

        st.info(
            "Run a credit assessment first."
        )