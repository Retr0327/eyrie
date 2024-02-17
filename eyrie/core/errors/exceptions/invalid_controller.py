from types import FunctionType

from eyrie.core.errors.messages import INVALID_CONTROLLER_MESSAGE

from .runtime import RuntimeException


class InvalidControllerException(RuntimeException):
    def __init__(self, controller: object | FunctionType) -> None:
        msg = INVALID_CONTROLLER_MESSAGE(controller)
        super().__init__(msg=msg)
