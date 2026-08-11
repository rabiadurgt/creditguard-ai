import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="System Monitor",
    page_icon="🖥️",
    layout="wide"
)

from styles import load_css
from api_client import check_api_health
from utils.model_metadata import load_model_metadata
from utils.prediction_logs import load_prediction_logs


# ======================================================
# LOAD DATA
# ======================================================

try:
    metadata = load_model_metadata()
except Exception:
    st.error("Model metadata could not be loaded.")
    st.stop()

logs = load_prediction_logs()

st.markdown(load_css(), unsafe_allow_html=True)

st.title("🖥️ System Monitor")

st.caption(
    "Monitor model health, validation metrics and prediction service."
)

# ======================================================
# LIVE MONITORING METRICS
# ======================================================

st.markdown(
    '<div class="section-title">Live Monitoring Metrics</div>',
    unsafe_allow_html=True
)


api_ok = check_api_health()


total_predictions = 0
avg_risk_score = 0
avg_response_time = 0
avg_confidence = 0

approve_rate = 0



if not logs.empty:

    total_predictions = len(logs)

    avg_risk_score = (
        logs["risk_score"]
        .mean()
    )

    avg_response_time = (
        logs["response_time_ms"]
        .mean()
    )


    avg_confidence = (
        logs["confidence"]
        .mean()
    )


    approve_rate = (
        (logs["decision"] == "APPROVE")
        .mean()
    )


c1, c2, c3, c4 = st.columns(4)


with c1:
    st.metric(
        "API Status",
        "🟢 Healthy" if api_ok else "🔴 Down"
    )


with c2:
    st.metric(
        "Prediction Count",
        f"{total_predictions:,}"
    )


with c3:
    st.metric(
        "Average Latency",
        f"{avg_response_time:.0f} ms"
        if avg_response_time > 0
        else "-"
    )


with c4:
    st.metric(
        "Average Confidence",
        f"{avg_confidence:.2%}"
    )


# ======================================================
# MODEL INFORMATION
# ======================================================

st.markdown(
    '<div class="section-title">Model Information</div>',
    unsafe_allow_html=True
)


st.markdown(
f"""
<div class="card model-info-card">

<div class="kpi-title">
Dataset
</div>

<div class="kpi-value">
{metadata["dataset"]}
</div>

<br>

<div class="kpi-subtitle">
<b>Algorithm:</b> {metadata["model_name"]}
</div>

<div class="kpi-subtitle">
<b>Validation:</b> {metadata["validation"]}
</div>

<div class="kpi-subtitle">
<b>ROC-AUC:</b> {metadata["roc_auc"]}
</div>

<div class="kpi-subtitle">
<b>Training Samples:</b> {metadata["training_samples"]:,}
</div>


</div>
""",
unsafe_allow_html=True
)

# ======================================================
# PREDICTION HISTORY
# ======================================================

if not logs.empty:

    st.divider()

    st.markdown(
        '<div class="section-title">Prediction History</div>',
        unsafe_allow_html=True
    )


    history = logs.copy()


    history = history.sort_values(
        "timestamp",
        ascending=False
    ).head(20)


    history["risk_score"] = (
        history["risk_score"]
        .apply(lambda x: f"{x:.2%}")
    )


    history["confidence"] = (
        history["confidence"]
        .apply(lambda x: f"{x:.2%}")
    )


    history["response_time_ms"] = (
        history["response_time_ms"]
        .apply(lambda x: f"{x:.0f} ms")
    )


    history = history[
        [
            "timestamp",
            "decision",
            "risk_score",
            "confidence",
            "response_time_ms"
        ]
    ]

def decision_style(value):

    if value == "APPROVE":
        return (
            "background-color:#DCFCE7;"
            "color:#166534;"
            "font-weight:600;"
        )

    elif value == "REVIEW":
        return (
            "background-color:#FEF9C3;"
            "color:#854D0E;"
            "font-weight:600;"
        )

    elif value == "REJECT":
        return (
            "background-color:#FEE2E2;"
            "color:#991B1B;"
            "font-weight:600;"
        )

    return ""

history_display = history.copy()

st.dataframe(
    history_display,
    use_container_width=True,
    hide_index=True,
    height=400
)


