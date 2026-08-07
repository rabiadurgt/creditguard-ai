import streamlit as st
import pandas as pd


# =====================================================
# SHAP HELPERS
# =====================================================

def parse_explanations(explanations):

    features = []
    impacts = []

    for exp in explanations:

        parts = exp.split(": impact")

        features.append(parts[0].strip())
        impacts.append(float(parts[1].strip()))

    return pd.DataFrame({
        "Feature": features,
        "Impact": impacts
    })


def explain_shap(feature, impact):

    feature_map = {

        "DAYS_BIRTH": "Applicant age",
        "DAYS_EMPLOYED": "Employment history",
        "employment_age_ratio": "Employment-to-age ratio",
        "annuity_credit_ratio": "Annuity-to-credit ratio",
        "credit_income_ratio": "Credit-to-income ratio",
        "income_per_family": "Income per family member",
        "income_per_child": "Income per child",
        "is_car_owner": "Vehicle ownership",
        "is_realty_owner": "Property ownership"

    }

    name = feature_map.get(feature, feature)

    if impact >= 0:
        return f"📈 {name} increased the predicted credit risk."

    return f"📉 {name} reduced the predicted credit risk."


# =====================================================
# STATUS HELPERS
# =====================================================

def status_color(status: str):

    colors = {

        "APPROVE": "#16a34a",
        "REVIEW": "#f59e0b",
        "REJECT": "#dc2626"

    }

    return colors.get(status.upper(), "#2563eb")


def status_icon(status: str):

    icons = {

        "APPROVE": "✅",
        "REVIEW": "⚠️",
        "REJECT": "❌"

    }

    return icons.get(status.upper(), "ℹ️")


# =====================================================
# RISK HELPERS
# =====================================================

def risk_color(level: str):

    colors = {

        "LOW": "#22c55e",
        "MEDIUM": "#f59e0b",
        "HIGH": "#ef4444"

    }

    return colors.get(level.upper(), "#2563eb")


def risk_icon(level: str):

    icons = {

        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🔴"

    }

    return icons.get(level.upper(), "⚪")


# =====================================================
# REUSABLE UI
# =====================================================

def badge(text, color="#2563eb"):

    st.markdown(
        f"""
<div style="
display:inline-block;
padding:6px 12px;
border-radius:20px;
background:{color};
color:white;
font-weight:600;
font-size:14px;
">
{text}
</div>
""",
        unsafe_allow_html=True
    )


def metric_card(title, value, subtitle=""):

    st.markdown(
        f"""
<div style="
padding:18px;
border-radius:14px;
background:white;
box-shadow:0 2px 8px rgba(0,0,0,.08);
margin-bottom:15px;
">

<p style="
margin:0;
font-size:14px;
color:#6b7280;
">
{title}
</p>

<h2 style="
margin-top:8px;
margin-bottom:6px;
">
{value}
</h2>

<p style="
margin:0;
font-size:13px;
color:#9ca3af;
">
{subtitle}
</p>

</div>
""",
        unsafe_allow_html=True
    )