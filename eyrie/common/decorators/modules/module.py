from eyrie.common.constants import (
    MODULE_METADATA_FIELDS,
    MetaData,
)
from eyrie.common.interfaces import ModuleMetadata
from eyrie.common.utils import (
    validate_by_type,
    validate_module_keys,
)
from eyrie.core.errors import ExceptionsZone


def Module(metadata: ModuleMetadata = {}):
    """Decorator that marks a class as a module.

    Modules are used to organize the application structure into scopes. Controllers and
    Providers are scoped by the module they are declared in. Modules and their classes
    (Controllers and Providers) form a graph.
    """

    keys = metadata.keys()
    validate_by_type(metadata, ModuleMetadata)
    ExceptionsZone.run(callback=lambda: validate_module_keys(keys))

    def wrapper(cls: type):
        is_global = getattr(cls, MetaData.GLOBAL_MODULE, False)
        for field in MODULE_METADATA_FIELDS:
            module_data = metadata.get(field, [])
            setattr(cls, field, module_data)

        setattr(cls, MetaData.GLOBAL_MODULE, is_global)
        return cls

    return wrapper
