import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from .shared import (
    risk_color,
    status_icon,
)

# ==========================================================
# KPI CARD
# ==========================================================
def _kpi_card(
    title,
    value,
    icon="📊",
    subtitle="",
    progress=None
):

    progress_html = ""

    if progress is not None:
        # Streamlit'in HTML'i kod bloğu sanmaması için sol boşluklar kaldırıldı
        progress_val = max(0.0, min(float(progress), 100.0))
        progress_html = f'<div class="progress-container"><div class="progress-bar" style="width:{progress_val:.1f}%;"></div></div>'

    html = f"""<div class="card">
<div class="card-top">
<span class="card-icon">{icon}</span>
<span class="kpi-title">{title}</span>
</div>
<div class="kpi-value">{value}</div>
{progress_html}
<div class="kpi-subtitle">{subtitle}</div>
</div>"""

    st.markdown(html, unsafe_allow_html=True)

# ==========================================================
# SECTION TITLE
# ==========================================================

def _section(title, icon):
    st.markdown(
        f'<div class="section-title">{icon} {title}</div>',
        unsafe_allow_html=True,
    )

# ==========================================================
# APPLICANT OVERVIEW
# ==========================================================

def applicant_overview(payload):
    _section(
        "Applicant Overview",
         "👤"
    )
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        _kpi_card(
            title="Annual Income",
            value=f"{payload['AMT_INCOME_TOTAL']:,.0f}",
            icon="💰",
            subtitle="Annual gross income"
        )

    with c2:
        _kpi_card(
            title="Credit Amount",
            value=f"{payload['AMT_CREDIT']:,.0f}",
            icon="💳",
            subtitle="Requested loan"
        )

    with c3:
        _kpi_card(
            title="Age",
            value=f"{abs(payload['DAYS_BIRTH']) // 365}",
            icon="👤",
            subtitle="Applicant age"
        )

    with c4:
        _kpi_card(
            title="Employment",
            value=f"{abs(payload['DAYS_EMPLOYED']) // 365} yrs",
            icon="💼",
            subtitle="Working experience"
        )


# ==========================================================
# AI RECOMMENDATION
# ==========================================================
def ai_recommendation_card(result, show_title=True):

    if show_title:
        st.markdown(
            '<div class="section-title">🤖 AI Recommendation</div>',
            unsafe_allow_html=True
        )

    decision = result["decision"]["status"].upper()
    icon = status_icon(decision)

    if decision == "APPROVE":
        badge_class = "status-badge-approved"

    elif decision in ["REVIEW", "MANUAL REVIEW"]:
        badge_class = "status-badge-review"

    else:
        badge_class = "status-badge-rejected"

    st.markdown(
    f"""
<div class="{badge_class}">

<div class="kpi-title">
AI Recommendation
</div>

<div class="kpi-value">
{icon} {decision}
</div>

</div>
""",
    unsafe_allow_html=True,
)
# ==========================================================
# CONFIDENCE GAUGE
# ==========================================================

def confidence_gauge(confidence, show_title=True):
   
    with st.container(key="confidence_gauge_card"):
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=confidence * 100,
                number={"suffix": "%", "font": {"color": "#ffffff", "size": 30}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#a1a1a1"},
                    "bar": {"color": "#2563EB"},
                    "bgcolor": "#1e1e1e",
                    "borderwidth": 1,
                    "bordercolor": "#333333",
                    "steps": [
                        {"range": [0, 50], "color": "#3a1f1f"},
                        {"range": [50, 75], "color": "#3a3a1f"},
                        {"range": [75, 100], "color": "#1f3a1f"},
                    ],
                },
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=145,
            margin=dict(l=10, r=10, t=0, b=0),
        )

        st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# SHAP RISK DRIVERS (Plotly Çubuk Grafiği)
# ==========================================================

def shap_bar_chart(explanations):
    """
    Visual SHAP risk driver chart.
    Supports score / impact / value formats.
    """

    with st.container(key="shap_chart_card"):
        df = pd.DataFrame(explanations)

        # Normalize SHAP value column
        if isinstance(explanations, list) and len(explanations) > 0 and isinstance(explanations[0], str):
            
            parsed = []
            for item in explanations:
                parts = item.split(": impact")
                if len(parts) == 2:
                    parsed.append({"feature": parts[0].strip(), "score": float(parts[1].strip())})
            df = pd.DataFrame(parsed)

        if "score" not in df.columns:
            if "impact" in df.columns:
                df["score"] = df["impact"]
            elif "value" in df.columns:
                df["score"] = df["value"]
            elif 0 in df.columns: # Tek sütunlu DF durumları için
                parsed = []
                for val in df[0]:
                    parts = str(val).split(": impact")
                    if len(parts) == 2:
                        parsed.append({"feature": parts[0].strip(), "score": float(parts[1].strip())})
                df = pd.DataFrame(parsed)

        if df.empty or "score" not in df.columns:
            st.warning("SHAP explanation format is not supported.")
            return

        df = df.sort_values(
            by="score",
            ascending=True
        )

        # Risk colors
        df["color"] = df["score"].apply(
            lambda x: "#EF4444"
            if x > 0
            else "#22C55E"
        )

        fig = px.bar(
            df,
            x="score",
            y="feature",
            orientation="h",
            text="score",
        )

        fig.update_traces(
            marker_color=df["color"],
            texttemplate="%{text:.3f}",
            textposition="outside",
            textfont_color="#ffffff",
            hoverinfo="y+x",
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )