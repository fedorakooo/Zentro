from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from src.containers import Container
from src.schemas.products import ProductRead, ProductCreate, ProductUpdate
from src.application.abstractions.abstract_product_service import AbstractProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductRead])
@inject
async def list_products(
        skip: int = 0,
        limit: int = 100,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> list[ProductRead]:
    return await service.search_products(skip=skip, limit=limit)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_product(
        product_data: ProductCreate,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    return await service.create_product(product_data)


@router.get("/{product_id}", response_model=ProductRead)
@inject
async def get_product(
        product_id: str,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.put("/{product_id}", response_model=ProductRead)
@inject
async def update_product(
        product_id: str,
        product_data: ProductUpdate,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    updated = await service.update_product(product_id, product_data, partial=False)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated


@router.patch("/{product_id}", response_model=ProductRead)
@inject
async def partial_update_product(
        product_id: str,
        product_data: ProductUpdate,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    updated = await service.update_product(product_id, product_data, partial=True)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_product(
        product_id: str,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> None:
    success = await service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@router.get("/search", response_model=list[ProductRead])
@inject
async def search_products(
        name: str | None = None,
        brand: str | None = None,
        brand_id: int | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        skip: int = 0,
        limit: int = 100,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    return await service.search_products(
        name=name,
        brand=brand,
        brand_id=brand_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit
    )


@router.get("/count", response_model=int)
@inject
async def count_products(
        name: str | None = None,
        brand: str | None = None,
        brand_id: int | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    return await service.count_products(
        name=name,
        brand=brand,
        brand_id=brand_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price
    )
