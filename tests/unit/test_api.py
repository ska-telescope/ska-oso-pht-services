"""
Unit tests for ska_oso_pht_services.api
"""

import json
from http import HTTPStatus
from unittest import mock

from ska_oso_pdm.generated.models.proposal import Proposal
from ska_oso_pdm.openapi import CODEC as OPENAPI_CODEC

from .util import (
    VALID_PROPOSAL_DATA_JSON,
    VALID_PROPOSAL_FRONTEND_UPDATE_JSON,
    VALID_PROPOSAL_GET_LIST_RESULT_JSON,
    VALID_PROPOSAL_UPDATE_RESULT_JSON,
    assert_json_is_equal,
)


@mock.patch("ska_oso_pht_services.api.oda")
def test_proposal_create(mock_oda, client):
    """
    Check the proposal_create method returns the expected prsl_id and status code
    """

    uow_mock = mock.MagicMock()
    uow_mock.prsls.__contains__.return_value = True
    uow_mock.prsls.add.return_value = OPENAPI_CODEC.loads(
        Proposal, VALID_PROPOSAL_DATA_JSON
    )
    mock_oda.uow.__enter__.return_value = uow_mock

    response = client.post(
        "/ska-oso-pht-services/pht/api/v1/proposals",
        data=VALID_PROPOSAL_DATA_JSON,
        headers={"Content-type": "application/json"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.text == "prsl-1234"


@mock.patch("ska_oso_pht_services.api.oda")
def test_proposal_get(mock_oda, client):
    uow_mock = mock.MagicMock()
    uow_mock.prsls.__contains__.return_value = True
    uow_mock.prsls.get.return_value = OPENAPI_CODEC.loads(
        Proposal, VALID_PROPOSAL_DATA_JSON
    )

    mock_oda.uow.__enter__.return_value = uow_mock

    result = client.get(
        "/ska-oso-pht-services/pht/api/v1/proposals/prsl-1234",
        data=VALID_PROPOSAL_DATA_JSON,
        headers={"Content-type": "application/json"},
    )

    assert result.status_code == HTTPStatus.OK
    assert_json_is_equal(result.text, VALID_PROPOSAL_DATA_JSON)


@mock.patch("ska_oso_pht_services.api.oda")
def test_proposal_get_list(mock_oda, client):
    list_result = json.loads(VALID_PROPOSAL_GET_LIST_RESULT_JSON)

    return_value = []
    for x in list_result:
        return_value.append(OPENAPI_CODEC.loads(Proposal, json.dumps(x)))

    uow_mock = mock.MagicMock()
    uow_mock.prsls.__contains__.return_value = True
    uow_mock.prsls.query.return_value = return_value

    mock_oda.uow.__enter__.return_value = uow_mock

    result = client.get("/ska-oso-pht-services/pht/api/v1/proposals/list/DefaultUser")

    assert result.status_code == HTTPStatus.OK
    assert_json_is_equal(result.text, VALID_PROPOSAL_GET_LIST_RESULT_JSON)


@mock.patch("ska_oso_pht_services.api.oda")
def test_proposal_edit(mock_oda, client):
    uow_mock = mock.MagicMock()
    uow_mock.prsls.__contains__.return_value = True
    uow_mock.prsls.get.return_value = OPENAPI_CODEC.loads(
        Proposal, VALID_PROPOSAL_UPDATE_RESULT_JSON
    )

    mock_oda.uow.__enter__.return_value = uow_mock

    result = client.put(
        "/ska-oso-pht-services/pht/api/v1/proposals/prsl-1234",
        data=VALID_PROPOSAL_FRONTEND_UPDATE_JSON,
        headers={"Content-type": "application/json"},
    )

    assert_json_is_equal(result.text, VALID_PROPOSAL_UPDATE_RESULT_JSON)
    assert result.status_code == HTTPStatus.OK


def test_proposal_validate(client):
    result = client.post("/ska-oso-pht-services/pht/api/v1/proposals/validate", data={})

    assert result.status_code == HTTPStatus.OK
    assert result.text == "post /proposals/validate"


def test_upload_pdf(client):
    result = client.post("/ska-oso-pht-services/pht/api/v1/upload/pdf", data={})

    assert result.status_code == HTTPStatus.OK
    assert result.text == "post /upload/pdf"


def test_get_coordinates(client):
    name = "LHS337"
    result = client.get(f"/ska-oso-pht-services/pht/api/v1/coordinates/{name}")

    assert result.status_code == HTTPStatus.OK
    assert result.text == "12:38:49.0984 -38:22:53.67"
