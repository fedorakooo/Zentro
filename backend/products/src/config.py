class MongoSettings:
    url: str = "mongodb://localhost:27017"
    db_name: str = "products_db"


class KafkaSettings:
    boostrap_servers: str = "localhost:29092"
    topic_product_event: str = "product_events"
    topic_review_evenv: str = "review_event"


class Settings:
    mongo: MongoSettings = MongoSettings()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
