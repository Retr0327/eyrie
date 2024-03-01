import sys
from typing import Callable

from .exception_handler import ExceptionHandler


def tear_down(error: Exception = None):
    return sys.exit(1)


class ExceptionsZone:
    exception_handler = ExceptionHandler()

    @classmethod
    def run(cls, callback: Callable, tear_down: Callable = tear_down) -> None:
        try:
            callback()
        except Exception as error:
            cls.exception_handler.handle(error)
            tear_down(error)

    @classmethod
    async def async_run(
        cls, callback: Callable, tear_down: Callable = tear_down
    ) -> None:
        try:
            await callback()
        except Exception as error:
            cls.exception_handler.handle(error)
            tear_down(error)
