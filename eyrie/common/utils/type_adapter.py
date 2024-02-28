from typing import (
    Any,
    Literal,
    _TypedDict,
)

from pydantic import TypeAdapter

ValidationType = Literal["json", "python", "strings"]


def validate_by_type(
    data: Any, type: _TypedDict, validation_type: ValidationType = "python"
):
    adapter = TypeAdapter(type)
    match validation_type:
        case "python":
            return adapter.validate_python(data)
        case "json":
            return adapter.validate_json(data)
        case "string":
            return adapter.validate_strings(data)
