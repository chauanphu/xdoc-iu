import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
from streamlit.components.v1 import html
import requests
import os

# Load data (replace with your dataset path and preprocessing)
data = pd.read_csv("diabetes.csv")  # Example dataset
X_test = data.drop(columns=["Class"])    # Features only; adjust columns as needed
class_labels = ["Non-Diabetic", "Pre-Diabetic", "Diabetic"]  # Adjust based on your data

# Load pre-trained XGBoost model
xgb_model = xgb.XGBClassifier()
xgb_model.load_model("xgb_model.json")  # Path to your saved model

# Set up SHAP explainer
explainer = shap.TreeExplainer(xgb_model)

# Streamlit app
st.title("Diabetes Prediction Explainer")

# Select patient from dropdown
patient_idx = st.selectbox("Select Patient", options=range(len(X_test)))
single_patient = X_test.iloc[patient_idx]

# **Display Patient Details**
st.subheader("Patient Details")
st.table(single_patient.to_frame().T)

# **Make Prediction**
predicted_class = xgb_model.predict(single_patient.values.reshape(1, -1))[0]
probabilities = xgb_model.predict_proba(single_patient.values.reshape(1, -1))[0]
st.subheader("Model Prediction")
st.write(f"**Predicted Class:** {class_labels[predicted_class]}")
st.write(f"**Probabilities:** {dict(zip(class_labels, probabilities))}")

# **Calculate SHAP Values**
shap_values = explainer.shap_values(single_patient.values.reshape(1, -1))
shap_vals_pred = shap_values[0, :, predicted_class]  # SHAP values for predicted class
base_value = explainer.expected_value[predicted_class]  # Base value for predicted class

# # **Generate Prompt**
# top_feature_idx = np.argmax(np.abs(shap_vals_pred))
# top_feature = X_test.columns[top_feature_idx]
# prompt = f"""
# You are a medical assistant AI. Explain the diabetes prediction in simple terms for a patient.
# Prediction: {class_labels[predicted_class]} with {probabilities[predicted_class]*100:.0f}% confidence.
# Top contributing factor: {top_feature} = {single_patient[top_feature]}, SHAP contribution: {shap_vals_pred[top_feature_idx]:.2f}.
# """
# # Note: Enhance this prompt by adding more features or context as needed.

# # **Call Gemini API (Hypothetical)**
# api_key = os.getenv("GEMINI_API_KEY")  # Set this in your environment
# url = "https://api.gemini.ai/v1/generate"  # Replace with actual endpoint
# headers = {"Authorization": f"Bearer {api_key}"}
# data = {"prompt": prompt, "max_tokens": 200}
# try:
#     response = requests.post(url, headers=headers, json=data)
#     explanation = response.json()["text"]
# except Exception as e:
#     explanation = f"Error fetching explanation: {str(e)}"

# # **Display Explanation**
# st.subheader("Explanation from LLM")
# st.write(explanation)
# **Display SHAP Force Plot**
# Create the force plot (ensure you're not forcing matplotlib rendering)
# Generate SHAP force plot (without Matplotlib)
st.subheader("SHAP Waterfall Plot")
fig, ax = plt.subplots(figsize=(10, 6))  # Adjust size as needed
shap.plots.waterfall(shap.Explanation(
    values=shap_vals_pred,                      # SHAP values
    base_values=explainer.expected_value[predicted_class],  # Base value
    data=single_patient,                        # Input data
    feature_names=X_test.columns.tolist()       # Feature names
))
st.pyplot(fig)
# **Display Prompt (Optional)**
# with st.expander("View Prompt Sent to LLM"):
#     st.write(prompt)