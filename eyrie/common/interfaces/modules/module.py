from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from eyrie.common.interfaces import MiddlewareConsumer


class EyrieModule(ABC):
    @abstractmethod
    def configure(self, consumer: MiddlewareConsumer):  # noqa: F841
        pass
