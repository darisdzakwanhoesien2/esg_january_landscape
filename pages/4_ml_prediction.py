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
with st.spinner("Training ML model..."):
    # `train_model` chooses XGBoost if available, otherwise falls back to RandomForest.
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
    missing = [c for c in X.columns if c not in input_df.columns]
    if missing:
        st.error(
            "Assessment responses don't match the model features. "
            f"Missing: {', '.join(missing)}"
        )
        st.stop()

    # map descriptive assessment keys to the model's feature names
    feature_map = {
        "Energy consumption monitoring": "E1",
        "Carbon emissions tracking": "E2",
        "Waste management policy": "E3",
        "Employee safety policy": "S1",
        "Diversity & inclusion": "S2",
        "Community engagement": "S3",
        "Board structure": "G1",
        "Anti-corruption policy": "G2",
        "Data protection": "G3",
    }
    # rename any descriptive columns to the short codes used in training
    input_df = input_df.rename(columns={k: v for k, v in feature_map.items() if k in input_df.columns})

    # determine expected feature order from the trained model or training X
    expected_cols = None
    try:
        expected_cols = model.get_booster().feature_names
    except Exception:
        pass
    if expected_cols is None:
        try:
            expected_cols = X.columns.tolist()
        except Exception:
            expected_cols = list(input_df.columns)

    # add missing features with zeros and ensure correct column order
    for col in expected_cols:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_cols]

    with st.spinner("Predicting ESG score..."):
        pred = model.predict(input_df)[0]

    st.metric("Predicted ESG Score", round(pred, 2))
else:
    st.info("Please complete the ESG self-assessment first.")
