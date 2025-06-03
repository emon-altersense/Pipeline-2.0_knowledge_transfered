from confluent_kafka import Consumer as KafkaConsumerClient, cimpl
from consumer import Consumer


class KafkaConsumer(Consumer):
    """
    Kafka Consumer implementation.
    """

    def __init__(self, topic, config) -> None:
        """
        Initialize the Kafka Consumer.

        Args:
            topic: The Kafka topic to consume messages from.
            config: The Kafka configuration.
        """
        self.topic = topic
        self.consumer = None
        self.config = config

    def connect(self) -> None:
        """
        Connect to the Kafka topic.
        """
        self.consumer = KafkaConsumerClient(self.config)
        self.consumer.subscribe([self.topic])
        print(f"Connected to Kafka topic: {self.topic}")

    async def consume(self) -> None:
        """
        Consume messages from the Kafka topic.
        """
        if not self.consumer:
            raise Exception("Consumer not connected. Call 'connect()' first.")

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None or msg.key() is None or msg.value() is None:
                    continue

                yield msg, msg.key(), msg.value(), msg.timestamp()

        except Exception as e:
            print(f"Error during message consumption: {e}")

    async def commit_offsets(self, msg: cimpl.Message) -> None:
        """
        Commit the offsets for the consumed messages.

        Args:
            msg: The message to commit the offset for.
        """
        if self.consumer is not None:
            self.consumer.commit(message=msg)

    def disconnect(self) -> None:
        """
        Disconnect from the Kafka topic.
        """
        if self.consumer is not None:
            self.consumer.close()
            self.consumer = None
            print(f"Disconnected from Kafka topic: {self.topic}")
