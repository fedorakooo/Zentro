from fastapi import APIRouter
from app.models import ProductsPublic

router = APIRouter(tags=["items"])

@router.get("/")
def read_items():
        return ProductsPublic(data=[], count=0)
