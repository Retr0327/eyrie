from eyrie.core.errors.messages import USING_INVALID_CLASS_AS_A_MODULE_MESSAGE

from .runtime import RuntimeException


class InvalidClassModuleException(RuntimeException):
    def __init__(self, provider: str | type, module: str | type) -> None:
        msg = USING_INVALID_CLASS_AS_A_MODULE_MESSAGE(cls=provider, module=module)
        super().__init__(msg=msg)
