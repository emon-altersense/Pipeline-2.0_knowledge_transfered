import time
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError, ExecutionTimeout
from producer import Producer, retry_on_failure


class MongoDBProducer(Producer):
    """
    MongoDB Producer that connects to a MongoDB database and produces data.
    """

    def __init__(self, uri, db_name, collection_name, batch_size=20, time_interval=5):
        """
        Initialize the MongoDB Producer

        Args:
            uri: The MongoDB URI.
            db_name: The MongoDB database name.
            collection_name: The MongoDB collection name.
            batch_size: The number of documents to batch insert.
            time_interval: The time interval in seconds to flush the batch.
        """
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.time_interval = time_interval
        self.client = None
        self.mongo_db = None
        self.mongo_collection = None
        self.batch = []
        self.last_flush_time = time.time()
        self.batch_lock = asyncio.Lock()

    @retry_on_failure(max_retries=5, delay=1, backoff=2)
    async def connect(self):
        """
        Connect to the MongoDB database with retry mechanism.
        """
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.client.admin.command("ping")
            self.mongo_db = self.client[self.db_name]
            self.mongo_collection = self.mongo_db[self.collection_name]
            print(f"Connected to MongoDB database: {self.db_name}, collection: {self.collection_name}")
            await self.create_indexes()

        except Exception as e:
            print("Connection failed. Retrying...")
            raise e

    async def reconnect(self):
        """
        Attempt to reconnect to the MongoDB database if disconnected.
        """
        print("Attempting to reconnect...")
        await self.connect()

    async def disconnect(self):
        """
        Disconnect from the MongoDB database.
        """
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")

    async def create_indexes(self):
        """
        Create indexes on the MongoDB collection for faster querying.
        """
        await self.mongo_collection.create_index([("camera_id", 1), ("timestamp", 1)])

    async def produce(self, data):
        """
        Adds data to the batch and saves it when batch size is reached or time interval expires.

        Args:
            data: The data to be added to the batch.
        """
        async with self.batch_lock:
            self.batch.append(data)

        # Outer block ensures no DEADLOCK
        await self._flush_batch()

    async def _flush_batch(self):
        """
        Flushes the current batch to the MongoDB collection.
        """
        async with self.batch_lock:
            if not self.batch:
                return

            # Make a copy of the batch to avoid mutation issues
            batch_to_insert = self.batch.copy()
            self.batch.clear()
            self.last_flush_time = time.time()

        try:
            await self.mongo_collection.insert_many(batch_to_insert)
        except (ServerSelectionTimeoutError, ExecutionTimeout) as e:
            print(f"Timeout occurred: {e}. Retrying...")
            await self.reconnect()
            # Retry inserting the batch after reconnecting
            await self._retry_flush(batch_to_insert)

        except Exception as e:
            print(f"Error inserting batch: {e}. Reconnecting and retrying...")
            await self.reconnect()
            await self._retry_flush(batch_to_insert)

    async def _retry_flush(self, batch, max_retries=10):
        """
        Retry flushing a batch after a reconnect attempt.

        Args:
            batch (list): The batch of data to retry inserting.
            max_retries (int): Maximum number of retry attempts.
        """
        print("Retrying to insert batch after reconnect...")
        for attempt in range(max_retries):
            try:
                await self._flush_batch()
                return
            except Exception as e:
                print(f"Retry {attempt + 1} failed: {e}")
                await asyncio.sleep(1)  # Backoff delay
        print(f"Failed to insert batch after {max_retries} retries. Saving for later retry.")
