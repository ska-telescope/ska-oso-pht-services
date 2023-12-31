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


def test_hello_world():
    """
    TODO
    """
    response = requests.get(f"{PHT_URL}/hello-world")
    print(PHT_URL)
    print(response.text)
    assert response.status_code == HTTPStatus.OK
    assert response.text == "Hello, world!"
