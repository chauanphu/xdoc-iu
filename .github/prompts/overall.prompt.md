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
app/
├── app.py                        # Main entrypoint to initialize FastAPI, middleware, and routing
├── config/
│   ├── __init__.py
│   └── settings.py               # Application configuration (env vars, DB settings, secrets)
├── auth/
│   ├── __init__.py
│   ├── models.py                 # ORM models for user and roles
│   ├── schemas.py                # Pydantic models for authentication endpoints
│   ├── routes.py                 # Endpoints: /login, /register, etc.
│   ├── services.py               # Business logic: token generation, password hashing, etc.
│   └── utils.py                  # Helper functions for authentication (e.g., JWT validation)
├── ml/
│   ├── __init__.py
│   ├── model.py                  # XGBoost model loader and inference logic
│   ├── preprocessing.py          # Data preprocessing functions for ML input
│   ├── postprocessing.py         # Functions to format or adjust inference output
│   └── routes.py                 # API endpoint(s) for predictions (/predict)
├── explainability/
│   ├── __init__.py
│   ├── shap_explainer.py         # Integrate SHAP for feature importance
│   ├── gemini_api.py             # Wrapper to interact with the Gemini API for natural language explanations
│   └── routes.py                 # Endpoints for explainability (/explain)
├── patient/
│   ├── __init__.py
│   ├── models.py                 # ORM models for patient profiles (with encryption where needed)
│   ├── schemas.py                # Pydantic schemas for patient data
│   ├── routes.py                 # CRUD endpoints for patient profile management
│   └── services.py               # Business logic for patient-related operations
├── hospital/
│   ├── __init__.py
│   ├── models.py                 # ORM models for hospital/tenant data
│   ├── schemas.py                # Pydantic schemas for hospital management
│   ├── routes.py                 # Endpoints to manage hospitals and associated doctors/patients
│   └── services.py               # Business logic for tenant management
├── db/
│   ├── __init__.py
│   ├── base.py                   # Base class for SQLAlchemy models
│   └── session.py                # Database session and connection management
├── tests/
│   ├── __init__.py
│   ├── test_auth.py              # Unit/integration tests for authentication module
│   ├── test_ml.py                # Tests for ML inference logic
│   ├── test_explainability.py    # Tests for explainability endpoints and logic
│   ├── test_patient.py           # Tests for patient profile management
│   └── test_hospital.py          # Tests for hospital/tenant management
└── Dockerfile                    # Containerization for deployment