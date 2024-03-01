import logging

from .exceptions import RuntimeException


class ExceptionHandler:
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

    def handle(self, exception: RuntimeException | Exception) -> None:
        if not isinstance(exception, RuntimeException):
            self.logger.error(msg=str(exception), exc_info=exception)
        else:
            self.logger.error(exception.what(), exc_info=exception)
