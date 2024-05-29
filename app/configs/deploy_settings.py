from app.configs import Settings
from app.utils.secrets_ import get_secret

env = get_secret()


class DeploySettings(Settings):
    DB_HOST: str = env["DB_HOST"]
    DB_PORT: int = int(env["DB_PORT"])
    DB_USER: str = env["DB_USER"]
    DB_PASSWORD: str = env["DB_PASSWORD"]
    DB_DB: str = env["DB_DB"]
    GMAIL_USERNAME: str = env["GMAIL_USERNAME"]
    GMAIL_PASSWORD: str = env["GMAIL_PASSWORD"]
    REDIS_URL: str = env["REDIS_URL"]
    SECRET_KEY: str = env["SECRET_KEY"]
    ALGORITHM: str = env["ALGORITHM"]
    AWS_ACCESS_KEY_ID: str = env["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY: str = env["AWS_SECRET_ACCESS_KEY"]
    AWS_S3_BUCKET_NAME: str = env["AWS_S3_BUCKET_NAME"]
    redis_ttl: int = 300
