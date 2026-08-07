import streamlit as st
from datetime import datetime


def render_sidebar():
    """
    Global application sidebar.

    Contains only:
        - Brand
        - Application settings
        - Global actions

    Returns
    -------
    analyze : bool
        Whether analysis button was clicked.

    settings : dict
        Global application settings.
    """

    # ==================================================
    # BRAND
    # ==================================================

    st.sidebar.title("🏦 CreditGuard AI")

    st.sidebar.caption(
        "AI-Powered Credit Risk Platform"
    )

    st.sidebar.divider()

    # ==================================================
    # APPLICATION SETTINGS
    # ==================================================

    st.sidebar.subheader("⚙ Application Settings")

    applicant_id = st.sidebar.text_input(
        "Applicant ID",
        value="APP-100001"
    )

    application_date = st.sidebar.date_input(
        "Application Date",
        value=datetime.today()
    )

    st.sidebar.divider()

    # ==================================================
    # ACTIONS
    # ==================================================

    
    settings = {
        "applicant_id": applicant_id,
        "application_date": application_date
    }

    return settings