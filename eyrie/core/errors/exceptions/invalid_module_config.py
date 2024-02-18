from eyrie.core.errors.messages import INVALID_MODULE_CONFIG_MESSAGE

from .runtime import RuntimeException


class InvalidModuleConfigException(RuntimeException):
    def __init__(self, module_key: str) -> None:
        msg = INVALID_MODULE_CONFIG_MESSAGE(module_key=module_key)
        super().__init__(msg=msg)
