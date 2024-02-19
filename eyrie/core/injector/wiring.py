from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide as _Provide

from eyrie.core.utils import get_provider_token

if TYPE_CHECKING:
    from dependency_injector.providers import Provider
    from dependency_injector.wiring import Modifier


class Provide(_Provide):
    def __init__(
        self, provider: Provider | type, modifier: Modifier | None = None
    ) -> None:
        token = get_provider_token(provider)
        super().__init__(provider=token, modifier=modifier)
