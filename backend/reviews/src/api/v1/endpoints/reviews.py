from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from src.application.abstractions.abstract_review_service import AbstractReviewService
from src.containers.container import Container
from src.schemas.review import ReviewRead, ReviewCreate

router = APIRouter()


@router.get("/products/{product_id}/reviews", response_model=list[ReviewRead])
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


@router.post("/products/{product_id}/reviews", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
@inject
async def create_product_review(
        user_id: int,
        product_id: str,
        review_data: ReviewCreate,
        service: AbstractReviewService = Depends(Provide[Container.review_service])
) -> ReviewRead:
    return await service.create(review_data, user_id, product_id)
