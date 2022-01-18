import logging
import os 

from dotenv import load_dotenv

import boto3
from botocore import exceptions
from botocore.exceptions import ClientError

# Loads variables on the .env file on the environment variables
user = os.environ.get("USER") if os.environ.get("USER") else os.environ.get("USERNAME")
load_dotenv(f'/home/{user}/credentials/.env') 

# Create a boto3 client with getenv variables, that loads environment variables on our python code
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def create_bucket(name: str):
    try:
        s3_client.create_bucket(
            Bucket=name
        )
        logging.info(f'Bucket {name} created')
    except ClientError as e:
        logging.error(e)
        return False
    return True

create_bucket(name="Datalake-0123456789")