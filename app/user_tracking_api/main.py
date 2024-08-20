from fastapi import APIRouter

from app.user_tracking_api.routes import tracking

api_router = APIRouter()
api_router.include_router(
    tracking.router, prefix="/tracking", tags=["tracking"]
)
