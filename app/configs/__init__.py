from app.configs.base_settings import Settings
from app.configs.deploy_settings import DeploySettings
from app.utils.secrets_ import get_secret


def get_settings() -> Settings:
    env = get_secret()
    if env["ENV"] == "deploy":
        return DeploySettings()
    return Settings(_env_file=".env", _env_file_encoding="utf-8")


settings = get_settings()
