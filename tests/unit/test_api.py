"""
Unit tests for ska_oso_pht_services.api
"""


from http import HTTPStatus
import datetime
from unittest import mock

from .util import (
    VALID_MOCKED_DATA_JSON,
    VALID_MOCKED_DATA_LIST_JSON,
    assert_json_is_equal,
)


def test_proposal_get(client):
    result = client.get(
        "/ska-oso-pht-services/pht/api/v1/proposals/prp-00001"
    )

    assert result.status_code == HTTPStatus.OK
    assert_json_is_equal(result.text, VALID_MOCKED_DATA_JSON)


def test_proposal_get_list(client):
    result = client.get("/ska-oso-pht-services/pht/api/v1/proposals/list")

    assert result.status_code == HTTPStatus.OK
    assert_json_is_equal(result.text, VALID_MOCKED_DATA_LIST_JSON)


# def test_proposal_create(client):
#     result = client.post("/ska-oso-pht-services/pht/api/v1/proposals", data={})

#     assert result.status_code == HTTPStatus.OK
#     assert result.text == f"prsl-t0001-{datetime.datetime.today().strftime('%Y%m%d')}-00002"
    
# @mock.patch("ska_oso_pht_services.api.oda")
# def test_proposal_create_with_mock(mock_oda, client):
#     """
#     Check the proposal_create method returns the expected prsl_id and status code
#     """
    
#     now = datetime.datetime.now()
#     with mock.patch("ska_oso_pht_services.api.datetime") as mock_datetime:
#         mock_datetime.datetime.now.return_value = now

#         with mock.patch(
#             "ska_oso_pht_services.api.SkuidClient", autospec=True
#         ) as mock_skuidclient_cls:
#             instance = mock_skuidclient_cls.return_value
#             # random ID to return as a fake PRSL ID by the mock SKUID client
#             prsl_id = "foo"
#             instance.fetch_skuid.return_value = prsl_id

#             response = client.post("/ska-oso-pht-services/pht/api/v1/proposals", data={})
            
#         assert response.status_code == HTTPStatus.OK
#         assert response.text == prsl_id

def test_proposal_edit(client):
    result = client.put(
        "/ska-oso-pht-services/pht/api/v1/proposals/prsl-00001",
        data={},
    )

    assert result.status_code == HTTPStatus.OK
    assert result.text == "put /proposals"


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
