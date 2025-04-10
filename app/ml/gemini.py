import os
from google import genai
from google.genai import types
from config.settings import settings
import numpy as np

if settings.GEMINI_API_KEY is None:
    raise ValueError("Please set the GEMINI_API_KEY environment variable")
client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)

model = "gemini-2.0-flash"

# Model for Doctor (Precise and Clinical)
FOR_DOCTOR = (
    "You are a medical decision support assistant for healthcare professionals. "
    "Provide precise and concise clinical explanations based on SHAP feature importance. "
    "Use accurate medical terminology and statistical details. "
    "Prioritize clinical relevance and actionable insights without unnecessary elaboration."
    "Avoid using overly technical jargon that may confuse the audience. "
    "Focus on the most significant features and their implications for patient care. "
    "Use the following format: "
    "- **Feature** (value: {value}): SHAP = {shap_value:.3f}\n"
    "  - Explanation: {explanation}\n"
    "  - Clinical significance: {clinical_significance}\n"
)
# Model for Patient (Educational and Empathetic)
FOR_PATIENT=(
    "You are a patient-friendly medical assistant. "
    "Explain disease predictions in a clear, educational, and empathetic manner. "
    "Clearly define technical terms and concepts (e.g., SHAP, cholesterol, blood pressure). "
    "Provide practical health advice relevant to each feature discussed."
    "Use the following format: "
    "- **Feature** (value: {value}): SHAP = {shap_value:.3f}\n"
    "  - Explanation: {explanation}\n"
    "  - Clinical significance: {clinical_significance}\n"
    "  - Practical advice: {practical_advice}\n"
    "  - Lifestyle changes: {lifestyle_changes}\n"
    "Add disclaimer: 'This is a machine-generated response based on data and should not replace professional medical advice.'"
)

def build_diabetes_prompt(features_with_shap: list[dict], prediction: int, confidence: float, audience: str):
    sorted_features = sorted(features_with_shap, key=lambda x: abs(x['shap_value']), reverse=True)
    feature_explanations = "\n".join([
        f"- **{item['feature']}** (value: {item['value']}): SHAP = {item['shap_value']:.3f}"
        for item in sorted_features
    ])
    
    match prediction:
        case 0:
            label = "Non-Diabetic"
        case 1:
            label = "Pre-Diabetic"
        case 2:
            label = "Diabetic"
        case _:
            raise ValueError("Invalid prediction value. Must be 0, 1, or 2.")
        
    if audience == "doctor":
        prompt = f"""
        Prediction: {label} risk of diabetes ({confidence:.1%} confidence).

        SHAP Feature Contributions:
        {feature_explanations}

        Provide a precise clinical interpretation emphasizing the significance of these features.
        """
    elif audience == "patient":
        prompt = f"""
        Based on your health data, the model estimates your risk of diabetes is **{'high' if prediction else 'low'}** (confidence: {confidence:.1%}).

        Here's why this prediction was made, including how each factor influenced the result:

        {feature_explanations}

        Please explain clearly what each factor means for the patient's health, defining medical terms in simple language, and offer practical suggestions for improvement.
        """
    else:
        raise ValueError("Audience must be 'doctor' or 'patient'.")

    return prompt.strip()

def build_cardio_prompt(features_with_shap: list[dict], prediction: int, confidence: float, audience: str):
    sorted_features = sorted(features_with_shap, key=lambda x: abs(x['shap_value']), reverse=True)
    feature_explanations = "\n".join([
        f"- **{item['feature']}** (value: {item['value']}): SHAP = {item['shap_value']:.3f}"
        for item in sorted_features
    ])

    if audience == "doctor":
        prompt = f"""
        Prediction: {'High' if prediction else 'Low'} risk of cardiovascular disease ({confidence:.1%} confidence).

        SHAP Feature Contributions:
        {feature_explanations}

        Provide a precise clinical interpretation emphasizing the significance of these features.
        """
    elif audience == "patient":
        prompt = f"""
        Based on your health data, the model estimates your risk of heart disease is **{'high' if prediction else 'low'}** (confidence: {confidence:.1%}).

        Here's why this prediction was made, including how each factor influenced the result:

        {feature_explanations}

        Please explain clearly what each factor means for the patient's health, defining medical terms in simple language, and offer practical suggestions for improvement.
        """
    else:
        raise ValueError("Audience must be 'doctor' or 'patient'.")

    return prompt.strip()

def generate(prompt, audience):
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=FOR_DOCTOR if audience == "doctor" else FOR_PATIENT,
    )
    answer = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return answer.text