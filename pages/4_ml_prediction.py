import streamlit as st
import pandas as pd
import time
from core.ml_models import train_model

st.header("🤖 ML-Based ESG Prediction")

# -----------------------------
# Load data
# -----------------------------
data = pd.read_csv("data/sample_training.csv")
X = data.drop("esg_score", axis=1)
y = data["esg_score"]

# -----------------------------
# Progress UI
# -----------------------------
progress_bar = st.progress(0)
status_text = st.empty()

status_text.text("Initializing model...")
time.sleep(0.3)
progress_bar.progress(10)

status_text.text("Preparing training data...")
time.sleep(0.3)
progress_bar.progress(30)

status_text.text("Training ESG prediction model...")
with st.spinner("Training ML model (XGBoost)..."):
    model = train_model(X, y)

progress_bar.progress(70)

status_text.text("Finalizing model...")
time.sleep(0.2)
progress_bar.progress(90)

status_text.text("Model ready")
progress_bar.progress(100)

# -----------------------------
# Prediction
# -----------------------------
if "assessment" in st.session_state:
    input_df = pd.DataFrame([st.session_state["assessment"]])

    with st.spinner("Predicting ESG score..."):
        pred = model.predict(input_df)[0]

    st.metric("Predicted ESG Score", round(pred, 2))
else:
    st.info("Please complete the ESG self-assessment first.")
