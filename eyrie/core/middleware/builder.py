from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import TYPE_CHECKING

from eyrie.common.interfaces.middlewares import MiddlewareConsumer

from .proxy import ConfigProxy

if TYPE_CHECKING:
    from eyrie.common.interfaces import (
        EyrieMiddleware,
        MiddlewareConfigProxy,
    )


@dataclass(slots=True)
class MiddlewareBuilder(MiddlewareConsumer):
    middleware_collection: list = field(default_factory=list)

    def apply(self, *middleware: EyrieMiddleware) -> MiddlewareConfigProxy:
        return ConfigProxy(builder=self, middlewares=middleware)

    def build(self):
        return list(self.middleware_collection)
