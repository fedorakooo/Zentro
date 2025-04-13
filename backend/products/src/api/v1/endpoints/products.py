from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from src.containers.container import Container
from src.enums.product import ProductStatus
from src.schemas.products import ProductRead, ProductCreate, ProductUpdate
from src.application.abstractions.abstract_product_service import AbstractProductService
from src.schemas.saga import SagaResponse

router = APIRouter(prefix="/products", tags=["Products"])


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


@router.get("/", response_model=list[ProductRead])
@inject
async def get_products(
        name: str | None = None,
        brand: str | None = None,
        brand_id: int | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        skip: int = 0,
        limit: int = 100,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> list[ProductRead]:
    return await service.get_products(
        name=name,
        brand=brand,
        brand_id=brand_id,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit
    )

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_product(
        product_data: ProductCreate,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    return await service.create_product(product_data)


@router.put("/{product_id}", response_model=ProductRead)
@inject
async def update_product(
        product_id: str,
        product_data: ProductUpdate,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> ProductRead:
    updated = await service.update_product(product_id, product_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_202_ACCEPTED)
@inject
async def delete_product(
        product_id: str,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> SagaResponse:
    try:
        is_success = await service.delete_product(product_id)
        if not is_success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return SagaResponse(
            success=True,
            message="Product deletion in progress",
            compensation_data={"product_id": product_id}
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )


@router.post("/{product_id}/compensate", status_code=status.HTTP_200_OK)
@inject
async def compensate_delete_product(
        product_id: str,
        original_status: ProductStatus,
        service: AbstractProductService = Depends(Provide[Container.product_service])
) -> SagaResponse:
    await service.compensate_delete_product(product_id, original_status)
    return SagaResponse(
        success=True,
        message="Product delete compensation completed",
        compensation_data={"product_id": product_id}
    )
