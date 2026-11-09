from fastapi import APIRouter

from app.api.v1.endpoints import health, stocks, users, auth


api_router = APIRouter()


api_router.include_router(
    health.router,
    tags=["Health"]
)

api_router.include_router(
    stocks.router
)

api_router.include_router(
    users.router
)

api_router.include_router(auth.router)