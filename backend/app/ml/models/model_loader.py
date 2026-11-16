
from app.ml.models.model_registry import load_model


def get_prediction_model(
    model_name: str = "linear_regression",
    version: str = "v1"
):
    """
    Load a trained model for prediction.
    """

    model = load_model(model_name, version)

    return model
