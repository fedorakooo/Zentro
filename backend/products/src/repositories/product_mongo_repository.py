from beanie import PydanticObjectId

from src.models.product import Product
from src.repositories.abstract_product_mongo_repo import AbstractProductMongoRepository


class ProductMongoRepository(AbstractProductMongoRepository):
    async def get_by_id(self, product_id: str) -> Product | None:
        product_id = PydanticObjectId(product_id)
        return await Product.find_one({"_id": product_id})

    async def get_by_ids(self, product_ids: list[str]) -> list[Product]:
        product_ids = [PydanticObjectId(pid) for pid in product_ids]
        return await Product.find({"_id": {"$in": product_ids}}).to_list()

    async def create(self, product: Product) -> Product:
        await product.create()
        return product

    async def update(self, product_id: str, update_data: dict) -> Product | None:
        product_id = PydanticObjectId(product_id)
        product = await self.get_by_id(product_id)
        if product is None:
            return None

        await product.update({"$set": update_data})
        return await self.get_by_id(product_id)

    async def delete(self, product_id: str) -> bool:
        product = await self.get_by_id(product_id)
        if product is None:
            return False
        await product.delete()
        return True

    async def search(
            self,
            name: str | None = None,
            brand: str | None = None,
            brand_id: int | None = None,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[Product]:

        query = {}
        if name:
            query["$text"] = {"$search": name}
        if brand:
            query["brand"] = brand
        if brand_id is not None:
            query["brand_id"] = brand_id
        if category_id is not None:
            query["category_id"] = category_id
        if min_price is not None or max_price is not None:
            price_query = {}
            if min_price is not None:
                price_query["$gte"] = min_price
            if max_price is not None:
                price_query["$lte"] = max_price
            query["price"] = price_query

        return await Product.find(query).skip(skip).limit(limit).to_list()

    async def count(
            self,
            name: str | None = None,
            brand: str | None = None,
            brand_id: int | None = None,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None
    ) -> int:

        query = {}
        if name:
            query["$text"] = {"$search": name}
        if brand:
            query["brand"] = brand
        if brand_id is not None:
            query["brand_id"] = brand_id
        if category_id is not None:
            query["category_id"] = category_id
        if min_price is not None or max_price is not None:
            price_query = {}
            if min_price is not None:
                price_query["$gte"] = min_price
            if max_price is not None:
                price_query["$lte"] = max_price
            query["price"] = price_query

        return await Product.find(query).count()
