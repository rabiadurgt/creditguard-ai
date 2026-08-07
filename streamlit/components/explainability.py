import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.shared import (
    parse_explanations,
    explain_shap
)


def explain_shap(feature, impact):

    feature_map = {

        "DAYS_BIRTH":
            "Applicant age",

        "DAYS_EMPLOYED":
            "Employment history",

        "employment_age_ratio":
            "Employment-to-age ratio",

        "annuity_credit_ratio":
            "Annuity-to-credit ratio",

        "credit_income_ratio":
            "Credit-to-income ratio",

        "income_per_family":
            "Income per family member",

        "income_per_child":
            "Income per child",

        "is_car_owner":
            "Vehicle ownership",

        "is_realty_owner":
            "Property ownership"
    }

    name = feature_map.get(feature, feature)

    if impact >= 0:
        return f"📈 {name} increased the predicted credit risk."
    else:
        return f"📉 {name} reduced the predicted credit risk."



def shap_chart(explanations):

    features = []
    impacts = []

    for exp in explanations:

       

        parts = exp.split(": impact")

        feature = parts[0].strip()
        impact = float(parts[1].strip())


        features.append(feature)
        impacts.append(impact)

    df = pd.DataFrame({
        "Feature": features,
        "Impact": impacts
    })

    df = df.sort_values(
        "Impact"
    )

    with st.container(key="shap_chart_card"):

        colors = [
            "#EF4444" if x > 0 else "#22C55E"
            for x in df["Impact"]
        ]

        fig = px.bar(
            df,
            x="Impact",
            y="Feature",
            orientation="h",
            text="Impact",
        )

        fig.update_traces(
            marker_color=colors,
            texttemplate="%{text:.3f}",
            textposition="outside",
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10,r=10,t=20,b=10),
            height=320,
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


def top_risk_cards(explanations):

    df = parse_explanations(explanations)

    df = df.reindex(
        df["Impact"].abs().sort_values(ascending=False).index
    )

    for _, row in df.head(5).iterrows():

        color = "#ef4444" if row["Impact"] > 0 else "#22c55e"

        icon = "🔺" if row["Impact"] > 0 else "🟢"

        st.markdown(
f"""
<div class="card" style="margin-bottom:12px;">

<div class="kpi-title">
{icon} {row["Feature"]}
</div>

<div class="kpi-value" style="color:{color};">
{row["Impact"]:.3f}
</div>

<div class="kpi-subtitle">
SHAP Impact Score
</div>

</div>
""",
unsafe_allow_html=True
)

def natural_language_explanations(explanations, compact=False):

    parsed = []

    for exp in explanations:

        feature = exp.split(": impact")[0]

        impact = float(
            exp.split(": impact")[1]
        )

        parsed.append(
            (
                feature,
                impact,
                explain_shap(feature, impact)
            )
        )

    # ======================================================
    # Executive Summary küçük kartları
    # ======================================================

    if compact:

        parsed = sorted(
            parsed,
            key=lambda x: abs(x[1]),
            reverse=True
        )[:3]

        for _, impact, text in parsed:

            color = "#EF4444" if impact > 0 else "#22C55E"

            st.markdown(
    f"""
<div class="xai-card">

<div class="xai-title">
Insight
</div>

<div
class="xai-text"
style="
border-left:4px solid {color};
padding-left:10px;
">

{text}

</div>

</div>
""",
    unsafe_allow_html=True
)

        return

    # ======================================================
    # Full explanations
    # ======================================================

    st.markdown(
        """
The following explanations summarize the model's reasoning
in business-friendly language.
"""
    )

    for _, _, text in parsed:

        st.markdown(
    f"""
<div class="xai-card">

<div class="xai-text">

{text}

</div>

</div>
""",
    unsafe_allow_html=True
)


def feature_importance_table(explanations):

    df = parse_explanations(explanations)

    df["Absolute Impact"] = df["Impact"].abs()

    df = df.sort_values(
        "Absolute Impact",
        ascending=False
    )

    df.insert(
        0,
        "Rank",
        range(1, len(df) + 1)
    )

    with st.container(key="feature_table_card"):

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

def prediction_breakdown(explanations):

    df = parse_explanations(explanations)

    df = df.sort_values(
        "Impact",
        ascending=False
    )

    colors = [
        "#ef4444" if x > 0 else "#22c55e"
        for x in df["Impact"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Impact"],
            y=df["Feature"],
            orientation="h",
            marker_color=colors
        )
    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        xaxis_title="Impact",

        yaxis_title="",

        height=320,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )   

    with st.container(key="prediction_breakdown_card"):

        st.plotly_chart(
            fig,
            use_container_width=True
        )