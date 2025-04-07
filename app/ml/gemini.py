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

generate_content_config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
    )

def prepare_prompt(columns: list[str], predicted_class, probabilities, shap_values, raw_data):
    # Create prompt
    top_indices: np.ndarray = np.argsort(np.abs(shap_values))[-3:][::-1]
    top_shap = shap_values[top_indices]
    top_values = raw_data[top_indices.tolist()]
    top_features = np.array(columns)[top_indices]

    class_labels = ["Không có bệnh tiểu đường", "Có bệnh tiểu đường", "Tiền tiểu đường"]
    prompt = f"""

    You are a medical assistant AI. Based on the following data, explain the diabetes prediction in simple terms for a patient.

    Your answer should be in Vietnamese and should include:
    - The predicted class and its probability.
    - The top 3 features contributing to the prediction, their values, and their SHAP contributions.
    - A brief explanation of the clinical context of the features.
    - The features are: {columns}
    - A disclaimer that this is not a medical diagnosis and the patient should consult a healthcare professional.

    Prediction: The model predicts a {probabilities[predicted_class]*100:.2f}% chance of being {class_labels[predicted_class]}.

    Top contributing factors:
    - Feature: {top_features[0]}, Value: {top_values[0]}, SHAP contribution: {top_shap[0]:.2f}
    - Feature: {top_features[1]}, Value: {top_values[1]}, SHAP contribution: {top_shap[1]:.2f}
    - Feature: {top_features[2]}, Value: {top_values[2]}, SHAP contribution: {top_shap[2]:.2f}

    Clinical context:
    - HbA1c: Normal <5.7%, Pre-Diabetes 5.7-6.4%, Diabetes ≥6.5%
    - Fasting Blood Sugar: Normal <100 mg/dL, Pre-Diabetes 100-125 mg/dL, Diabetes ≥126 mg/dL
    - BMI: Normal 18.5-24.9, Overweight 25-29.9, Obese ≥30

    Please provide a clear, concise explanation suitable for a non-technical audience.
    """
    return prompt

def generate(prompt):
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    answer = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return answer.text