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
explainer = shap.Explainer(model, X)
shap_values = explainer(X)

# -----------------------------
# Beeswarm plot (CORRECT)
# -----------------------------
st.subheader("Global Feature Importance (Beeswarm)")

fig, ax = plt.subplots()          # ✅ create Figure explicitly
shap.plots.beeswarm(shap_values, show=False)
st.pyplot(fig)                    # ✅ pass Figure, not Axes
plt.close(fig)                    # ✅ cleanup



# import streamlit as st
# import shap
# import pandas as pd
# from core.ml_models import train_model

# st.header("🧠 Explainability (XAI)")

# data = pd.read_csv("data/sample_training.csv")
# X = data.drop("esg_score", axis=1)
# y = data["esg_score"]

# model = train_model(X, y)
# explainer = shap.Explainer(model, X)

# shap_values = explainer(X)

# st.pyplot(shap.plots.beeswarm(shap_values, show=False))
