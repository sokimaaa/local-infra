from __future__ import annotations

import argparse
import sys

from scripts.compose_runner import build_compose_command, print_run_summary, resolve_compose_files, run_compose
from scripts.constants import ROOT
from scripts.env_manager import build_runtime_env_file, resolve_optional_env_file
from scripts.service_registry import available_services, normalize_services


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run reusable Docker Compose stacks for local development.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 local_infra.py up kafka postgres\n"
            "  python3 local_infra.py --stateful up kafka postgres\n"
            "  python3 local_infra.py --env-file .env.project-a up kafka postgres\n"
            "  python3 local_infra.py config kafka postgres\n"
            "  python3 local_infra.py down kafka postgres"
        ),
    )
    parser.add_argument(
        "--env-file",
        help="Extra env overrides applied on top of service defaults and optional .env.example",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the docker compose command instead of executing it.",
    )
    parser.add_argument(
        "--stateful",
        action="store_true",
        help="Use volume-backed compose files when available. Default mode is stateless.",
    )
    parser.add_argument(
        "command",
        choices=["up", "down", "config", "list"],
        help="Action to execute.",
    )
    parser.add_argument(
        "services",
        nargs="*",
        help="Services to include in the stack, e.g. kafka postgres.",
    )
    return parser


def split_passthrough_args(raw_args: list[str]) -> tuple[list[str], list[str]]:
    if "--" not in raw_args:
        return raw_args, []

    separator_index = raw_args.index("--")
    return raw_args[:separator_index], raw_args[separator_index + 1 :]


def print_available_services() -> None:
    print("Available services:")
    for name in available_services():
        print(f"  - {name}")


def build_compose_args(command_name: str, passthrough_args: list[str]) -> list[str]:
    compose_args = [command_name]
    if command_name == "up":
        compose_args.append("-d")
    compose_args.extend(passthrough_args)
    return compose_args


def main(argv: list[str] | None = None) -> int:
    raw_args = list(argv) if argv is not None else sys.argv[1:]
    parser = build_parser()
    parsed_args, passthrough_args = split_passthrough_args(raw_args)
    args = parser.parse_args(parsed_args)

    if args.command == "list":
        print_available_services()
        return 0

    if not args.services:
        parser.error("at least one service is required unless command=list")

    services = normalize_services(args.services)
    root_env_file = ROOT / ".env.example"
    override_env_file = resolve_optional_env_file(args.env_file)
    env_file, env_values = build_runtime_env_file(services, root_env_file, override_env_file)
    compose_project = env_values.get("COMPOSE_PROJECT_NAME", "undefined")
    compose_files, warnings = resolve_compose_files(services, args.stateful)
    compose_args = build_compose_args(args.command, passthrough_args)
    command = build_compose_command(env_file, compose_files, compose_args)

    print_run_summary(
        services=services,
        compose_project=compose_project,
        env_file=env_file,
        root_env_exists=root_env_file.exists(),
        override_env_file=override_env_file,
        stateful=args.stateful,
        warnings=warnings,
        command=command,
    )

    if args.dry_run:
        return 0

    return run_compose(command)
