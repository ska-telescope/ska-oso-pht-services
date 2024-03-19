import unittest

import boto3
from moto import mock_aws

from ska_oso_pht_services.utils.s3_bucket import (
    create_presigned_url_download_pdf,
    create_presigned_url_post_pdf,
)

PRESIGNED_URL_EXPIRY_TIME = 60


@mock_aws
class TestS3Bucket(unittest.TestCase):
    def setUp(self):
        self.s3 = boto3.client("s3")
        self.s3.create_bucket(Bucket="mybucket")

    def test_create_presigned_url_download_pdf(self):
        result = create_presigned_url_download_pdf(
            "mybucket", "example.pdf", self.s3, PRESIGNED_URL_EXPIRY_TIME
        )

        from_client = self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": "mybucket",
                "Key": "example.pdf",
            },
            ExpiresIn=PRESIGNED_URL_EXPIRY_TIME,
        )
        assert result == from_client

    def test_create_presigned_url_post_pdf(self):
        result = create_presigned_url_post_pdf(self.s3, "mybucket", "example.pdf")
        from_client = self.s3.generate_presigned_post(
            "mybucket", "example.pdf", Fields=None, Conditions=None, ExpiresIn=3600
        )

        assert result == from_client
