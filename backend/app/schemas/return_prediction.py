
from datetime import datetime

from pydantic import BaseModel, Field


class ReturnPredictionResponse(BaseModel):

    symbol: str

    company_name: str

    last_available_date: datetime

    current_close: float = Field(ge=0)

    predicted_return: float

    predicted_return_percent: float

    model_name: str

    model_version: str

    prediction_horizon: str

    generated_at: datetime

    disclaimer: str = (
        "This prediction is experimental and is not "
        "financial advice. It does not guarantee future returns."
    )
