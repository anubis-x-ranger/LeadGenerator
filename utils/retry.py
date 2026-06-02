
import asyncio
from functools import wraps


def async_retry(
    retries: int = 3,
    delay: int = 2,
    exceptions: tuple = (Exception,)
):

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(retries):

                try:
                    return await func(*args, **kwargs)

                except exceptions as e:

                    last_exception = e

                    if attempt < retries - 1:

                        await asyncio.sleep(delay)

            raise last_exception

        return wrapper

    return decorator