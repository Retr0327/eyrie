from eyrie.core.errors.messages import INVALID_MODULE_TYPE_MESSAGE

from .runtime import RuntimeException


class InvalidModuleTypeException(RuntimeException):
    def __init__(self, module: str | type) -> None:
        msg = INVALID_MODULE_TYPE_MESSAGE(module=module)
        super().__init__(msg=msg)
