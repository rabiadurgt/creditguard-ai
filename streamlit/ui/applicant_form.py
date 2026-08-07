import streamlit as st
import plotly.graph_objects as go


def render_applicant_form():

    st.markdown("## 👤 Applicant Overview")

    # ==================================================
    # FINANCIAL PROFILE
    # ==================================================

    with st.expander("💰 Financial Profile", expanded=True):

        c1, c2 = st.columns(2)

        with c1:

            income = st.number_input(
                "Annual Income",
                min_value=0,
                value=300000,
                step=1000,
            )

            credit = st.number_input(
                "Credit Amount",
                min_value=0,
                value=100000,
                step=1000,
            )

        with c2:

            goods = st.number_input(
                "Goods Price",
                min_value=0,
                value=80000,
                step=1000,
            )

            annuity = st.number_input(
                "Annual Payment",
                min_value=0,
                value=5000,
                step=100,
            )

        annuity_credit_ratio = annuity / credit if credit else 0
        percentage = annuity_credit_ratio * 100

        # ------------------------------
        # LIVE PAYMENT BURDEN
        # ------------------------------

        fig = go.Figure(
            data=[
                go.Pie(
                    values=[percentage, max(0, 100 - percentage)],
                    hole=0.72,
                    marker_colors=["#0A93A6", "#E2E8F0"],
                    hoverinfo="none",
                    textinfo="none",
                )
            ]
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            width=90,
            height=90,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        g1, g2 = st.columns([1, 6])

        with g1:
            st.plotly_chart(
                fig,
                config={"displayModeBar": False},
                use_container_width=False,
            )

        with g2:

            st.markdown(
                f"""
<div style="margin-top:5px">

<span style="font-size:13px;font-weight:600;color:#64748B;">
Payment Burden Ratio
</span>

<br>

<span style="font-size:28px;font-weight:700;color:#0F172A;">
{percentage:.2f}%
</span>

<br>

<span style="font-size:12px;color:#94A3B8;">
Payment burden is {percentage:.2f}% of requested credit.
</span>

</div>
""",
                unsafe_allow_html=True,
            )

    # ==================================================
    # CREDIT SCORES
    # ==================================================

    with st.expander("📊 Credit Assessment Scores"):

        c1, c2, c3 = st.columns(3)

        with c1:
            ext1 = st.slider("Financial Stability", 0.0, 1.0, 0.70, 0.01)

        with c2:
            ext2 = st.slider("External Credit Score", 0.0, 1.0, 0.75, 0.01)

        with c3:
            ext3 = st.slider("Credit History Score", 0.0, 1.0, 0.75, 0.01)

    # ==================================================
    # CREDIT HISTORY
    # ==================================================

    with st.expander("📚 Credit History"):

        c1, c2 = st.columns(2)

        with c1:
            active_contracts = st.number_input(
                "Active Contracts",
                min_value=0,
                value=1,
            )

        with c2:
            late_payment_ratio = st.slider(
                "Late Payment Ratio",
                0.0,
                1.0,
                0.05,
                0.01,
            )

    # ==================================================
    # PERSONAL INFORMATION
    # ==================================================

    with st.expander("👤 Personal Information"):

        c1, c2 = st.columns(2)

        with c1:

            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=40,
            )

            gender = st.selectbox(
                "Gender",
                ["M", "F"],
            )

        with c2:

            family = st.number_input(
                "Household Members",
                min_value=1,
                value=3,
            )

            children = st.number_input(
                "Children",
                min_value=0,
                value=1,
            )

    # ==================================================
    # EMPLOYMENT
    # ==================================================

    with st.expander("💼 Employment & Assets"):

        c1, c2 = st.columns(2)

        with c1:

            employment = st.number_input(
                "Employment Duration (Years)",
                min_value=0,
                max_value=60,
                value=15,
            )

            car = st.selectbox(
                "Own Car",
                ["Y", "N"],
            )

        with c2:

            realty = st.selectbox(
                "Own Realty",
                ["Y", "N"],
            )

    # ==================================================
    # PAYLOAD
    # ==================================================

    payload = {

        "AMT_INCOME_TOTAL": income,
        "AMT_GOODS_PRICE": goods,
        "AMT_CREDIT": credit,
        "AMT_ANNUITY": annuity,

        "annuity_credit_ratio": annuity_credit_ratio,

        "EXT_SOURCE_1": ext1,
        "EXT_SOURCE_2": ext2,
        "EXT_SOURCE_3": ext3,

        "CODE_GENDER": gender,

        "FLAG_OWN_CAR": car,
        "FLAG_OWN_REALTY": realty,

        "CNT_FAM_MEMBERS": family,
        "CNT_CHILDREN": children,

        "active_contracts": active_contracts,
        "late_payment_ratio": late_payment_ratio,

        "DAYS_BIRTH": -(age * 365),
        "DAYS_EMPLOYED": -(employment * 365),
    }

    # ==================================================
    # BUTTONS
    # ==================================================

    st.markdown("<br>", unsafe_allow_html=True)

    _, center, _ = st.columns([2, 3, 2])

    with center:

        b1, b2 = st.columns(2)

        with b1:
            reset = st.button(
                "↺ Reset",
                use_container_width=True,
            )

        with b2:
            submitted = st.button(
                "🔍 Analyze Credit Risk",
                use_container_width=True,
                type="primary",
            )

    if reset:
        st.rerun()

    return submitted, reset, payload