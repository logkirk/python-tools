from typing import Callable
from datetime import datetime
from functools import wraps


def retry_on_exception(*exceptions, timeout=60) -> Callable:
    """Decorator which retries the decorated function on any of specified exceptions up
    to specified timeout.

    Note: Must use Callable type hint to get PyCharm argument popups to work for
        decorated functions

    Examples:
        @retry_on_exception(TypeError)
        @retry_on_exception(TypeError, RuntimeError)
        @retry_on_exception(TypeError, RuntimeError, timeout=5)

    Args:
        exceptions: exceptions to catch
        timeout (int): how long to retry

    Raises:
        TimeoutError if timeout expired before function was successfully completed.
    """

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            last_exc = None
            while True:
                if (datetime.now() - start_time).total_seconds() > timeout:
                    raise TimeoutError(
                        "Timeout expired after {} second(s) trying to perform function "
                        '"{}".'.format(timeout, func.__name__)
                    ) from last_exc
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    continue

        return wrapper

    return _decorator
