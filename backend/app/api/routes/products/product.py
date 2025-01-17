from fastapi import APIRouter
from fastapi.params import Depends

from app.core.schemas.cart import CartItemRequest
from app.core.schemas.products import Product
from app.core.schemas.users import User
from app.services.products.product import get_product_by_id, add_item_to_cart
from app.services.users.user import get_current_active_auth_user

router = APIRouter(tags=["Product"], prefix="/products")


@router.get("/{product_id}")
async def get_product(product_id: int) -> Product:
    product: Product = await get_product_by_id(product_id)
    return product


@router.post("/{product_id}")
async def add_product_to_cart(
        product_id: int,
        quantity: int,
        user: User = Depends(get_current_active_auth_user)
):
    cart_item: CartItemRequest = CartItemRequest(
        user_id=user.id,
        product_id=product_id,
        quantity=quantity)
    result = await add_item_to_cart(cart_item)
    return result
