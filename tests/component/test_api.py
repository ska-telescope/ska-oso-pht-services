import json
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from os import getenv

import pytest
import requests

# TODO: add assert_json_is_equal
from ..unit.util import (
    VALID_PROPOSAL_DATA_JSON,
    VALID_PROPOSAL_GET_VALIDATE_BODY_JSON,
    VALID_PROPOSAL_GET_VALIDATE_BODY_JSON_TARGET_NOT_FOUND,
)

# TODO: revisit test_proposal_put
# from ska_oso_pht_services.connectors.pht_handler import transform_update_proposal

KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
PHT_URL = getenv(
    "PHT_URL", f"http://ska-oso-pht-services-rest-test:5000/{KUBE_NAMESPACE}/pht/api/v1"
)

test_prsl_id = ""


# TODO: revisit test cases
def test_proposal_create():
    """
    Test that the POST /proposals path receives the request
    and returns a valid Proposal ID
    """

    global test_prsl_id  # pylint: disable=W0603

    response = requests.post(
        f"{PHT_URL}/proposals",
        data=VALID_PROPOSAL_DATA_JSON,
        headers={"Content-type": "application/json"},
    )

    assert response.status_code == HTTPStatus.OK
    assert f"prsl-t0001-{datetime.today().strftime('%Y%m%d')}" in response.text

    test_prsl_id = response.text


def test_proposal_get():
    """
    Test that the GET /proposals/{identifier} path receives the request
    and returns the correct response of the created proposal
    """

    response = requests.get(f"{PHT_URL}/proposals/{test_prsl_id}")
    result = json.loads(response.content)

    assert result["prsl_id"] == test_prsl_id
    assert response.status_code == HTTPStatus.OK


def test_proposal_get_list():
    """
    Test that the GET /proposals/list/{identifier} path receives the request
    and returns the correct response in an array
    """

    requests.post(
        f"{PHT_URL}/proposals",
        data=VALID_PROPOSAL_DATA_JSON,
        headers={"Content-type": "application/json"},
    )

    response = requests.get(f"{PHT_URL}/proposals/list/DefaultUser")
    result = json.loads(response.content)

    assert response.status_code == HTTPStatus.OK
    assert result[0]["metadata"]["created_by"] == "DefaultUser"


def test_proposal_put():
    """
    TODO: review pdm for datatype for investigators and investigator_id
    Test that the PUT /proposals/{identifier} path receives the request
    and returns the correct response
    """

    NEW_VALID_PROPOSAL_DATA_JSON = VALID_PROPOSAL_DATA_JSON

    new_valid_proposal_data_json = json.loads(NEW_VALID_PROPOSAL_DATA_JSON)
    new_valid_proposal_data_json["prsl_id"] = test_prsl_id

    NEW_VALID_PROPOSAL_DATA_JSON = json.dumps(new_valid_proposal_data_json)

    response = requests.put(
        f"{PHT_URL}/proposals/{test_prsl_id}",
        data=NEW_VALID_PROPOSAL_DATA_JSON,
        headers={"Content-type": "application/json"},
    )

    assert response.status_code == HTTPStatus.OK

    before_transform = json.loads(response.content)

    assert before_transform["metadata"]["version"] == 2
    assert datetime.fromisoformat(
        before_transform["metadata"]["last_modified_on"].replace("Z", "+00:00")
    ).timestamp() == pytest.approx(
        datetime.now(timezone.utc).timestamp(),
        abs=timedelta(seconds=100).total_seconds(),
    )

    # expected = transform_update_proposal(json.loads(VALID_PROPOSAL_DATA_JSON))
    # result = transform_update_proposal(json.loads(response.content))

    # TODO: review pdm for datatype for investigators and investigator_id
    # assert expected == result


# TODO: revisit after validate endpoint is updated with latest pdm
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
