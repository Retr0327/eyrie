from enum import StrEnum
from typing import get_args

from .interfaces import (
    HTTPMethodType,
    ModuleMetadata,
)


class Watermark(StrEnum):
    INJECTABLE = "__injectable__"
    CONTROLLER = "__controller__"
    GUARDS = "__guards__"


class MetaData(StrEnum):
    GLOBAL_MODULE = "__module:global__"
    GLOBAL_PROVIDER = "__provider:global__"
    EXPORTED_PROVIDER = "__provider:exported__"
    CONTROLLER_PATH = "__controller:path__"
    CONTROLLER_SCOPE = "__controller:scope__"
    REQUEST_METHOD_PATH = "__path__"


HTTP_METHODS: tuple[str, ...] = get_args(HTTPMethodType)
MODULE_METADATA_FIELDS = ModuleMetadata.__annotations__.keys()
