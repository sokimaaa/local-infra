from __future__ import annotations

from pathlib import Path

from scripts.constants import ROOT, SERVICE_ENV_FILES


def parse_env_file(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')
    return values


def resolve_optional_env_file(raw_value: str | None) -> Path | None:
    if not raw_value:
        return None

    candidate = Path(raw_value)
    return candidate if candidate.is_absolute() else ROOT / candidate


def build_runtime_env_file(
    services: list[str],
    root_env_file: Path | None,
    override_env_file: Path | None,
) -> tuple[Path, dict[str, str]]:
    layered_env_files = [SERVICE_ENV_FILES[service] for service in services]
    if root_env_file and root_env_file.exists():
        layered_env_files.append(root_env_file)
    if override_env_file:
        layered_env_files.append(override_env_file)

    values: dict[str, str] = {}
    for env_file in layered_env_files:
        if not env_file.exists():
            raise SystemExit(f"Env file does not exist: {env_file}")
        values.update(parse_env_file(env_file))

    generated_dir = ROOT / ".generated"
    generated_dir.mkdir(exist_ok=True)
    runtime_env_file = generated_dir / "runtime.env"
    lines = [f"{key}={values[key]}" for key in sorted(values)]
    runtime_env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return runtime_env_file, values
