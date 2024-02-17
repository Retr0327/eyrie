from dataclasses import (
    dataclass,
    field,
)
from typing import Callable

from eyrie.core.errors.exceptions import CircularDependencyException


@dataclass(slots=True)
class GraphInspector:
    providers: dict[str, list[type | Callable]] = field(default_factory=dict)

    def add_provider(self, provider: type | Callable):
        if provider not in self.providers:
            self.providers[provider] = []

    def add_dep(self, provider: type | Callable, dep: type | Callable):
        if provider not in self.providers:
            self.add_provider(provider)

        if dep not in self.providers[provider]:
            self.add_provider(dep)

        self.providers[provider].append(dep)

    def _resolve_provider(
        self,
        provider: type | Callable,
        resolved: list[type | Callable],
        unresolved: list[type | Callable],
    ):
        unresolved.append(provider)
        for dep in self.providers[provider]:
            if dep not in resolved:
                if dep in unresolved:
                    raise CircularDependencyException(provider=provider, dep=dep)
                self._resolve_provider(dep, resolved, unresolved)

        if provider not in resolved:
            resolved.append(provider)

        unresolved.remove(provider)

    def resolve_providers(self) -> list[type | Callable]:
        resolved, unresolved = [], []
        for provider in self.providers.keys():
            if provider not in unresolved:
                self._resolve_provider(provider, resolved, unresolved)
        return resolved
