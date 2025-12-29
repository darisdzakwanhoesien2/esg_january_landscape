import streamlit as st
import pandas as pd
from core.ml_models import train_model

st.header("🤖 ML-Based ESG Prediction")

data = pd.read_csv("data/sample_training.csv")

X = data.drop("esg_score", axis=1)
y = data["esg_score"]

model = train_model(X, y)

if "assessment" in st.session_state:
    input_df = pd.DataFrame([st.session_state["assessment"]])
    pred = model.predict(input_df)[0]
    st.metric("Predicted ESG Score", round(pred, 2))