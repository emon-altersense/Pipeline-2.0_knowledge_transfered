import asyncio
from functools import wraps


def retry_on_failure(max_retries=5, delay=1, backoff=2):
    """
    A decorator that retries a function upon failure with an exponential backoff strategy.

    Args:
        max_retries (int): Maximum number of retries before giving up.
        delay (int or float): Initial delay in seconds before retrying.
        backoff (int or float): Factor by which the delay increases after each failure.

    Returns:
        function: The wrapped function with retry logic.

    Raises:
        Exception: If the function fails after the maximum number of retries.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f"Error: {e}. Retrying {retries}/{max_retries} in {current_delay} seconds...")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            raise Exception(f"Failed after {max_retries} retries")

        return wrapper

    return decorator
