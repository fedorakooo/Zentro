from src.application.abstractions.abstract_review_service import AbstractReviewService
from src.infrastructure.kafka.config.kafka import get_kafka_consumer
from src.infrastructure.kafka.schemas.events import ReviewEvent, ReviewEventType


class Consumer:
    def __init__(self, review_service: AbstractReviewService):
        self.consumer = None
        self.review_service = review_service

    async def start(self):
        self.consumer = await get_kafka_consumer()
        await self.consumer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume_events(self):
        try:
            async for msg in self.consumer:
                event = ReviewEvent(**msg.value)

                if event.type == ReviewEventType.DELETE_COMPENSATE:
                    await self.review_service.delete_review(
                        review_id=event.review_id
                    )

                if event.type == ReviewEventType.DELETE_COMPENSATE:
                    await self.review_service.compensate_delete_review(
                        review_id=event.review_id,
                        original_status=event.original_status
                    )
        except Exception as exc:
            print(f"Kafka error: {exc}")
            raise
