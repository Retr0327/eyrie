from collections.abc import Sequence

from eyrie.common.constants import MODULE_METADATA_FIELDS
from eyrie.core.errors import InvalidModuleConfigException


def validate_module_keys(keys: Sequence[str]):
    for key in keys:
        if key not in MODULE_METADATA_FIELDS:
            raise InvalidModuleConfigException(module_key=key)
