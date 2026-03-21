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

Start the Confluent Platform Kafka stack:

```bash
python3 local_infra.py up cp-kafka
```

Start the same stack with Kafka REST Proxy enabled:

```bash
python3 local_infra.py up cp-kafka-rest
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
python3 local_infra.py up cp-kafka
python3 local_infra.py up cp-kafka-rest
python3 local_infra.py config kafka
```

## Current services

### Postgres

Service name and aliases: `postgres`, `pg`

Description: Single-node PostgreSQL database.

| Configurable env     | What it does                   | Default     |
|----------------------|--------------------------------|-------------|
| `POSTGRES_IMAGE_TAG` | Chooses Postgres image tag.    | `16-alpine` |
| `POSTGRES_PORT`      | Exposes Postgres on host port. | `5432`      |
| `POSTGRES_DB`        | Creates default database name. | `local`     |
| `POSTGRES_USER`      | Creates default database user. | `postgres`  |
| `POSTGRES_PASSWORD`  | Sets default user password.    | `postgres`  |

### Kafka

Service name and aliases: `kafka`, `kafka-ui`, `kafkaui`

Description: Single-node Kafka, KRaft mode, includes UI.

| Configurable env        | What it does                      | Default                  |
|-------------------------|-----------------------------------|--------------------------|
| `KAFKA_IMAGE_TAG`       | Chooses Kafka image tag.          | `latest`                 |
| `KAFKA_PORT`            | Exposes Kafka broker on host.     | `9092`                   |
| `KAFKA_CONTROLLER_PORT` | Exposes Kafka controller on host. | `0`                      |
| `KAFKA_CLUSTER_ID`      | Sets the single-node KRaft ID.    | `MkU3OEVBNTcwNTJENDM2Qk` |
| `KAFKA_UI_IMAGE_TAG`    | Chooses Kafka UI image tag.       | `v0.7.2`                 |
| `KAFKA_UI_PORT`         | Exposes Kafka UI on host.         | `8080`                   |
| `KAFKA_UI_CLUSTER_NAME` | Labels the cluster inside the UI. | `local`                  |

### CP Kafka

Service name and aliases: `cp-kafka`, `cpkafka`, `cp-kafka-ui`

Description: Single-node Confluent Platform Kafka, KRaft mode, includes Schema Registry and UI.

| Configurable env           | What it does                              | Default                  |
|----------------------------|-------------------------------------------|--------------------------|
| `CP_KAFKA_PLATFORM_TAG`    | Chooses the Confluent Platform image tag. | `7.6.1`                  |
| `CP_KAFKA_UI_IMAGE_TAG`    | Chooses Kafka UI image tag.               | `v0.7.2`                 |
| `CP_KAFKA_PORT`            | Exposes Kafka broker on host.             | `29092`                  |
| `CP_KAFKA_CONTROLLER_PORT` | Exposes Kafka controller on host.         | `0`                      |
| `CP_SCHEMA_REGISTRY_PORT`  | Exposes Schema Registry on host.          | `8081`                   |
| `CP_SCHEMA_REGISTRY_COMPATIBILITY_LEVEL` | Sets global Schema Registry compatibility. | `BACKWARD` |
| `CP_KAFKA_UI_PORT`         | Exposes Kafka UI on host.                 | `8088`                   |
| `CP_KAFKA_CLUSTER_ID`      | Sets the single-node KRaft ID.            | `MkU3OEVBNTcwNTJENDM2Qk` |
| `CP_KAFKA_UI_CLUSTER_NAME` | Labels the cluster inside the UI.         | `cp-local`               |

### CP Kafka REST 

Service name and aliases: `cp-kafka-rest`, `cpkafkarest`, `cpkafkarest`, `kafkarest`, `kafka-rest`

Description: Extension for `cp-kafka` that adds Kafka REST Proxy. Running `cp-kafka-rest` from the CLI automatically
includes the base `cp-kafka` stack.

| Configurable env        | What it does                              | Default |
|-------------------------|-------------------------------------------|---------|
| `CP_KAFKA_PLATFORM_TAG` | Chooses the Confluent Platform image tag. | `7.6.1` |
| `CP_KAFKA_REST_PORT`    | Exposes Kafka REST Proxy on host.         | `8082`  |

### Complete env files

- [postgres.env](/Users/romandenysov/IdeaProjects/local-infra/env/postgres.env)
- [kafka.env](/Users/romandenysov/IdeaProjects/local-infra/env/kafka.env)
- [cp-kafka.env](/Users/romandenysov/IdeaProjects/local-infra/env/cp-kafka.env)
- [cp-kafka-rest.env](/Users/romandenysov/IdeaProjects/local-infra/env/cp-kafka-rest.env)
