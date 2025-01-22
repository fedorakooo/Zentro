from typing import List

from fastapi import APIRouter, Depends

from app.core.schemas.cart import CartItem
from app.core.schemas.users import User
from app.services.user.cart import get_cart_products_by_user_id
from app.services.user.user import get_current_active_auth_user

router = APIRouter(tags=["Cart"], prefix="/cart")


@router.get("/", response_model=List[CartItem])
async def get_user_cart(user: User = Depends(get_current_active_auth_user)):
    products_cart_item = await get_cart_products_by_user_id(user.id)
    return products_cart_item
