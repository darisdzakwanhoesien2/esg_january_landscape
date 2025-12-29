import streamlit as st
from core.scoring import compute_esg_score

st.header("📊 ESG Score")

if "assessment" not in st.session_state:
    st.warning("Complete the assessment first.")
else:
    score = compute_esg_score(st.session_state["assessment"])
    st.metric("Overall ESG Score", f"{score}/100")