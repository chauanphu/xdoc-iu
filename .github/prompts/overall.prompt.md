Imagine you are an expert in software engineering and Machine Learning. Assist me in building an ML API server using FastAPI.

Your coding should follow SOLID principles with naming convention is concise, context-aware.

My application called XDoc predicts the diabetes (XGBoost) and explain its features' significance (SHAP) in natural language using LLM (Gemini).

This is the Server-side API. It manages the authentication, authorization; diseases prediction; managing patient profile (with database).

The system should has components for:
- Authentication / Authorization: logged in as patient or doctor.
- ML Model: inference, data preprocessing, data postprocessing
- Explainability: SHAP, Gemini API
- Patient Profile Management: user info (encrypted), each patient can be independent or assigned to an EHR of a hospital
- Hospital / Tenant Management: manages its corresponding doctors, patients and EHR system.

Folder structure:
- app.py: Initializes FastAPI, includes middleware (authentication, logging), and registers all route modules.
- `config/`: Centralizes configuration settings, making it easier to manage environment-specific variables.
- `auth/`: Encapsulates all authentication and authorization logic, including models, endpoint definitions, and services for token generation.
- `ml/`: Handles ML-specific logic—from loading the XGBoost model and preprocessing input data to performing inference and formatting the results.
- `explain/`: Focuses on model explainability using SHAP and the Gemini API, separating these concerns from the core prediction logic.
- `patient/` and `hospital/`: Separate domains to manage patient data and hospital/tenant relationships, ensuring each has its own set of models, schemas, and business logic.
- `db/`: Centralizes database access and model base definitions for reuse across modules. For both Redis cache and Postgres
- `tests/`: Contains unit and integration tests, ensuring that each module adheres to expected behavior.