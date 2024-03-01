from dataclasses import dataclass
import inspect
from types import FunctionType
from typing import TypeVar

from fastapi.routing import APIRouter

from eyrie.common.constants import (
    HTTP_METHODS,
    MetaData,
)
from eyrie.core.errors import (
    ExceptionsZone,
    InvalidControllerHTTPMethodException,
    UnknownControllerHTTPMethodPathException,
)

from .proxy import RouterProxy

T = TypeVar("T")


@dataclass(slots=True)
class RouterFactory:
    controller: type[T]

    def _check_controller_method(self, method: FunctionType):
        if not hasattr(method, MetaData.REQUEST_METHOD_PATH):
            raise UnknownControllerHTTPMethodPathException(
                method=method, controller=self.controller
            )

        if method.method not in HTTP_METHODS:
            raise InvalidControllerHTTPMethodException(
                method=method.method, controller=self.controller
            )

    def _sanitize_path(self, prefix: str | None, path: str):
        combined_path = f"{prefix}{path}" if prefix else path
        if not combined_path.startswith("/"):
            return f"/{combined_path}"
        elif combined_path.endswith("/"):
            return combined_path[:-1]
        else:
            return combined_path

    def create(self) -> type[T]:
        router_config = getattr(self.controller, MetaData.CONTROLLER_SCOPE, {})
        prefix = router_config.pop("prefix", None)
        router = APIRouter(**router_config)
        controller_methods = inspect.getmembers(self.controller, inspect.isfunction)
        for _, method in controller_methods:
            if not hasattr(method, "method"):
                continue
            ExceptionsZone.run(lambda: self._check_controller_method(method))
            path = self._sanitize_path(
                prefix, getattr(method, MetaData.REQUEST_METHOD_PATH)
            )
            router.add_api_route(
                path=path, endpoint=method, methods=[method.method], **method.__kwargs__
            )

        setattr(self.controller, "router", router)
        instance = RouterProxy(controller=self.controller, router=router)
        return instance.create()
