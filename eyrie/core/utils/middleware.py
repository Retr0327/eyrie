import re


def is_regex_path(path: str) -> bool:
    return any(char in path for char in ".+*?()[]{}|^$")


def should_apply_middleware(
    request_method: str, request_path: str, config: dict
) -> bool:
    for excluded_route in config["excluded_routes"]:
        if is_regex_path(excluded_route["path"]):
            path_matches = re.match(excluded_route["path"], request_path) is not None
        else:
            path_matches = request_path == excluded_route["path"]

        if path_matches and (
            excluded_route["method"] == request_method
            or excluded_route["method"] == "ALL"
        ):
            return False

    for route in config["for_routes"]:
        if is_regex_path(route["path"]):
            path_matches = re.match(route["path"], request_path) is not None
        else:
            path_matches = request_path == route["path"]

        if path_matches and (
            route["method"] == request_method or route["method"] == "ALL"
        ):
            return True

    return False
