from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db


router = APIRouter()


@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "application": "FinSight AI",
        "message": "Backend is running successfully"
    }


@router.get("/health/db")
def database_health(db: Session = Depends(get_db)):

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except SQLAlchemyError as exc:

        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        ) from exc