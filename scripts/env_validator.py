from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    rule: str
    message: str


def validate_env_values(values: dict[str, str]) -> None:
    issues: list[ValidationIssue] = []
    issues.extend(_find_duplicate_ports(values))

    if not issues:
        return

    details = "\n".join(f"- [{issue.rule}] {issue.message}" for issue in issues)
    raise SystemExit(f"Env validation failed:\n{details}")


def _find_duplicate_ports(values: dict[str, str]) -> list[ValidationIssue]:
    port_usage: dict[str, list[str]] = {}

    for key, value in values.items():
        if not key.endswith("_PORT"):
            continue

        normalized = value.strip()
        # Docker treats host port 0 as "pick any free port", so it is not a collision.
        if not normalized or normalized == "0":
            continue

        port_usage.setdefault(normalized, []).append(key)

    issues: list[ValidationIssue] = []
    for port, keys in sorted(port_usage.items(), key=_port_sort_key):
        if len(keys) < 2:
            continue
        joined_keys = ", ".join(sorted(keys))
        issues.append(
            ValidationIssue(
                rule="unique-port-envs",
                message=f"host port {port} is assigned more than once: {joined_keys}",
            )
        )

    return issues


def _port_sort_key(item: tuple[str, list[str]]) -> tuple[int, str]:
    port = item[0]
    return (0, f"{int(port):05d}") if port.isdigit() else (1, port)
