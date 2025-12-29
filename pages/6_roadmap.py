import streamlit as st

st.header("🛣 ESG Improvement Roadmap")

if "assessment" not in st.session_state:
    st.warning("Complete assessment first.")
else:
    gaps = {
        k: v for k, v in st.session_state["assessment"].items()
        if v < 3
    }

    for item, score in gaps.items():
        st.write(f"🔧 **{item}** → Recommended improvement (current score: {score})")