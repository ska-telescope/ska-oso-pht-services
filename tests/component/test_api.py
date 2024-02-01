from http import HTTPStatus
from os import getenv
from datetime import datetime

import requests

KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
PHT_URL = getenv(
    "PHT_URL", f"http://ska-oso-pht-services-rest-test:5000/{KUBE_NAMESPACE}/pht/api/v1"
)

def test_proposal_post():
    """
    Test that the POST /test-proposals-post-for-oda path receives the request
    and returns a valid Proposal
    """
    
    response = requests.post(
        f"{PHT_URL}/proposals",
        data={},
        headers={"Content-type": "application/json"},
    )
    assert response.status_code == HTTPStatus.OK

    assert response.text == f"prsl-t0001-{datetime.today().strftime('%Y%m%d')}-00002"
