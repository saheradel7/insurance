from pydantic_settings import BaseSettings, SettingsConfigDict

import os


class Settings(BaseSettings):
    """
    Application settings.
    """

    keycloak_host: str = os.getenv("KEYCLOAK_HOST", "localhost")
    keycloak_port: int = int(os.getenv("KEYCLOAK_PORT", 8080))
    keycloak_username: str = os.getenv("KEYCLOAK_USERNAME", "admin")
    keycloak_password: str = os.getenv("KEYCLOAK_PASSWORD", "admin")
    keycloak_realm: str = os.getenv("KEYCLOAK_REALM", "master")
    keycloak_client: str = os.getenv("KEYCLOAK_CLIENT", "myclient")

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 5432))
    db_username: str = os.getenv("DB_USERNAME", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")
    db_name: str = os.getenv("DB_NAME", "postgres")
    db_sslmode: str = os.getenv("DB_SSLMODE", "disable")

    model_config = SettingsConfigDict(
        env_file=".env",
    )


env = Settings()
