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
    VALID_PROPOSAL_GET_VALIDATE_BODY_JSON,
    VALID_PROPOSAL_GET_VALIDATE_BODY_JSON_TARGET_NOT_FOUND,
    VALID_PROPOSAL_GET_VALIDATE_RESULT_JSON,
    VALID_PROPOSAL_GET_VALIDATE_RESULT_JSON_TARGET_NOT_FOUND,
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
    result = client.post(
        "/ska-oso-pht-services/pht/api/v1/proposals/validate",
        data=VALID_PROPOSAL_GET_VALIDATE_BODY_JSON,
        headers={"Content-type": "application/json"},
    )

    assert_json_is_equal(result.text, VALID_PROPOSAL_GET_VALIDATE_RESULT_JSON)
    assert result.status_code == HTTPStatus.OK


def test_proposal_validate_target_not_found(client):
    result = client.post(
        "/ska-oso-pht-services/pht/api/v1/proposals/validate",
        data=VALID_PROPOSAL_GET_VALIDATE_BODY_JSON_TARGET_NOT_FOUND,
        headers={"Content-type": "application/json"},
    )

    assert_json_is_equal(
        result.text, VALID_PROPOSAL_GET_VALIDATE_RESULT_JSON_TARGET_NOT_FOUND
    )
    assert result.status_code == HTTPStatus.OK


class TestGetSignedUrl:
    test_case = "prsl-1234-science.pdf"

    def test_get_upload_signed_url(self, client):
        for data in self.test_case:
            self.get_upload_signed_url(client, *data)

    def test_get_download_signed_url(self, client):
        for data in self.test_case:
            self.get_download_signed_url(client, *data)

    def get_upload_signed_url(self, client, name):
        base_url = "/ska-oso-pht-services/pht/api/v1/upload/signedurl/"

        response = client.get(f"{base_url}{name}")
        assert response.status_code == HTTPStatus.OK

    def get_download_signed_url(self, client, name):
        base_url = "/ska-oso-pht-services/pht/api/v1/download/signedurl/"

        response = client.get(f"{base_url}{name}")
        assert response.status_code == HTTPStatus.OK


class TestGetCoordinates:
    test_cases = [
        (
            "M31",
            "test",
            {
                "equatorial": {
                    "ra": "00:42:44.330",
                    "dec": "+41:16:07.500",
                    "redshift": -0.001,
                    "velocity": -300.0,
                }
            },
        ),
        (
            "N10",
            "galactic",
            {
                "galactic": {
                    "lat": -78.5856,
                    "lon": 354.21,
                    "redshift": 0.022946,
                    "velocity": 6800.0,
                }
            },
        ),
        (
            "N10",
            "equatorial",
            {
                "equatorial": {
                    "dec": "-33:51:30.197",
                    "ra": "00:08:34.539",
                    "redshift": 0.022946,
                    "velocity": 6800.0,
                }
            },
        ),
        (
            "M1",
            "",
            {
                "equatorial": {
                    "dec": "",
                    "ra": "",
                    "redshift": None,
                    "velocity": None,
                }
            },
        ),
    ]

    def get_coordinates_generic(self, client, name, reference_frame, expected_response):
        base_url = "/ska-oso-pht-services/pht/api/v1/coordinates/"
        if not reference_frame:
            response = client.get(f"{base_url}{name}")
            assert response.status_code == HTTPStatus.NOT_FOUND
            return

        response = client.get(f"{base_url}{name}/{reference_frame}")
        assert response.status_code == HTTPStatus.OK
        assert json.loads(response.data.decode()) == expected_response

    def test_get_coordinates(self, client):
        for data in self.test_cases:
            self.get_coordinates_generic(client, *data)
