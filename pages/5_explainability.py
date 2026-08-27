# import streamlit as st
# import shap
# import pandas as pd
# import matplotlib.pyplot as plt
# from core.ml_models import train_model

# st.header("🧠 Explainability (XAI)")

# # -----------------------------
# # Load data
# # -----------------------------
# data = pd.read_csv("data/sample_training.csv")
# X = data.drop("esg_score", axis=1)
# y = data["esg_score"]

# # -----------------------------
# # Train model
# # -----------------------------
# model = train_model(X, y)
# explainer = shap.Explainer(model, X)
# shap_values = explainer(X)

# # -----------------------------
# # Beeswarm plot (FIXED)
# # -----------------------------
# st.subheader("Global Feature Importance (Beeswarm)")

# plt.figure()
# shap.plots.beeswarm(shap_values, show=False)

# fig = plt.gcf()   # ✅ Get current figure
# st.pyplot(fig)
# plt.close(fig)    # ✅ Prevent memory leaks

import streamlit as st
import shap
import pandas as pd
import matplotlib.pyplot as plt
from core.ml_models import train_model

st.header("🧠 Explainability (XAI)")

# -----------------------------
# Load data
# -----------------------------
data = pd.read_csv("data/sample_training.csv")
X = data.drop("esg_score", axis=1)
y = data["esg_score"]

# -----------------------------
# Train model
# -----------------------------
model = train_model(X, y)

# SHAP can be computationally expensive. Using the training matrix as the
# background distribution helps estimate "typical" feature values for SMEs.
# Prefer TreeExplainer for tree models; fall back to the function explainer.
try:
    explainer = shap.TreeExplainer(model)
except Exception:
    explainer = shap.Explainer(model.predict, X)

shap_values = explainer(X)

# -----------------------------
# Beeswarm plot (CORRECTED)
# -----------------------------
st.subheader("Global Feature Importance (Beeswarm)")

fig = plt.gcf()                  # ✅ get the current Figure (not an Axes)
st.pyplot(fig)                    # ✅ pass Figure, not Axes
plt.close(fig)                    # ✅ cleanup
