import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from src.config import settings


async def get_kafka_producer() -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=settings.kafka.boostrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


async def get_kafka_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        settings.kafka.topic_review_event,
        bootstrap_servers=settings.kafka.boostrap_servers,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="product-service-group"
    )