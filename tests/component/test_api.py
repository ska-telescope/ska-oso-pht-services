"""
TODO
"""

from http import HTTPStatus

import requests


PHT_URL = (
    "http://ska-oso-pht-services-rest-test:5000/ska-oso-pht-services/pht/api/v1"
)


def test_hello_world():
    """
    TODO
    """
    response = requests.get(f"{PHT_URL}/hello-world")
    assert response.status_code == HTTPStatus.OK
    assert response.text == "Hello, world!"

