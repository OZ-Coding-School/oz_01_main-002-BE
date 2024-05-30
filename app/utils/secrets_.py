# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
from typing import Any

import boto3  # type: ignore
import orjson
from botocore.exceptions import ClientError, NoCredentialsError  # type: ignore


def get_secret() -> Any:

    secret_name = "mpg/secrets/env"
    region_name = "ap-northeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response["SecretString"]
        return orjson.loads(secret)

    except NoCredentialsError:
        return {"message": "Credentials not available"}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            return {"message": "The requested secret was not found"}
        else:
            return {"Error occurred: ": str(e)}


if __name__ == "__main__":
    get_secret()

    # Your code goes here.
