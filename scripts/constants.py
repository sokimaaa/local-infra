from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMPOSE_DIR = ROOT / "compose"
BASE_COMPOSE = COMPOSE_DIR / "base.yml"

SERVICE_ALIASES = {
    "af": "airflow",
    "cpkafka": "cp-kafka",
    "cp-kafka-ui": "cp-kafka",
    "cpkafkarest": "cp-kafka-rest",
    "kafkarest": "cp-kafka-rest",
    "kafka-rest": "cp-kafka-rest",
    "kafka-ui": "kafka",
    "kafkaui": "kafka",
    "pg": "postgres",
}

SERVICE_DEPENDENCIES = {
    "cp-kafka-rest": ["cp-kafka"],
}

SERVICE_FILES = {
    "airflow": {
        "stateless": COMPOSE_DIR / "services" / "airflow.yml",
        "stateful": COMPOSE_DIR / "services" / "airflow.stateful.yml",
    },
    "cp-kafka": {
        "stateless": COMPOSE_DIR / "services" / "cp-kafka.yml",
        "stateful": COMPOSE_DIR / "services" / "cp-kafka.stateful.yml",
    },
    "cp-kafka-rest": {
        "stateless": COMPOSE_DIR / "services" / "cp-kafka-rest.yml",
        "stateful": COMPOSE_DIR / "services" / "cp-kafka-rest.yml",
    },
    "postgres": {
        "stateless": COMPOSE_DIR / "services" / "postgres.yml",
        "stateful": COMPOSE_DIR / "services" / "postgres.stateful.yml",
    },
    "kafka": {
        "stateless": COMPOSE_DIR / "services" / "kafka.yml",
        "stateful": COMPOSE_DIR / "services" / "kafka.stateful.yml",
    },
    "s3": {
        "stateless": COMPOSE_DIR / "services" / "s3.yml",
        "stateful": COMPOSE_DIR / "services" / "s3.stateful.yml",
    },
}

SERVICE_ENV_FILES = {
    "airflow": ROOT / "env" / "airflow.env",
    "cp-kafka": ROOT / "env" / "cp-kafka.env",
    "cp-kafka-rest": ROOT / "env" / "cp-kafka-rest.env",
    "postgres": ROOT / "env" / "postgres.env",
    "kafka": ROOT / "env" / "kafka.env",
    "s3": ROOT / "env" / "s3.env",
}
