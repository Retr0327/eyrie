from types import FunctionType
from typing import Any

from eyrie.common.constants import HTTP_METHODS


def get_cls_name(cls: type | str | FunctionType) -> str:
    if isinstance(cls, str):
        return cls
    return getattr(cls, "__name__", None)


def UNKNOWN_EXPORT_MESSAGE(cls: str | type, module: str | type):
    cls_name, module_name = get_cls_name(cls), get_cls_name(module)
    return (
        f"Cannot export a provider/module that is not a part of the currently processed module ({module_name}). "
        f"Please verify whether the exported {cls_name} is available in this particular context.\n\n"
        "Possible Solutions:\n"
        f"Is {cls_name} part of the relevant providers/imports within {module_name}?"
    )


def USING_INVALID_CLASS_AS_A_MODULE_MESSAGE(cls: str | type, module: str | type):
    invalid_cls, module_name = get_cls_name(cls), get_cls_name(module)
    return (
        "Classes annotated with @Injectable() decorator must not appear in the 'imports' array of a module.\n"
        f"Please remove {invalid_cls} (including forwarded occurrences, if any) from all of the 'imports' arrays.\n\n"
        f"Scope {module_name}"
    )


def CIRCULAR_DEPENDENCY_MESSAGE(provider: str | type, dep: str | type):
    provider_name, dep_name = get_cls_name(provider), get_cls_name(dep)
    return (
        f"Circular reference detected: {provider_name} -> {dep_name}.\n"
        "Note that circular relationships between custom providers (e.g., factories) are "
        "not supported since functions cannot be called more than once."
    )


def INVALID_MODULE_CONFIG_MESSAGE(module_key: str):
    return f"Invalid property '{module_key}' passed into the @Module() decorator."


def INVALID_MODULE_METADATA_TYPE_MESSAGE(metadata_key: str):
    return f"Invalid type of the module `{metadata_key}` metadata, expected list."


def INVALID_CONTROLLER_MESSAGE(controller: type | FunctionType):
    token = get_cls_name(controller)
    if token is None:
        return (
            "An invalid controller has been detected. Perhaps, one of your controllers is "
            "missing the @Controller() decorator."
        )
    return (
        f"An invalid controller has been detected. '{token}' does not have the @Controller() "
        "decorator but it is being listed in the 'controllers' array of some module."
    )


def USING_INVALID_CLASS_AS_A_MODULE_MESSAGE(cls: str | type, module: str | type):
    cls_name, module_name = get_cls_name(cls), get_cls_name(module)
    return (
        "Classes annotated with @Injectable(), and @Controller() decorators "
        f"must not appear in the 'imports' array of a module. Please remove {cls_name} "
        "(including forwarded occurrences, if any) from all of the 'imports' arrays.\n\n"
        f"Scope [{module_name}]"
    )


def INVALID_MODULE_TYPE_MESSAGE(module: type | Any):
    module_name = get_cls_name(module)
    name = module if module_name is None else module_name
    return (
        f"Module '{name}' is not constructable or annotated with @Module() decorator."
    )


def UNKNOWN_DEPENDENCIES_MESSAGE(
    dep: type | Any, module: type | Any, dep_context: str | type
):
    dep_name, module_name, dep_context_name = (
        get_cls_name(dep),
        get_cls_name(module),
        get_cls_name(dep_context),
    )
    potentialSolutions = (
        "\n\nPotential solutions:\n"
        f"- If {dep_name} is a provider, is it part of the current {module_name}?\n"
        f"- If {dep_name} is exported from a separate @Module, is that module imported "
        f"within {module_name}?\n\n"
        "  @Module({\n"
        f"\timports: [ /* the Module containing {dep_name} */ ]\n"
        "  })"
    )

    return (
        f"Eyrie can't resolve dependencies of the {dep_name} of the {dep_context_name}. "
        f"Please make sure that the argument {dep_name} is available in the {module_name} context."
        f"{potentialSolutions}"
    )


def INVALID_DECORATOR_ITEM_MESSAGE(
    target: type | FunctionType, item: str, decorator: str
):
    context = get_cls_name(target)
    return f"Invalid {item} passed to {decorator}() decorator ({context})."


def INVALID_CONTROLLER_HTTP_METHOD_MESSAGE(
    method: str, controller: type | FunctionType
):
    controller_name = get_cls_name(controller)
    return (
        f"Invalid HTTP method `{method}` in controller {controller_name}. "
        f"Expected one of: {', '.join(HTTP_METHODS)}"
    )


def UNKNOWN_CONTROLLER_HTTP_METHOD_PATH(
    method: FunctionType, controller: type | FunctionType
):
    method_name, controller_name = get_cls_name(method), get_cls_name(controller)
    return f"Invalid path for method {method_name} in controller {controller_name}."
