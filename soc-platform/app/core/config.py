from dataclasses import dataclass
import os
from pathlib import Path


def load_dotenv(path: Path | str = ".env") -> None:
    """Load environment variables from a .env file if it exists."""

    env_path = Path(path)
    if not env_path.is_absolute():
        env_path = Path(__file__).resolve().parents[2] / env_path

    if not env_path.is_file():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        key, sep, value = line.partition("=")
        if sep != "=":
            continue

        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Central place for app-level configuration."""

    app_name: str = os.getenv("APP_NAME", "SOC Platform")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
