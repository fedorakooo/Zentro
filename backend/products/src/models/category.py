from beanie import Document, Indexed


class Category(Document):
    id: Indexed(int, unique=True)
    name: str
    parent_id: int | None = None
    query: str | None = None

    class Settings:
        name = "categories"
        indexes = [
            "parent_id"
        ]