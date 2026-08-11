import streamlit as st
import pandas as pd

from datetime import datetime   
from .shared import (
    status_color,
    status_icon
)

def show_agent(decision):

    status = decision["status"]
    reason = decision["reason"]

    color = status_color(status)
    icon = status_icon(status)

    st.markdown(
        f"""
<div style="
padding:20px;
border-radius:14px;
border-left:8px solid {color};
background:#f8fafc;
margin-bottom:20px;
">

<h2 style="
margin-top:15px;
color:{color};
">
{icon} {status}
</h2>

<p style="font-size:17px;">
{reason}
</p>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("### Decision Summary")
    st.success("✔ LightGBM model evaluated applicant")
    st.success("✔ SHAP explanation generated")
    st.success("✔ Credit policies retrieved from RAG")
    st.success("✔ Final recommendation created")


def executive_recommendation(result):

    decision = result["decision"]["status"]
    reason = result["decision"]["reason"]
    confidence = result["confidence"]

    color = status_color(decision)
    icon = status_icon(decision)

    pct_display = f"{confidence * 100:.2f}"
    pct_value = int(round(confidence * 100))

    st.markdown(
f"""
<div class="card executive-decision-card">

<div class="executive-decision-content">

<div class="card-top">
<span class="card-icon">{icon}</span>
<span class="kpi-title">Executive Decision</span>
</div>

<div class="kpi-value" style="color:{color};">{decision}</div>

<div class="kpi-subtitle">{reason}</div>

</div>

<div class="exec-decision-gauge">
<div class="exec-gauge-circle" style="background: conic-gradient(#0A93A6 0% {pct_value}%, #33353F {pct_value}% 100%);">
<div class="exec-gauge-inner">
<span class="exec-gauge-value">{pct_display}%</span>
</div>
</div>
<div class="exec-gauge-label">Decision Confidence</div>
</div>

</div>
""",
unsafe_allow_html=True
)
    

def reasoning_chain(result):

    decision = result["decision"]["status"]

    status_styles = {
        "APPROVE": {"color": "#22C55E", "bg": "rgba(34, 197, 94, 0.12)"},
        "REVIEW":  {"color": "#FACC15", "bg": "rgba(250, 204, 21, 0.12)"},
        "REJECT":  {"color": "#EF4444", "bg": "rgba(239, 68, 68, 0.12)"},
    }

    final_style = status_styles.get(
        decision,
        {"color": "#22C55E", "bg": "rgba(34, 197, 94, 0.12)"}
    )

    steps = [
        "LightGBM generated default probability",
        "SHAP identified influential features",
        "Relevant credit policies retrieved",
        "Decision Engine fused all evidence",
        f"Final Recommendation: {decision}",
    ]

    total = len(steps)
    blocks = []

    for i, text in enumerate(steps, start=1):

        if i == total:
            marker_style = (
                f'background:{final_style["color"]}22;'
                f'border-color:{final_style["color"]};'
                f'color:{final_style["color"]};'
            )
            text_style = f'color:{final_style["color"]};font-weight:700;'
        else:
            marker_style = ""
            text_style = ""

        blocks.append(
            f'<div class="reasoning-step">'
            f'<div class="reasoning-step-marker">'
            f'<span class="reasoning-step-number" style="{marker_style}">{i}</span>'
            f'<span class="reasoning-step-line"></span>'
            f'</div>'
            f'<div class="reasoning-step-text" style="{text_style}">{text}</div>'
            f'</div>'
        )

    st.markdown(
        f'<div class="reasoning-timeline">{"".join(blocks)}</div>',
        unsafe_allow_html=True
    )

def decision_justification(result):

    st.info(
        f"""
The AI Decision Engine recommends **{result["decision"]["status"]}**
because the machine learning model predicts a
default probability of **{result["risk_score"]:.2%}**.

This recommendation is supported by:

• SHAP feature importance analysis

• Relevant credit risk policies

• Decision Engine evidence fusion

The final recommendation balances
statistical prediction with business rules.
"""
    )



def audit_trail(result):

    import html

    audit = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Model": result["meta"]["model"],
        "Decision": result["decision"]["status"],
        "Risk Score": f"{result['risk_score']:.2%}",
        "Confidence": f"{result['confidence']:.2%}",
        "Policies Retrieved": len(result["policies"]),
        "SHAP Features": len(result["explanations"]),
    }

    rows = "".join(
        f'<tr><td class="audit-attr-cell">{html.escape(str(k))}</td>'
        f'<td class="audit-value-cell">{html.escape(str(v))}</td></tr>'
        for k, v in audit.items()
    )

    table_html = (
        '<div class="audit-table-wrapper">'
        '<table class="audit-table">'
        '<thead><tr><th>Attribute</th><th>Value</th></tr></thead>'
        f'<tbody>{rows}</tbody>'
        '</table>'
        '</div>'
    )

    st.markdown(table_html, unsafe_allow_html=True)


def agent_workflow():

    st.subheader("⚙️ Agent Workflow")

    workflow = [
        ("📥", "Application received"),
        ("⚡", "Feature engineering completed"),
        ("🤖", "LightGBM risk prediction"),
        ("🔍", "SHAP explanation generated"),
        ("📚", "RAG policy retrieval"),
        ("🧠", "Decision Engine reasoning"),
        ("✅", "Final recommendation")
    ]

    for icon, step in workflow:
        st.markdown(
            f"""
<div style="
padding:10px;
margin-bottom:8px;
border-radius:8px;
background:#f8fafc;
border-left:5px solid #3b82f6;
">
<b>{icon} {step}</b>
</div>
""",
            unsafe_allow_html=True
        )
