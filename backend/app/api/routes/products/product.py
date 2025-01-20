from fastapi import APIRouter, Form
from fastapi.params import Depends

from app.core.schemas.cart import CartItemRequest
from app.core.schemas.products import Product, ProductCreate, ProductCreateDB
from app.core.schemas.users import User
from app.services.products.product import get_product_by_id, add_item_to_cart, add_new_product
from app.services.users.user import get_current_active_auth_user
from app.api.routes.products.reviews import router as reviews_router

router = APIRouter(tags=["Product"], prefix="/products")

router.include_router(reviews_router)


@router.get("/{product_id:int}")
async def get_product(product_id: int) -> Product:
    product: Product = await get_product_by_id(product_id)
    return product


@router.post("/{product_id:int}")
async def add_product_to_cart(
        product_id: int,
        quantity: int = Form(...),
        user: User = Depends(get_current_active_auth_user)
):
    cart_item: CartItemRequest = CartItemRequest(
        user_id=user.id,
        product_id=product_id,
        quantity=quantity
    )

    result = await add_item_to_cart(cart_item)

    return result

@router.post("/create")
async def create_product(product: ProductCreate, user: User = Depends(get_current_active_auth_user)):
    new_product: ProductCreateDB = ProductCreateDB(**product.dict(), seller_id=user.id)

    result = await add_new_product(new_product)

    return result