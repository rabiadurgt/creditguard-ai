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

    color = status_color(decision)
    icon = status_icon(decision)
   
    st.markdown(f"""
<div style="
padding:24px;
background:white;
border-radius:16px;
border-left:8px solid {color};
box-shadow:0 4px 12px rgba(0,0,0,.08);
">

<h2 style="margin:0;">
{icon} Executive Recommendation
</h2>

<h1 style="
margin-top:20px;
color:{color};
">
{decision}
</h1>

<p style="font-size:18px;">
{reason}
</p>

</div>
""", unsafe_allow_html=True)
    

def reasoning_chain(result):

    steps = [

        ("①", "LightGBM generated default probability"),
        ("②", "SHAP identified influential features"),
        ("③", "Relevant credit policies retrieved"),
        ("④", "Decision Engine fused all evidence"),
        ("⑤", f"Final Recommendation: {result['decision']['status']}")
    ]

    for number, text in steps:

        st.markdown(
            f"""
<div style="
padding:12px;
margin-bottom:10px;
background:#f8fafc;
border-radius:10px;
border-left:5px solid #2563eb;
">
<b>{number}</b> {text}
</div>
""",
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

    audit = {

        "Timestamp":

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Model":

            result["meta"]["model"],

        "Decision":

            result["decision"]["status"],

        "Risk Score":

            f"{result['risk_score']:.2%}",

        "Confidence":

            f"{result['confidence']:.2%}",

        "Policies Retrieved":

            len(result["policies"]),

        "SHAP Features":

            len(result["explanations"])
    }

    df = pd.DataFrame(
        audit.items(),
        columns=["Attribute", "Value"]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )



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
