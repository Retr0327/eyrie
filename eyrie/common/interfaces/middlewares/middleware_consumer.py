from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
    Any,
)

if TYPE_CHECKING:
    from .middleware_config_proxy import MiddlewareConfigProxy


class MiddlewareConsumer(ABC):
    """Interface defining method for applying user defined middleware to routes."""

    @abstractmethod
    def apply(self, *middleware: Any) -> MiddlewareConfigProxy:  # noqa: F841
        pass
