from typing import Callable

from eyrie.core.errors.messages import CIRCULAR_DEPENDENCY_MESSAGE

from .runtime import RuntimeException


class CircularDependencyException(RuntimeException):
    def __init__(
        self, provider: str | type | Callable, dep: str | type | Callable
    ) -> None:
        msg = CIRCULAR_DEPENDENCY_MESSAGE(provider=provider, dep=dep)
        super().__init__(msg=msg)
