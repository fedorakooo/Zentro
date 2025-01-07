from fastapi import APIRouter

from app.api.routes import items, registration, auth

api_router = APIRouter()

api_router.include_router(items.router)
api_router.include_router(registration.router)
api_router.include_router(auth.router)
