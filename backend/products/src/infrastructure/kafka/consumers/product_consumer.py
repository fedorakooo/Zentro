from src.application.abstractions.abstract_product_service import AbstractProductService
from src.infrastructure.kafka.config.kafka import get_kafka_consumer
from src.infrastructure.kafka.schemas.product_events import ProductEvent, ProductEventType


class ProductConsumer:
    def __init__(self, product_service: AbstractProductService):
        self.consumer = None
        self.product_service = product_service

    async def start(self):
        self.consumer = await get_kafka_consumer()
        await self.consumer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume_events(self):
        try:
            async for msg in self.consumer:
                event = ProductEvent(**msg.value)

                if event.type == ProductEventType.DELETE_COMPENSATE:
                    await self.product_service.delete_product(
                        product_id=event.product_id
                    )

                if event.type == ProductEventType.DELETE_COMPENSATE:
                    await self.product_service.compensate_delete_product(
                        product_id=event.product_id,
                        original_status=event.original_status
                    )
        except Exception as exc:
            print(f"Kafka error: {exc}")
            raise