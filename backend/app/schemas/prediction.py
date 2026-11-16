
from datetime import datetime

from pydantic import BaseModel, Field


# Schema for prediction data
class PredictionData(BaseModel):

    symbol: str = Field(min_length=1, max_length=20)

    last_available_date: datetime

    current_close: float = Field(ge=0)

    predicted_next_close: float

    predicted_change: float

    predicted_change_percent: float

    model_name: str

    model_version: str


# Schema for complete prediction API response

class PredictionResponse(BaseModel):
    success: bool
    message: str
    data: PredictionData
    prediction_horizon: str = "Next available trading day"
    disclaimer: str = (
        "This prediction is experimental and is not financial advice. "
        "It does not guarantee future stock prices."
    )

