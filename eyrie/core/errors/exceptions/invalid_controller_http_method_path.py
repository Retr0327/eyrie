from types import FunctionType

from eyrie.core.errors.messages import UNKNOWN_CONTROLLER_HTTP_METHOD_PATH

from .runtime import RuntimeException


class UnknownControllerHTTPMethodPathException(RuntimeException):
    def __init__(
        self, method: FunctionType | str, controller: type | FunctionType
    ) -> None:
        msg = UNKNOWN_CONTROLLER_HTTP_METHOD_PATH(method=method, controller=controller)
        super().__init__(msg=msg)
