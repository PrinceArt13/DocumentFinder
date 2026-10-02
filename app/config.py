from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    clickhouse_host: str = "localhost"
    clickhouse_port: int
    clickhouse_user: str = "default"
    clickhouse_password: str
    clickhouse_database: str = "default"

    elasticsearch_host: str = "localhost"
    elasticsearch_port: int
    elasticsearch_user: str = "elastic"
    elasticsearch_password: str
    elasticsearch_index: str = "documents"

    app_host: str
    app_port: int

    csv_file_path: str


settings = Settings()
