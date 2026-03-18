from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMPOSE_DIR = ROOT / "compose"
BASE_COMPOSE = COMPOSE_DIR / "base.yml"

SERVICE_ALIASES = {
    "kafka-ui": "kafka",
    "kafkaui": "kafka",
    "pg": "postgres",
}

SERVICE_FILES = {
    "postgres": {
        "stateless": COMPOSE_DIR / "services" / "postgres.yml",
        "stateful": COMPOSE_DIR / "services" / "postgres.stateful.yml",
    },
    "kafka": {
        "stateless": COMPOSE_DIR / "services" / "kafka.yml",
        "stateful": COMPOSE_DIR / "services" / "kafka.stateful.yml",
    },
}

SERVICE_ENV_FILES = {
    "postgres": ROOT / "env" / "postgres.env",
    "kafka": ROOT / "env" / "kafka.env",
}
