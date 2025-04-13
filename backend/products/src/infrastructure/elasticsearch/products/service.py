from src.config import settings
from src.infrastructure.elasticsearch.client import ElasticSearchClient


class ElasticProductService:
    def __init__(self, client: ElasticSearchClient):
        self.client = client

    async def create_product(self, product_id: str, product: dict) -> bool:

        await self.client.client.index(
            index=settings.elasticsearch.product_index,
            document=product,
            id=product_id
        )
        return True

    async def delete_product(self, product_id: str) -> bool:
        await self.client.client.delete(index=settings.elasticsearch.product_index, id=product_id)
        return True

    async def update_product(self, product_id: str, product: dict) -> bool:
        await self.client.client.update(
            index=settings.elasticsearch.product_index,
            id=product_id,
            doc={"doc": product}
        )
        return True

    async def get_products(
            self,
            name: str | None = None,
            brand: str | None = None,
            brand_id: int | None = None,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[str]:
        must_clauses = []

        if name:
            must_clauses.append({
                "bool": {
                    "should": [
                        {"match_phrase": {"name": {"query": name, "boost": 3}}},

                        {"match": {"name": {"query": name, "fuzziness": "AUTO"}}},

                        {"match": {"name": {"query": name, "analyzer": "russian"}}}
                    ],
                    "minimum_should_match": 1
                }
            })

        if brand:
            must_clauses.append({
                "match": {"brand": {"query": brand, "operator": "and"}}
            })

        if brand_id:
            must_clauses.append({
                "term": {"brand_id": brand_id}
            })

        if category_id:
            must_clauses.append({
                "term": {"category_id": category_id}
            })

        if min_price is not None or max_price is not None:
            price_range = {}
            if min_price is not None:
                price_range["gte"] = min_price
            if max_price is not None:
                price_range["lte"] = max_price
            must_clauses.append({
                "range": {"price": price_range}
            })

        query_body = {
            "query": {
                "bool": {
                    "must": must_clauses if must_clauses else [{"match_all": {}}]
                }
            },
            "from": skip,
            "size": limit,
            "_source": False
        }

        response = await self.client.client.search(
            index=settings.elasticsearch.product_index,
            body=query_body
        )

        return [hit["_id"] for hit in response["hits"]["hits"]]