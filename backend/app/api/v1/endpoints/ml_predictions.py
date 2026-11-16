
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db

from app.ml.services.return_prediction_service import (
    predict_stock_return
)

from app.schemas.return_prediction import (
    ReturnPredictionResponse
)


router = APIRouter(
    prefix="/ml-predictions",
    tags=["ML Return Predictions"]
)


@router.get(
    "/{symbol}",
    response_model=ReturnPredictionResponse
)
def get_ml_stock_prediction(
    symbol: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    try:

        result = predict_stock_return(
            db=db,
            symbol=symbol
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except FileNotFoundError:

        raise HTTPException(
            status_code=503,
            detail="Prediction model is not available"
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
