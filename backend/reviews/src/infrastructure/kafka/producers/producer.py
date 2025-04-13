import uuid
import time

from aiokafka import AIOKafkaProducer

from src.infrastructure.kafka.config.kafka import get_kafka_producer
from src.infrastructure.kafka.schemas.events import ReviewEvent, ReviewEventType

class Producer:
    def __init__(self):
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        self.producer = await get_kafka_producer()
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_delete_event(self, review_id: int, original_status: str):
        event = ReviewEvent(
            event_id=str(uuid.uuid4()),
            type=ReviewEventType.DELETE,
            review_id=review_id,
            original_status=original_status,
            timestamp=int(time.time())
        )
        await self.producer.send("review_events", value=event.dict())

    async def send_compensation_event(self, review_id: int):
        event = ReviewEvent(
            event_id=str(uuid.uuid4()),
            type=ReviewEventType.DELETE_COMPENSATE,
            review_id=review_id,
            timestamp=int(time.time())
        )
        await self.producer.send("review_events", value=event.dict())