from scripts.constants import SERVICE_ALIASES, SERVICE_FILES


def normalize_services(services: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []

    for service in services:
        key = SERVICE_ALIASES.get(service.lower(), service.lower())
        if key not in SERVICE_FILES:
            supported = ", ".join(sorted(SERVICE_FILES))
            raise SystemExit(f"Unsupported service '{service}'. Supported services: {supported}")
        if key not in seen:
            seen.add(key)
            normalized.append(key)

    return normalized


def available_services() -> list[str]:
    return sorted(SERVICE_FILES)
