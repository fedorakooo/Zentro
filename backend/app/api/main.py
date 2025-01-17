from fastapi import APIRouter

from app.api.routes import auth, user
from app.api.routes.products import items, product
from app.api.routes.auth import registration

api_router = APIRouter()

api_router.include_router(items.router)
api_router.include_router(registration.router)
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(product.router)
