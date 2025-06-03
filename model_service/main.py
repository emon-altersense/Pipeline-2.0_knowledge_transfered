import asyncio
import time
import numpy as np
import torch
from consumer import MongoDBConsumer
from ultralytics import YOLO

model = YOLO("person_best_model.pt")


async def main():
    frames = []
    consumer = MongoDBConsumer(
        uri="mongodb://localhost:27017",
        db_name="activity_detection",
        collection_name="activity_data"
    )
    await consumer.connect()

    async for document in consumer.consume():
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(document["timestamp"] // 1000)))

        frame = np.frombuffer(document["frame"][0], dtype=document["frame_dtype"]).reshape(document["frame_shape"])

        frame = torch.from_numpy(frame.copy()).to(torch.device("cuda"), non_blocking=True).unsqueeze(0).float() / 255
        frames.append(frame)

    start_time = time.time()

    for f in frames:
        model.predict(f, conf=0.5)

    print(f"{time.time() - start_time:0.5f} seconds")

    await consumer.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
