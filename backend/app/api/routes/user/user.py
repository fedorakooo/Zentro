from fastapi import APIRouter
from app.api.routes.user.cart import router as cart_router
from app.api.routes.user.products import router as products_router
from app.api.routes.user.profile import router as profile_router

router = APIRouter(tags=["User"], prefix="/user")

router.include_router(cart_router)
router.include_router(products_router)
router.include_router(profile_router)