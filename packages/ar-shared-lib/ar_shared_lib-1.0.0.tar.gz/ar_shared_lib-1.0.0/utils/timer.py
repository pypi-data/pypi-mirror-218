import logging
import timeit
import functools
from typing import Optional

logger = logging.getLogger(__name__)


def timer(
    number_of_iterations: Optional[int] = 1_000,
    logger: Optional[logging.Logger] = logger,
):
    """Decorator to measure execution time of a function"""

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            execution_time = timeit.timeit(
                lambda: func(*args, **kwargs),
                number=number_of_iterations,
            )

            logger.info(
                f"Function {func.__name__} executed {number_of_iterations} times, "
                f"in {execution_time} seconds"
            )

            return func(*args, **kwargs)
        return wrapper
    return decorator
