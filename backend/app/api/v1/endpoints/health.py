from fastapi import APIRouter


router = APIRouter()

@router.get("/health" )
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "healthy",
            "application": "FinSight-AI",
            "message": "The API is up and running!"
            }