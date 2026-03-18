from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from scripts.constants import BASE_COMPOSE, ROOT, SERVICE_ENV_FILES, SERVICE_FILES


def resolve_compose_files(services: list[str], stateful: bool) -> tuple[list[Path], list[str]]:
    compose_files: list[Path] = []
    warnings: list[str] = []

    for service in services:
        service_files = SERVICE_FILES[service]
        if stateful:
            stateful_file = service_files.get("stateful")
            if stateful_file and stateful_file.exists():
                compose_files.append(stateful_file)
                continue
            warnings.append(
                f"Warning: service '{service}' has no stateful compose file. Falling back to stateless variant."
            )

        compose_files.append(service_files["stateless"])

    return compose_files, warnings


def build_compose_command(env_file: Path, compose_files: list[Path], compose_args: list[str]) -> list[str]:
    command = [
        "docker",
        "compose",
        "--project-directory",
        str(ROOT),
        "--env-file",
        str(env_file),
        "-f",
        str(BASE_COMPOSE),
    ]
    for compose_file in compose_files:
        command.extend(["-f", str(compose_file)])
    command.extend(compose_args)
    return command


def print_run_summary(
    services: list[str],
    compose_project: str,
    env_file: Path,
    root_env_exists: bool,
    override_env_file: Path | None,
    stateful: bool,
    warnings: list[str],
    command: list[str],
) -> None:
    source_files = [str(SERVICE_ENV_FILES[service].relative_to(ROOT)) for service in services]
    if root_env_exists:
        source_files.append(".env")
    if override_env_file:
        source_files.append(
            str(override_env_file.relative_to(ROOT) if override_env_file.is_relative_to(ROOT) else override_env_file)
        )

    print(f"Env sources: {', '.join(source_files)}", flush=True)
    print(f"Generated env file: {env_file.relative_to(ROOT)}", flush=True)
    print(f"Compose project: {compose_project}", flush=True)
    print(f"Mode: {'stateful' if stateful else 'stateless'}", flush=True)
    print(f"Services: {', '.join(services)}", flush=True)
    for warning in warnings:
        print(warning, flush=True)
    print("Command:", shlex.join(command), flush=True)


def run_compose(command: list[str]) -> int:
    completed = subprocess.run(command, cwd=ROOT)
    return completed.returncode
