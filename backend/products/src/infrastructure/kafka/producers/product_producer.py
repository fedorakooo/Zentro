import uuid
import time

from aiokafka import AIOKafkaProducer

from src.infrastructure.kafka.config.kafka import get_kafka_producer
from src.infrastructure.kafka.schemas.product_events import ProductEvent, ProductEventType

class ProductProducer:
    def __init__(self):
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        self.producer = await get_kafka_producer()
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_delete_event(self, product_id: str, original_status: str):
        event = ProductEvent(
            event_id=str(uuid.uuid4()),
            type=ProductEventType.DELETE,
            product_id=product_id,
            original_status=original_status,
            timestamp=int(time.time())
        )
        await self.producer.send("product_events", value=event.dict())

    async def send_compensation_event(self, product_id: str, original_status: str):
        event = ProductEvent(
            event_id=str(uuid.uuid4()),
            type=ProductEventType.DELETE_COMPENSATE,
            product_id=product_id,
            original_status=original_status,
            timestamp=int(time.time())
        )
        await self.producer.send("product_events", value=event.dict())