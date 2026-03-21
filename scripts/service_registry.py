from scripts.constants import SERVICE_ALIASES, SERVICE_DEPENDENCIES, SERVICE_FILES


def _append_service(service: str, seen: set[str], normalized: list[str]) -> None:
    for dependency in SERVICE_DEPENDENCIES.get(service, []):
        _append_service(dependency, seen, normalized)

    if service not in seen:
        seen.add(service)
        normalized.append(service)


def normalize_services(services: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []

    for service in services:
        key = SERVICE_ALIASES.get(service.lower(), service.lower())
        if key not in SERVICE_FILES:
            supported = ", ".join(sorted(SERVICE_FILES))
            raise SystemExit(f"Unsupported service '{service}'. Supported services: {supported}")
        _append_service(key, seen, normalized)

    return normalized


def available_services() -> list[str]:
    return sorted(SERVICE_FILES)
