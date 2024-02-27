from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .middleware_configuration import RouteInfo
    from .middleware_consumer import MiddlewareConsumer


class MiddlewareConfigProxy(ABC):
    @abstractmethod
    def exclude(self, *routes: str | RouteInfo) -> MiddlewareConfigProxy:  # noqa: F841
        """Excludes routes from the currently processed middleware."""

    @abstractmethod
    def for_routes(self, *routes: str | RouteInfo) -> MiddlewareConsumer:  # noqa: F841
        """Attaches passed routes to the currently configured middleware."""
