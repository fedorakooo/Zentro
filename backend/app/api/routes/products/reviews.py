from fastapi import APIRouter, Depends, Form
from pydantic import conint

from app.core.schemas.reviews import ReviewCreate
from app.core.schemas.users import User
from app.services.products.reviews import add_review_about_product
from app.services.user.user import get_current_active_auth_user

router = APIRouter(tags=["Reviews"])

@router.post("/{product_id:int}/add_review")
async def add_product_review(
        product_id: int,
        rating: conint(ge=1, le=5) = Form(...),
        comment: str = Form(...),
        user: User = Depends(get_current_active_auth_user)
):
    review = ReviewCreate(
        user_id=user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )

    result = await add_review_about_product(review)

    return result
