from pydantic import BaseModel


class CategoryCreate(BaseModel):
    id: int
    name: str
    query: str | None = None
    parent_id: int | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None
    query: str | None = None


class CategoryRead(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    query: str | None = None
