from elasticsearch import AsyncElasticsearch

from src.config import settings
from src.infrastructure.elasticsearch.mappings.product import PRODUCT_INDEX_MAPPING


class ElasticSearchClient:
    def __init__(self):
        self.client: AsyncElasticsearch | None = None
        self.host = settings.elasticsearch.host
        self.request_timeout = settings.elasticsearch.request_timeout

    async def connect(self) -> AsyncElasticsearch:
        try:
            self.client = AsyncElasticsearch(
                hosts=self.host,
                request_timeout=self.request_timeout
            )
            if not await self.client.indices.exists(index=settings.elasticsearch.product_index):
                response = await self.client.indices.create(
                    index=settings.elasticsearch.product_index,
                    body=PRODUCT_INDEX_MAPPING
                )
            return self.client
        except Exception as exc:
            raise

    async def close(self) -> None:
        if self.client:
            await self.client.close()

    async def is_healthy(self) -> bool:
        return await self.client.ping() if self.client else False
