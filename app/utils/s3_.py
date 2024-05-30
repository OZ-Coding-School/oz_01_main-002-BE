import boto3  # type: ignore

from app.configs import settings

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID  # type: ignore
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY  # type: ignore
AWS_S3_BUCKET_NAME = settings.AWS_S3_BUCKET_NAME  # type: ignore


def s3_client() -> boto3.client:
    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return s3
