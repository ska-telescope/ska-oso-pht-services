"""
TODO
"""

from http import HTTPStatus
from os import getenv

import requests

KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
PHT_URL = getenv(
    "PHT_URL", f"http://ska-oso-pht-services-rest-test:5000/{KUBE_NAMESPACE}/pht/api/v1"
)



def test_proposal_post(client):
    result = client.post(f"{PHT_URL}/create-proposal", data={})
    assert result.status_code == HTTPStatus.CREATED
    assert result.text == "prp-default_generator_id-20240117-00001"