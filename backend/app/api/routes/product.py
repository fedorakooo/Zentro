from fastapi import APIRouter

from app.core.schemas.products import Product
from app.services.product import get_product_by_id

router = APIRouter(tags=["Product"], prefix="/products")


@router.get("/{product_id}")
async def get_product(product_id: int) -> Product:
    product: Product = await get_product_by_id(product_id)
    return product
