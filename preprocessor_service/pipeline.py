import asyncio
from dask.distributed import Client


async def dask_process_task(preprocessor_class, message):
    """
    Dask task function to process data in parallel.

    Args:
        preprocessor_class: The preprocessor class to handle the task_type.
        message: The data to be processed.

    Returns:
        dict: Processed data.
    """
    preprocessor = preprocessor_class
    result_ = await preprocessor.preprocess(data=message)
    return result_


async def activity_detection_pipeline(
    consumer_client, preprocessor_class, producer_client
):
    """
    Pipeline to consume data from Kafka, process it using Dask, and produce it to MongoDB.

    Args:
        consumer_client: The Kafka consumer client.
        preprocessor_class: The preprocessor class to handle the task_type.
        producer_client: The MongoDB producer client.
    """
    dask_client = Client(n_workers=8)
    print("Dask Client started:", dask_client)

    try:
        async for msg, *message in consumer_client.consume():
            future = dask_client.submit(dask_process_task, preprocessor_class, message)
            processed_data = future.result()
            await producer_client.produce(processed_data)
            await consumer_client.commit_offsets(msg=msg)

    except asyncio.CancelledError:
        print("Pipeline interrupted.")

    except Exception as e:
        print(f"Pipeline error: {e}")

    finally:
        dask_client.close()
