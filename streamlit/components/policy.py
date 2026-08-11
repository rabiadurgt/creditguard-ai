import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def policy_summary_cards(policies):

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Retrieved Policies",
            len(policies)
        )


    with col2:

        high_risk = sum(
            1
            for p in policies
            if "reject" in p.get("text", "").lower()
        )

        st.metric(
            "High Risk Policies",
            high_risk
        )


    with col3:

        avg_similarity = 0

        scores = [
            p.get("similarity", 0)
            for p in policies
        ]

        if scores:
            avg_similarity = sum(scores) / len(scores)


        st.metric(
            "Average Similarity",
            f"{avg_similarity:.2f}"
        )

        
def show_retrieved_policies(policies):

    for policy in policies:

        title = (
            policy.get(
                "policy",
                "Unknown Policy"
            )
            .replace("_", " ")
            .title()
        )


        st.markdown(
            f"""
<div style="
padding:15px;
margin-bottom:12px;
background:white;
border-radius:12px;
border:1px solid #e5e7eb;
">

<h4>📄 {title}</h4>

<p>
{policy.get("reason","No explanation available.")}
</p>

</div>
""",
            unsafe_allow_html=True
        )


def show_policy_reasoning(policies):

    st.info(
        """
The AI retrieved these policies based on
semantic similarity between the applicant profile
and internal credit rules.
"""
    )


    for policy in policies:

        score = policy.get(
            "similarity",
            None
        )


        if score:

            st.write(
                f"🔎 {policy['policy']} "
                f"- similarity: {score:.2f}"
            )

def policy_similarity_chart(policies):

    rows = []


    for policy in policies:

        rows.append({

            "Policy":
                policy.get(
                    "policy",
                    "Unknown"
                ),

            "Similarity":
                policy.get(
                    "similarity",
                    0
                )
        })


    df = pd.DataFrame(rows)


    fig = px.bar(
        df,
        x="Similarity",
        y="Policy",
        orientation="h",
        title="Policy Retrieval Similarity"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
def policy_matrix(policies):

    if not policies:
        st.info("No policies were retrieved.")
        return

    rows = []

    for policy in policies:

        name = policy.get(
            "policy",
            "Unknown"
        ).replace(
            "policy_",
            ""
        ).replace(
            "_",
            " "
        ).title()

        text = policy.get(
            "text",
            ""
        ).lower()

        if "reject" in text:

            severity = "High"
            status = "🔴 Critical"

        elif (
            "manual review" in text
            or "review" in text
        ):

            severity = "Medium"
            status = "🟡 Review"

        else:

            severity = "Low"
            status = "🟢 Passed"

        rows.append({

            "Policy": name,

            "Status": status,

            "Severity": severity,

            "Matched": "✔"

        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def policy_evidence(policies):

    if not policies:
        st.info("No policies were retrieved.")
        return

    accent_colors = ["#3B82F6", "#22C55E", "#FACC15"]
    blocks = []

    for i, policy in enumerate(policies):
        title = policy["policy"].replace("_", " ").title()
        reason = policy.get("reason", "No explanation available.")
        color = accent_colors[i % len(accent_colors)]

        blocks.append(
            f'<div class="policy-evidence-card" style="border-left-color:{color};">'
            f'<div class="policy-evidence-title">'
            f'<span class="policy-evidence-icon" style="background:{color};"></span>'
            f'{title}'
            f'</div>'
            f'<div class="policy-evidence-text">{reason}</div>'
            f'</div>'
        )

    st.markdown("".join(blocks), unsafe_allow_html=True)



