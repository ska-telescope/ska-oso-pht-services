import json
from datetime import datetime, timedelta
from http import HTTPStatus
from os import getenv

import pytest
import requests

from ska_oso_pht_services.connectors.pht_handler import transform_update_proposal

# TODO: add assert_json_is_equal
from ..unit.util import (
    VALID_PROPOSAL_DATA_JSON,
    VALID_PROPOSAL_FRONTEND_UPDATE_JSON,
    VALID_PROPOSAL_GET_VALIDATE_BODY_JSON,
    VALID_PROPOSAL_GET_VALIDATE_BODY_JSON_TARGET_NOT_FOUND,
    VALID_PROPOSAL_GET_VALIDATE_RESULT_JSON_TARGET_NOT_FOUND
)

KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
PHT_URL = getenv(
    "PHT_URL", f"http://ska-oso-pht-services-rest-test:5000/{KUBE_NAMESPACE}/pht/api/v1"
)


# TODO: revisit test cases
def test_proposal_create():
    """
    Test that the POST /proposals path receives the request
    and returns a valid Proposal ID
    """

    response = requests.post(
        f"{PHT_URL}/proposals",
        data={VALID_PROPOSAL_DATA_JSON},
        headers={"Content-type": "application/json"},
    )
    assert response.status_code == HTTPStatus.OK
    assert f"prsl-t0001-{datetime.today().strftime('%Y%m%d')}" in response.text


def test_proposal_get():
    """
    Test that the GET /proposals/{identifier} path receives the request
    and returns the correct response prsl-1234 is pulled in filesystem on k8s-pre-test
    """

    response = requests.get(f"{PHT_URL}/proposals/prsl-1234")

    # assert_json_is_equal(response.content, VALID_PROPOSAL_DATA_JSON)
    result = transform_update_proposal(json.loads(response.content))

    assert result["prsl_id"] == "prsl-1234"
    assert response.status_code == HTTPStatus.OK


def test_proposal_get_list():
    """
    Test that the GET /proposals/list/{identifier} path receives the request
    and returns the correct response in an array
    """
    requests.post(
        f"{PHT_URL}/proposals",
        data={VALID_PROPOSAL_DATA_JSON},
        headers={"Content-type": "application/json"},
    )

    response = requests.get(f"{PHT_URL}/proposals/list/DefaultUser")
    result = json.loads(response.content)

    print(response.content)
    print(response.content)

    assert response.status_code == HTTPStatus.OK
    assert result[0]["metadata"]["created_by"] == "DefaultUser"


def test_proposal_put():
    """
    TODO: review pdm for datatype for investigators and investigator_id
    Test that the PUT /proposals/{identifier} path receives the request
    and returns the correct response
    """

    response = requests.put(
        f"{PHT_URL}/proposals/prsl-1234",
        data=VALID_PROPOSAL_FRONTEND_UPDATE_JSON,
        headers={"Content-type": "application/json"},
    )

    assert response.status_code == HTTPStatus.OK

    before_transform = json.loads(response.content)

    # assert before_transform["metadata"]["version"] == 2

    assert datetime.fromisoformat(
        before_transform["metadata"]["last_modified_on"]
    ).timestamp() == pytest.approx(
        datetime.now().timestamp(), abs=timedelta(seconds=100).total_seconds()
    )

    expected = transform_update_proposal(
        json.loads(VALID_PROPOSAL_FRONTEND_UPDATE_JSON)
    )
    print("response content")
    print(response.content)

    result = transform_update_proposal(json.loads(response.content))

    print("transformed response content")
    print(result)

    print('result["metadata"]["version"]')
    print(type(result["metadata"]["version"]))
    print(result["metadata"]["version"])

    del result["metadata"]
    del expected["metadata"]

    # TODO: review pdm for datatype for investigators and investigator_id
    # assert expected == result


def test_proposal_validate():
    """
    Test that the POST /proposals/validate path receives the request
    and returns result and messages
    """

    response = requests.post(
        f"{PHT_URL}/proposals/validate",
        data=VALID_PROPOSAL_GET_VALIDATE_BODY_JSON,
        headers={"Content-type": "application/json"},
    )

    result = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert result["result"] is True


def test_proposal_validate_target_not_found():
    """
    Test that the POST /proposals/validate path receives the request
    and returns result and messages
    """

    response = requests.post(
        f"{PHT_URL}/proposals/validate",
        data=VALID_PROPOSAL_GET_VALIDATE_BODY_JSON_TARGET_NOT_FOUND,
        headers={"Content-type": "application/json"},
    )

    result = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert result["result"] is False
