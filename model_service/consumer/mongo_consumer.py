from motor.motor_asyncio import AsyncIOMotorClient
from consumer.consumer import Consumer
from consumer.utils import retry_on_failure


class MongoDBConsumer(Consumer):
    """
    MongoDB Consumer that connects to a MongoDB database and consumes data.
    """

    def __init__(self, uri, db_name, collection_name, batch_size=20):
        """
        Initialize the MongoDB Consumer.

        Args:
            uri: MongoDB connection URI.
            db_name: MongoDB database name.
            collection_name: MongoDB collection name.
            batch_size: Number of documents to fetch in a single batch.
        """
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.client = None
        self.mongo_db = None
        self.mongo_collection = None

    @retry_on_failure(max_retries=5, delay=1, backoff=2)
    async def connect(self) -> None:
        """
        Connect to the MongoDB database with retry mechanism.
        """
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.client.admin.command("ping")
            self.mongo_db = self.client[self.db_name]
            self.mongo_collection = self.mongo_db[self.collection_name]
            print(f"Connected to MongoDB database: {self.db_name}, collection: {self.collection_name}")
        except Exception as e:
            print("Connection failed. Retrying...")
            raise e

    async def disconnect(self) -> None:
        """
        Disconnect from the MongoDB database.
        """
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    async def consume(self):
        """
        Consume data from the MongoDB collection.
        """
        try:
            async for document in self.mongo_collection.find():
                yield document
        except Exception as e:
            print(f"Error during data consumption: {e}")
