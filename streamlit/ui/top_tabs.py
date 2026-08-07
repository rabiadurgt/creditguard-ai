import streamlit as st


def render_top_tabs():
    """
    Custom top navigation tabs.

    Returns
    -------
    str
        "input" or "result"
    """

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "input"

    col1, col2, _ = st.columns([1.4, 1.4, 5.2])

    with col1:

        input_active = (
            st.session_state.active_tab == "input"
        )

        if st.button(
            "📋 Input & Analysis",
            key="tab_input",
            type="primary" if input_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_tab = "input"
            st.rerun()

    with col2:

        result_active = (
            st.session_state.active_tab == "result"
        )

        if st.button(
            "📊 Risk Results",
            key="tab_result",
            type="primary" if result_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_tab = "result"
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    return st.session_state.active_tab