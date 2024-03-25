# TODO: connect s3 credentials using SKAO Vault

import boto3

import ska_oso_pht_services.utils.config as config

AWS_SERVER_PUBLIC_KEY = config.AWS_SERVER_PUBLIC_KEY
AWS_SERVER_SECRET_KEY = config.AWS_SERVER_SECRET_KEY
AWS_PHT_BUCKET_NAME = config.AWS_PHT_BUCKET_NAME
AWS_REGION_NAME = config.AWS_REGION_NAME

PRESIGNED_URL_EXPIRY_TIME = 60


def get_aws_client():
    aws_access_key_id = AWS_SERVER_PUBLIC_KEY
    aws_secret_access_key = AWS_SERVER_SECRET_KEY
    region_name = AWS_REGION_NAME
    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )


def create_presigned_url_download_pdf(
    key, s3_client, expiry, bucket=AWS_PHT_BUCKET_NAME
):
    """Generate a presigned URL S3 URL for a file
    :param bucket: string
    :param key: string
    :param s3_client: boto3.client
    :param expiry: int
    :return: presigned url of file
    """

    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expiry,
    )

    return url


def create_presigned_url_upload_pdf(key, s3_client, expiry, bucket=AWS_PHT_BUCKET_NAME):
    """Generate a presigned URL S3 URL for a file
    :param bucket: string
    :param key: string
    :param s3_client: boto3.client
    :param expiry: int
    :return: presigned url of file
    """

    url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expiry,
    )

    return url
