import re


def sanitize_path(prefix: str | None, path: str) -> str:
    combined_path = f"{prefix or ''}{path}"
    sanitized_path = re.sub(r"^/*", "/", combined_path)
    return re.sub(r"/+$", "", sanitized_path)
