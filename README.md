# Local Infra

Reusable local infrastructure repo for development across different projects.

## Idea

This repo is built around three rules:

- Compose files define services only
- default values live in `env/`
- the root `.env.example` stays tiny and is used only for project-specific overrides

> Compose files do not contain fallback defaults like `${VAR:-value}`.
>
> If a required variable is missing from the merged env set, Docker Compose should fail immediately. That is
> intentional.

## Quick start

### 1. Optional: create root overrides

```bash
cp .env.example .env.project
```

Then adjust only what is project-specific.

### 2. Start services

For example, to start postgres and kafka:

```bash
python3 local_infra.py up postgres kafka
```

Start the same stack with persistent volumes:

```bash
python3 local_infra.py --stateful up postgres kafka
```

Start only Postgres:

```bash
python3 local_infra.py up postgres
```

### 3. Dry Run

Preview the exact Docker Compose command:

```bash
python3 local_infra.py --dry-run up postgres kafka
```

### 4. Overriding env file

Use an extra override file:

```bash
python3 local_infra.py --env-file .env.project up postgres kafka
```

Keep these extra override files outside `env/` so `env/` remains reserved for service defaults only.

## CLI usage

```bash
python3 local_infra.py [--env-file PATH] [--dry-run] [--stateful] <command> [services...]
```

Commands:

- `up`
- `down`
- `config`
- `list`

Examples:

```bash
python3 local_infra.py list
python3 local_infra.py up kafka postgres
python3 local_infra.py --stateful up kafka postgres
python3 local_infra.py config kafka
```

## Current services

### Postgres

Service name and aliases: `postgres`, `pg`

Description: Single-node PostgreSQL database.

| Configurable env       | What it does                      | Default                |
|------------------------|-----------------------------------|------------------------|
| `POSTGRES_IMAGE_TAG`   | Chooses Postgres image tag.       | `16-alpine`            |
| `POSTGRES_PORT`        | Exposes Postgres on host port.    | `5432`                 |
| `POSTGRES_DB`          | Creates default database name.    | `local`                |
| `POSTGRES_USER`        | Creates default database user.    | `postgres`             |
| `POSTGRES_PASSWORD`    | Sets default user password.       | `postgres`             |

### Kafka

Service name and aliases: `kafka`, `kafka-ui`, `kafkaui`

Description: Single-node Kafka, includes UI.

| Configurable env        | What it does                      | Default                  |
|-------------------------|-----------------------------------|--------------------------|
| `KAFKA_IMAGE_TAG`       | Chooses Kafka image tag.          | `latest`                 |
| `KAFKA_PORT`            | Exposes Kafka broker on host.     | `9092`                   |
| `KAFKA_UI_PORT`         | Exposes Kafka UI on host.         | `8080`                   |

### Complete env files

- [postgres.env](/Users/romandenysov/IdeaProjects/local-infra/env/postgres.env)
- [kafka.env](/Users/romandenysov/IdeaProjects/local-infra/env/kafka.env)
