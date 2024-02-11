from typing import Callable

from typing_extensions import (
    Literal,
    NotRequired,
    TypedDict,
)

ProviderScope = Literal[
    "factory",
    "singleton",
    "container",
    "callable",
    "coroutine",
    "object",
    "list",
    "dict",
    "configuration",
    "resource",
    "aggregate",
    "selector",
    "dependency",
]


class ProviderConfig(TypedDict):
    """Interface defining a *Class* type provider."""

    provide: str | Callable | type
    """The injection token."""
    scope: ProviderScope
    """
    The scope of the injection token which determines the lifecycle of the provided
    instances. It should be one of the predefined scopes in `ProviderScope`. See
    more about scopes at
    [providers](https://python-dependency-injector.ets-labs.org/providers/index.html).
    """
    inject: NotRequired[list[str | Callable | type | dict]]
    """
    A list specifying dependencies to be injected into the provided instance.
    """


class ModuleMetadata(TypedDict):
    """Optional list of imported modules that export the providers which are
    required in this module.
    """

    imports: NotRequired[list[type | Callable | None]]
    """
    Optional list of imported modules that export the providers which are
    required in this module.
    """
    exports: NotRequired[list[type | Callable | ProviderConfig | None]]
    """
    Optional list of the subset of providers that are provided by this module and
    should be available in other modules which import this module.
    """
    providers: NotRequired[list[type | Callable | ProviderConfig | None]]
    """
    Optional list of providers that will be instantiated by the Nest injector and
    that may be shared at least across this module.
    """
    controllers: NotRequired[list[type | Callable | None]]
    """
    Optional list of controllers defined in this module which have to be
    instantiated.
    """
