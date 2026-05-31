import streamlit as st
from core.indicators import ESG_INDICATORS

st.header("📋 ESG Self-Assessment")

responses = {}

for pillar, indicators in ESG_INDICATORS.items():
    st.subheader(pillar)
    for indicator in indicators:
        # Store response by indicator ID (E1..G3) so it matches ML feature columns.
        responses[indicator["id"]] = st.slider(
            indicator["label"],
            0, 5, 0,
            help="0 = not implemented, 5 = fully implemented"
        )

st.session_state["assessment"] = responses
