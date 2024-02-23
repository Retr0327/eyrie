from eyrie.core.errors.messages import UNKNOWN_DEPENDENCIES_MESSAGE

from .runtime import RuntimeException


class UndefinedDependencyException(RuntimeException):
    def __init__(
        self, dep: str | type, module: str | type, dep_context: str | type
    ) -> None:
        message = UNKNOWN_DEPENDENCIES_MESSAGE(
            dep=dep, module=module, dep_context=dep_context
        )
        super().__init__(msg=message)
