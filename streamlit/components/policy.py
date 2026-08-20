import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_DIR = PROJECT_ROOT / "data" / "policies"

POLICY_DESCRIPTIONS = {
    "policy_income": "Income level and financial stability",
    "policy_credit": "Credit exposure and credit-to-income",
    "policy_employment": "Employment stability and history",
    "policy_family": "Dependents and household obligations",
    "policy_collateral": "Property and vehicle ownership",
}

def _strip_first_heading(text):

    lines = text.strip().split("\n")

    if lines and lines[0].strip().startswith("#"):
        lines = lines[1:]

    return "\n".join(lines).strip()

# =====================================================
# SUMMARY STAT CARDS
# =====================================================

def policy_summary_cards(policies, total_policies=5):

    retrieved_count = len(policies)
    not_retrieved_count = max(total_policies - retrieved_count, 0)

    stats = [
        ("Total Policies", total_policies),
        ("Retrieved", retrieved_count),
        ("Not Retrieved", not_retrieved_count),
    ]

    cols = st.columns(3)

    for col, (label, value) in zip(cols, stats):
        with col:
            st.markdown(
                f'<div class="policy-stat-card">'
                f'<div class="policy-stat-value">{value}</div>'
                f'<div class="policy-stat-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True
            )


# =====================================================
# POLICY KNOWLEDGE BASE
# =====================================================

def policy_knowledge_base(policy_dir=None):

    policy_path = Path(policy_dir) if policy_dir else DEFAULT_POLICY_DIR
    files = sorted(policy_path.glob("*.md"))

    if not files:
        st.info("No policy documents found.")
        return

    cols = st.columns(3)

    for i, file in enumerate(files):

        policy_name = (
            file.stem
            .replace("policy_", "")
            .replace("_", " ")
            .title()
        )

        with cols[i % 3]:

            st.markdown(
                f'<div class="policy-kb-card">'
                f'<div class="policy-kb-title">📄 {policy_name} Policy</div>'
                f'<div class="policy-kb-source">Source: <code>{file.name}</code></div>'
                f'</div>',
                unsafe_allow_html=True
            )

            with st.expander("View policy"):
                content = _strip_first_heading(file.read_text(encoding="utf-8"))
                st.markdown(content)


# =====================================================
# RETRIEVED POLICY EVIDENCE
# =====================================================

def show_retrieved_policies(policies):

    if not policies:
        st.info("No relevant policies were retrieved for this application.")
        return

    for policy in policies:

        title = (
            policy.get("policy", "Unknown Policy")
            .replace("policy_", "")
            .replace("_", " ")
            .title()
        )

        score = policy.get("score", 0)
        reason = policy.get("reason", "No explanation available.")
        source = policy.get("policy", "unknown") + ".md"

        st.markdown(
            f'<div class="policy-explorer-card">'
            f'<div class="policy-explorer-header">'
            f'<span class="policy-explorer-title">📄 {title} Policy</span>'
            f'<span class="policy-explorer-score">Ranking: {score:.1f}</span>'
            f'</div>'
            f'<div class="policy-explorer-reason">{reason}</div>'
            f'<div class="policy-explorer-source">Source: <code>{source}</code></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        with st.expander("View policy"):
            policy_file = DEFAULT_POLICY_DIR / f"{policy.get('policy')}.md"
            if policy_file.exists():
                content = _strip_first_heading(policy_file.read_text(encoding="utf-8"))
                st.markdown(content)
            else:
                st.info("Policy source file not found.")


# =====================================================
# POLICY RETRIEVAL RANKING
# =====================================================

def policy_ranking_chart(policies):

    if not policies:
        st.info("No policies to chart.")
        return

    rows = [
        {
            "Policy": p.get("policy", "unknown").replace("policy_", "").replace("_", " ").title(),
            "Ranking Score": p.get("score", 0),
        }
        for p in policies
    ]

    df = pd.DataFrame(rows).sort_values("Ranking Score", ascending=True)

    fig = px.bar(df, x="Ranking Score", y="Policy", orientation="h", text="Ranking Score")

    fig.update_traces(
        marker_color="#0A93A6",
        texttemplate="%{text:.1f}",
        textposition="outside",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E4E4E7",
        xaxis=dict(gridcolor="#33353F", color="#8F98A8"),
        yaxis=dict(color="#E4E4E7"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=320,
    )

    with st.container(key="ranking_chart_card"):
        st.plotly_chart(fig, use_container_width=True)


# =====================================================
# POLICY EVALUATION MATRIX
# =====================================================
def policy_matrix(policies, policy_dir=None):

    policy_path = Path(policy_dir) if policy_dir else DEFAULT_POLICY_DIR
    all_files = sorted(policy_path.glob("*.md"))

    retrieved = {p.get("policy"): p for p in policies}

    rows = ""

    for file in all_files:

        key = file.stem
        name = key.replace("policy_", "").replace("_", " ").title()

        if key in retrieved:
            score = retrieved[key].get("score", 0)
            status_html = (
                '<span class="matrix-status matrix-retrieved">'
                '<span class="matrix-dot dot-green"></span>Retrieved</span>'
            )
            score_display = f"{score:.1f}"
            name_class = "matrix-name"
        else:
            status_html = (
                '<span class="matrix-status matrix-not-retrieved">'
                '<span class="matrix-dot dot-gray"></span>Not retrieved</span>'
            )
            score_display = "—"
            name_class = "matrix-name matrix-name-muted"

        rows += (
            f'<tr><td class="{name_class}">{name}</td>'
            f'<td>{status_html}</td>'
            f'<td class="matrix-score">{score_display}</td></tr>'
        )

    table_html = (
        '<div class="matrix-table-wrapper">'
        '<table class="matrix-table">'
        '<thead><tr><th>Policy</th><th>Retrieval status</th><th>Ranking</th></tr></thead>'
        f'<tbody>{rows}</tbody>'
        '</table>'
        '</div>'
    )

    st.markdown(table_html, unsafe_allow_html=True)


# =====================================================
# POLICY EVIDENCE — used by AI Decision Agent page
# =====================================================

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
            f'{title}</div>'
            f'<div class="policy-evidence-text">{reason}</div>'
            f'</div>'
        )

    st.markdown("".join(blocks), unsafe_allow_html=True)