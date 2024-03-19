# TODO: connect s3 credentials using SKAO Vault

# import config

# AWS_SERVER_PUBLIC_KEY = config.AWS_SERVER_PUBLIC_KEY
# AWS_SERVER_SECRET_KEY = config.AWS_SERVER_SECRET_KEY
# AWS_PHT_BUCKET_NAME = config.AWS_PHT_BUCKET_NAME
# AWS_REGION_NAME = config.AWS_REGION_NAME

# PRESIGNED_URL_EXPIRY_TIME = 60


# def _get_aws_client():
#     aws_access_key_id = AWS_SERVER_PUBLIC_KEY
#     aws_secret_access_key = AWS_SERVER_SECRET_KEY
#     region_name = AWS_REGION_NAME
#     return boto3.client(
#         "s3",
#         aws_access_key_id=aws_access_key_id,
#         aws_secret_access_key=aws_secret_access_key,
#         region_name=region_name,
#     )


# def _get_all_bucket_object_with_client():
#     s3_client = _get_aws_client()
#     objects = s3_client.list_objects_v2(Bucket=AWS_PHT_BUCKET_NAME)

#     for obj in objects["Contents"]:
#         print(obj["Key"])


def create_presigned_url_download_pdf(bucket, key, s3_client, expiry):
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


def create_presigned_url_post_pdf(
    s3_client, bucket_name, object_name, fields=None, conditions=None, expiration=3600
):
    """Generate a presigned URL S3 POST request to upload a file
    :param s3_client: boto3.client
    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    response = s3_client.generate_presigned_post(
        bucket_name,
        object_name,
        Fields=fields,
        Conditions=conditions,
        ExpiresIn=expiration,
    )
    return response
