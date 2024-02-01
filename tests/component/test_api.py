from http import HTTPStatus
from os import getenv

import requests

KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
PHT_URL = getenv(
    "PHT_URL", f"http://ska-oso-pht-services-rest-test:5000/{KUBE_NAMESPACE}/pht/api/v1"
)

def test_proposal_post_for_oda():
    """
    Test that the POST /test-proposals-post-for-oda path receives the request
    and returns a valid Proposal
    """

    response = requests.post(
        f"{PHT_URL}/test-proposals-post-for-oda",
        data={},
        headers={"Content-type": "application/json"},
    )
    assert response.status_code == HTTPStatus.OK

    assert response.text == "prsl-t0001-20240131-00002"
    
def test_proposal_post():
    result = requests.post(f"{PHT_URL}/proposal/create", data={})
    assert result.status_code == HTTPStatus.OK
    assert result.text == "prp-00001"
