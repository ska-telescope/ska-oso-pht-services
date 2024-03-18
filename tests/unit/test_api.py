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


# def test_get_coordinates(client):
#     name = "LHS337"
#     reference_frame = "any"
#     response = client.get(
#         f"/ska-oso-pht-services/pht/api/v1/coordinates/{name}/{reference_frame}"
#     )

#     assert response.status_code == HTTPStatus.OK
#     expected_response = {
#         "equatorial": {
#             "declination": "-38:22:53.670",
#             "right_ascension": "12:38:49.098",
#         }
#     }
#     assert json.loads(response.data.decode()) == expected_response


class TestGetCoordinates:
    test_cases = [
        (
            "LHS337",
            "any",
            {
                "equatorial": {
                    "right_ascension": "12:38:49.098",
                    "declination": "-38:22:53.670",
                }
            },
        ),
        (
            "M31",
            "test",
            {
                "equatorial": {
                    "right_ascension": "00:42:44.330",
                    "declination": "+41:16:07.500",
                }
            },
        ),
        (
            "NGC253",
            "any",
            {
                "equatorial": {
                    "right_ascension": "00:47:33.134",
                    "declination": "-25:17:19.680",
                }
            },
        ),
        ("N10", "galactic", {"galactic": {"latitude": -78.5856, "longitude": 354.21}}),
        (
            "N10",
            "equatorial",
            {
                "equatorial": {
                    "declination": "-33:51:30.197",
                    "right_ascension": "00:08:34.539",
                }
            },
        ),
        ("M1", "", {"equatorial": {"declination": "", "right_ascension": ""}}),
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

    def test_coordinates(self, client):
        for data in self.test_cases:
            self.get_coordinates_generic(client, *data)
