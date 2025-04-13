from fastapi import HTTPException, status


class HttpInvalidProductIdError(HTTPException):
    def __init__(self, product_id: str):
        detail = f"Invalid product ID format: '{product_id}'. Must be a 24-character hex string"
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class HttpProductNotFoundError(HTTPException):
    def __init__(self, product_id: str):
        detail = f"Product with ID '{product_id}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