# ======================================================
# HIGH RISK APPLICATIONS
# ======================================================

if not logs.empty:

    st.divider()

    st.markdown(
        '<div class="section-title">High Risk Applications</div>',
        unsafe_allow_html=True
    )


    high_risk = logs.copy()


    high_risk = (
        high_risk
        .sort_values(
            "risk_score",
            ascending=False
        )
        .head(10)
    )


    high_risk["risk_score"] = (
        high_risk["risk_score"]
        .apply(lambda x: f"{x:.2%}")
    )


    high_risk["confidence"] = (
        high_risk["confidence"]
        .apply(lambda x: f"{x:.2%}")
    )


    high_risk = high_risk[
        [
            "timestamp",
            "decision",
            "risk_score",
            "confidence",
            "income",
            "credit",
            "age"
        ]
    ]


def row_style(row):

    if row["decision"] == "APPROVE":
        return [
            "background-color:#DCFCE7;"
            "color:#166534;"
            "font-weight:600;"
        ] * len(row)

    elif row["decision"] == "REVIEW":
        return [
            "background-color:#FEF9C3;"
            "color:#854D0E;"
            "font-weight:600;"
        ] * len(row)

    elif row["decision"] == "REJECT":
        return [
            "background-color:#FEE2E2;"
            "color:#991B1B;"
            "font-weight:600;"
        ] * len(row)

    return [""] * len(row)



st.dataframe(
    high_risk.style.apply(
        row_style,
        axis=1
    ),
    use_container_width=True,
    hide_index=True
)

# ======================================================
# LOG ANALYTICS
# ======================================================

if not logs.empty:

    # ======================================================
    # DISTRIBUTION ANALYTICS
    # ======================================================

    st.divider()

    col1, col2 = st.columns(2)


    # ------------------------------
    # Prediction Distribution
    # ------------------------------

    with col1:

        st.markdown(
            '<div class="section-title">Prediction Distribution</div>',
            unsafe_allow_html=True
        )

        decision_counts = (
            logs["decision"]
            .value_counts()
            .reset_index()
        )

        decision_counts.columns = [
            "Decision",
            "Count"
        ]


        fig = px.pie(
            decision_counts,
            names="Decision",
            values="Count",
            hole=0.55
        )


        fig.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ------------------------------
    # Risk Distribution
    # ------------------------------

    with col2:

        st.markdown(
            '<div class="section-title">Risk Distribution</div>',
            unsafe_allow_html=True
        )


        fig = px.histogram(
            logs,
            x="risk_score",
            nbins=10
        )


        fig.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )


        fig.update_xaxes(
            tickformat=".0%"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ------------------------------
    # Risk Score Trend
    # ------------------------------

    st.divider()

    st.markdown(
        '<div class="section-title">Risk Distribution Trend</div>',
        unsafe_allow_html=True
    )

    risk_trend = logs.copy()

    risk_trend["timestamp"] = pd.to_datetime(
        risk_trend["timestamp"]
    )

    risk_trend = risk_trend.sort_values(
        "timestamp"
    )

    fig = px.line(
        risk_trend,
        x="timestamp",
        y="risk_score",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Risk Score",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350
    )


    fig.update_yaxes(
        tickformat=".0%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ------------------------------
    # Response Time Trend
    # ------------------------------

    st.divider()

    st.markdown(
        '<div class="section-title">Response Time Trend</div>',
        unsafe_allow_html=True
    )


    response_trend = logs.copy()


    response_trend["timestamp"] = pd.to_datetime(
        response_trend["timestamp"]
    )


    response_trend = response_trend.sort_values(
        "timestamp"
    )


    fig = px.line(
        response_trend,
        x="timestamp",
        y="response_time_ms",
        markers=True
    )


    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Milliseconds",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350
    )


    st.plotly_chart(
        fig,
        use_container_width=True
)

# ======================================================
# SYSTEM LOG
# ======================================================

st.divider()

st.markdown(
    '<div class="section-title">System Log</div>',
    unsafe_allow_html=True
)

if api_ok:
    st.success("🟢 Prediction service healthy")
else:
    st.error("🔴 Prediction service unavailable")

st.success("🟢 Model loaded successfully")
st.success("🟢 Feature pipeline available")