# app/explain/gemini_client.py
import requests

class GeminiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def generate_explanation(self, shap_values, additional_context: dict) -> str:
        # Craft the payload as required by the Gemini API
        payload = {
            "shap_values": shap_values.tolist(),
            "context": additional_context
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.base_url}/explain", json=payload, headers=headers)
        return response.json().get("explanation", "")