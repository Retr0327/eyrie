from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import FunctionType

    from eyrie.common.interfaces.modules import ProviderConfig


def get_provider_token(provider: str | type | FunctionType | ProviderConfig):
    """The get_provider_token function returns a token that represents a provider."""

    if isinstance(provider, str):
        return provider
    elif isinstance(provider, dict):
        provide = provider.get("provide")
        if isinstance(provide, str):
            return provide
        provider_cls = provider.get("inject", [provide])[0]
    else:
        provider_cls = provider

    token = f"{provider_cls.__module__}.{provider_cls.__qualname__}"
    return token.replace(".", "_")
