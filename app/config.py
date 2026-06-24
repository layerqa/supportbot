from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    driver: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: int = 5432
    user: str = "supportbot"
    password: str = "supportbot"
    name: str = "supportbot"

    @property
    def url(self) -> str:
        return (
            f"{self.driver}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    bot_token: SecretStr
    admin_ids: list[int] = Field(default_factory=list)
    support_chat_id: int
    support_org_name: str

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)


settings = Settings()
