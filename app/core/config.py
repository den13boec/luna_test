from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from urllib.parse import quote_plus


class Settings(BaseSettings):
    API_KEY: SecretStr
    ENV: str = "dev"
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def DATABASE_URL(self) -> str:
        pwd = quote_plus(self.POSTGRES_PASSWORD.get_secret_value())
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{pwd}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
