import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class ProductBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2048)

# Database model, database table inferred from class name
class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)


# Properties to return via API, id is always required
class ProductPublic(ProductBase):
    id: uuid.UUID


class ProductsPublic(SQLModel):
    data: list[ProductPublic]
    count: int