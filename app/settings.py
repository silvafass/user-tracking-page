import warnings
from typing import Literal, Self

from pydantic import PostgresDsn, computed_field, model_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_v1_str: str = "/api/v1"
    secret_key: str
    domain: str = "localhost"
    environment: Literal["local", "staging", "production"] = "local"

    project_name: str
    postgres_server: str
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str = ""
    postgres_db: str = ""
    db_echo: bool = False

    @computed_field
    @property
    def postgress_db_connection_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_server,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "secret_to_development_proposal":
            message = (
                f"The value of {var_name} is "
                '"secret_to_development_proposal", '
                "for security, please change it, at least for deployments."
            )
            if self.environment == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.secret_key)
        self._check_default_secret("POSTGRES_PASSWORD", self.postgres_password)

        return self

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
