from types import FunctionType

from eyrie.core.errors.messages import INVALID_CONTROLLER_HTTP_METHOD_MESSAGE

from .runtime import RuntimeException


class InvalidControllerHTTPMethodException(RuntimeException):
    def __init__(self, method: str, controller: type | FunctionType) -> None:
        msg = INVALID_CONTROLLER_HTTP_METHOD_MESSAGE(
            method=method, controller=controller
        )
        super().__init__(msg=msg)
