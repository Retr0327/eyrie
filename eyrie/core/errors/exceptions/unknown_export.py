from eyrie.core.errors.messages import UNKNOWN_EXPORT_MESSAGE

from .runtime import RuntimeException


class UnknownExportException(RuntimeException):
    def __init__(self, provider: str | type, module: str | type) -> None:
        message = UNKNOWN_EXPORT_MESSAGE(cls=provider, module=module)
        super().__init__(msg=message)
