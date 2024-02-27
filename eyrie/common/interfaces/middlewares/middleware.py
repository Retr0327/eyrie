from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:
    from starlette.middleware.base import (
        RequestResponseEndpoint,
        _CachedRequest,
    )
    from starlette.types import ASGIApp


class EyrieGlobalMiddleware(ABC, BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, *args, **kwargs) -> None:
        super().__init__(app, *args, **kwargs)

    @abstractmethod
    async def dispatch(
        self, request: _CachedRequest, call_next: RequestResponseEndpoint  # noqa: F841
    ):
        pass


class EyrieMiddleware(ABC):
    pass
