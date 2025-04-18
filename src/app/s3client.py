
__author__ = "William Morris [morriswa]"
"""
    easy s3 client, to easily complete application needs
"""

import logging
import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config


__s3_client = boto3.client(
    "s3",
    endpoint_url=f'https://s3.{os.getenv('AWS_REGION')}.amazonaws.com',
)
__log = logging.getLogger(__name__)
__s3_bucket = os.getenv('AWS_S3_BUCKET')
__s3_environment = os.getenv('AWS_S3_ENVIRONMENT')


def list(prefix):
    objects = []
    paginator = __s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=__s3_bucket, Prefix=f'{__s3_environment}/{prefix}/'):
        if 'Contents' in page:
            for obj in page['Contents']:
                objects.append(str(obj['Key']).removeprefix(f'{__s3_environment}/{prefix}/'))
    return objects

def upload(upload_file, key) -> None:
    try:
        __s3_client.upload_fileobj(
            Fileobj=upload_file,
            Bucket=__s3_bucket,
            Key=f'{__s3_environment}/{key}',
            ExtraArgs={
                'ContentType': upload_file.content_type
            }
        )
    except ClientError as e:
        __log.error(e)


def sget(key: str, expires_in_minutes: int = 30) -> Optional[str]:
    return get(key, expires_in_minutes) if exists(key) else None


def get(key: str, expires_in_minutes: int = 30) -> str:
    response = __s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': __s3_bucket,
            'Key': f'{__s3_environment}/{key}',
        },
        ExpiresIn=expires_in_minutes * 60)
    return response


def exists(key: str) -> bool:
    try:
        __s3_client.head_object(Bucket=__s3_bucket, Key=f'{__s3_environment}/{key}',)
        return True
    except ClientError:
        return False


def delete(key: str) -> None:
    __s3_client.delete_object(Bucket=__s3_bucket, Key=f'{__s3_environment}/{key}',)
