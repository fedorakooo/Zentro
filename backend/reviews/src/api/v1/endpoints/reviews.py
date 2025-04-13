from fastapi import APIRouter, Depends, status, HTTPException
from dependency_injector.wiring import inject, Provide

from src.application.abstractions.abstract_review_service import AbstractReviewService
from src.containers.container import Container
from src.enums.review_status import ReviewStatus
from src.schemas.review import ReviewRead, ReviewCreate
from src.schemas.saga import SagaResponse

router = APIRouter(prefix="/products/{product_id}/reviews", tags=["Reviews"])


@router.get("/", response_model=list[ReviewRead])
@inject
async def get_product_reviews(
        product_id: str,
        rating: int | None = None,
        skip: int = 0,
        limit: int = 100,
        service: AbstractReviewService = Depends(Provide[Container.review_service])
) -> list[ReviewRead]:
    return await service.get_product_reviews(
        product_id=product_id,
        rating=rating,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_product_review(
        product_id: str,
        review_data: ReviewCreate,
        user_id: int,  # В реальном проекте лучше получать из аутентификации
        service: AbstractReviewService = Depends(Provide[Container.review_service])
) -> ReviewRead:
    return await service.create_review(review_data, user_id, product_id)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_product_review(
        product_id: str,
        review_id: int,
        service: AbstractReviewService = Depends(Provide[Container.review_service])
):
    try:
        await service.delete_review_by_id(review_id)
    except HTTPException:
        raise


@router.post("/{review_id}/compensate", status_code=status.HTTP_200_OK)
@inject
async def compensate_delete_product(
        product_id: str,
        review_id: int,
        original_status: ReviewStatus,
        service: AbstractReviewService = Depends(Provide[Container.review_service])
) -> SagaResponse:
    return await service.compensate_delete_review(review_id, original_status)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_all_reviews_by_product(
        product_id: str,
        service: AbstractReviewService = Depends(Provide[Container.review_service])
):
    await service.delete_all_reviews_by_product_id(product_id)