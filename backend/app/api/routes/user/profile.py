from fastapi import APIRouter
from fastapi.params import Depends

from app.core.schemas.users import User
from app.services.user.user import get_current_active_auth_user
from app.api.routes.user.cart import router as cart_router
from app.api.routes.user.products import router as products_router

router = APIRouter(tags=["Profile"], prefix="/user")

router.include_router(cart_router)
router.include_router(products_router)


@router.get("/", response_model=User)
async def get_user_profile(user: User = Depends(get_current_active_auth_user)):
    return user
