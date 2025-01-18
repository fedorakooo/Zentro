from fastapi import APIRouter

from app.api.routes.user import profile, cart
from app.api.routes.products import items, product
from app.api.routes.auth import registration, auth

api_router = APIRouter()

api_router.include_router(items.router)
api_router.include_router(registration.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(product.router)
api_router.include_router(cart.router)
