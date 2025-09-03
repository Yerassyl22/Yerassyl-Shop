from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = "*"
    PROJECT_NAME: str = "Yerassyl Shop"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()