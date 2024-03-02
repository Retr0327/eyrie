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
from eyrie.core.utils import sanitize_path

from .proxy import RouterProxy

T = TypeVar("T")


@dataclass(slots=True)
class RouterFactory:
    controller: type[T]
    global_prefix: str = ""

    def _check_controller_method(self, method: FunctionType):
        if not hasattr(method, MetaData.REQUEST_METHOD_PATH):
            raise UnknownControllerHTTPMethodPathException(
                method=method, controller=self.controller
            )

        if method.method not in HTTP_METHODS:
            raise InvalidControllerHTTPMethodException(
                method=method.method, controller=self.controller
            )

    def create(self) -> type[T]:
        router_config = getattr(self.controller, MetaData.CONTROLLER_SCOPE, {})
        controller_prefix = router_config.pop("prefix", None)
        router = APIRouter(**router_config)
        controller_methods = inspect.getmembers(self.controller, inspect.isfunction)
        for _, method in controller_methods:
            if not hasattr(method, "method"):
                continue
            ExceptionsZone.run(lambda: self._check_controller_method(method))
            controller_path = sanitize_path(
                controller_prefix, getattr(method, MetaData.REQUEST_METHOD_PATH)
            )
            router.add_api_route(
                path=sanitize_path(self.global_prefix, controller_path),
                endpoint=method,
                methods=[method.method],
                **method.__kwargs__,
            )

        setattr(self.controller, "router", router)
        instance = RouterProxy(controller=self.controller, router=router)
        return instance.create()
