
from fastapi import APIRouter, HTTPException, Depends

from app.api.deps import get_current_user
from app.ml.services.prediction_service import predict_stock_price
from app.schemas.prediction import PredictionResponse

router = APIRouter(
    prefix="/predictions",
    tags=["Stock Predictions"]
)



# Static route - FIRST
@router.get("/model-info")
def get_prediction_model_info(
    current_user=Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "model_name": "Linear Regression",
            "model_version": "v1",
            "supported_symbols": ["RELIANCE"],
            "prediction_horizon": "Next available trading day",
            "features_count": 15,
            "model_type": "Regression",
            "status": "Active"
        }
    }


# Dynamic route - AFTER STATIC ROUTE
@router.get("/{symbol}", response_model=PredictionResponse)
def get_stock_prediction(
    symbol: str,
    current_user=Depends(get_current_user)
):
    try:
        result = predict_stock_price(symbol)

        return {
            "success": True,
            "message": "Stock prediction generated successfully",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Prediction model not found"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating prediction"
        )




