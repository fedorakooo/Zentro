from sqlalchemy.orm import Mapped

from src.models.base import Base
from src.enums.review_status import ReviewStatus


class ReviewORM(Base):
    __tablename__ = "reviews"

    user_id: Mapped[int]
    product_id: Mapped[str]
    rating: Mapped[int]
    comment: Mapped[str | None]
    status: Mapped[ReviewStatus]
