import logging
import os

import boto3
from botocore.exceptions import ClientError
from ninja import Schema

EXPIRATION = 3600 # 1 hour

class _FieldsUploadDataSchema(Schema):
    key: str
    AWSAccessKeyId: str
    policy: str
    signature: str

class UploadDataSchema(Schema):
    url: str
    fields: _FieldsUploadDataSchema



def create_presigned_url_post(file_path) -> UploadDataSchema:
    s3_client = boto3.client('s3')

    try:
        response = s3_client.generate_presigned_post(os.getenv('AWS_S3_BUCKET'), file_path,
                                                     Fields=None, Conditions=None, ExpiresIn=EXPIRATION)
    except ClientError as e:
        logging.error(e)
        return None

    return UploadDataSchema(**response)

def create_presigned_url_get(file_path) -> str:
    s3_client = boto3.client('s3')

    try:
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': os.getenv('AWS_S3_BUCKET'), 'Key': file_path},
                                                    ExpiresIn=EXPIRATION)

    except ClientError as e:
        logging.error(e)
        return None

    return response

def does_file_exist(file_path) -> bool:
    s3_client = boto3.client('s3')

    try:
        s3_client.head_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=file_path)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

    return True
