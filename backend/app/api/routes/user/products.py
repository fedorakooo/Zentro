from fastapi import APIRouter, Depends
from typing import List

from app.core.schemas.products import Product
from app.core.schemas.users import User
from app.services.user.user import check_seller_permissions
from app.services.user.products import get_created_products_by_user_id

router = APIRouter(tags=["Products"], prefix="/products")


@router.get("/created", response_model=List[Product])
async def get_created_products(user: User = Depends(check_seller_permissions)):
    products: List[Product] = await get_created_products_by_user_id(user.id)
    return products
