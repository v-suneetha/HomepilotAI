from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "HomePilot AI"
    debug: bool = True


settings = Settings()
