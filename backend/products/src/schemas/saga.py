from pydantic import BaseModel


class SagaResponse(BaseModel):
    success: bool
    message: str
    compensation_data: dict | None = None
