import asyncio
from consumer import KafkaConsumer
from pipeline import activity_detection_pipeline
from preprocess.object_detection import YOLOv8Preprocessor
from producer import MongoDBProducer


async def main():
    _preprocessor_class = YOLOv8Preprocessor()  # YOLOv8Preprocessor
    kafka_config = {
        "bootstrap.servers": "127.0.0.1:9094",
        "group.id": "activity_detection_group",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }

    _consumer_client = KafkaConsumer(topic="activity_detection", config=kafka_config)
    _consumer_client.connect()

    _producer_client = MongoDBProducer(
        uri="mongodb://localhost:27017/",
        db_name="activity_detection",
        collection_name="activity_data",
    )
    await _producer_client.connect()

    await activity_detection_pipeline(
        consumer_client=_consumer_client,
        preprocessor_class=_preprocessor_class,
        producer_client=_producer_client,
    )


if __name__ == "__main__":
    asyncio.run(main())
