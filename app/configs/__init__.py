from app.configs.base_settings import Settings


def get_settings() -> Settings:
    return Settings(_env_file=".env", _env_file_encoding="utf-8")


settings = get_settings()
