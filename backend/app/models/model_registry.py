
from pathlib import Path
import joblib


# Project backend directory
BACKEND_DIR = Path(__file__).resolve().parents[3]

# Directory to store trained model artifacts
ARTIFACT_DIR = BACKEND_DIR / "app" / "ml" / "artifacts"


def save_model(model, model_name: str, version: str = "v1"):
    """
    Save a trained ML model using Joblib.
    """

    if not model_name or not version:
        raise ValueError("Model name and version are required")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    model_path = ARTIFACT_DIR / f"{model_name}_{version}.joblib"

    joblib.dump(model, model_path)

    print(f"Model saved successfully: {model_path}")

    return model_path


def load_model(model_name: str, version: str = "v1"):
    """
    Load a previously saved ML model.
    """

    model_path = ARTIFACT_DIR / f"{model_name}_{version}.joblib"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found: {model_path}"
        )

    model = joblib.load(model_path)

    print(f"Model loaded successfully: {model_path}")

    return model
