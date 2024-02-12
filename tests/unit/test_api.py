"""
Unit tests for ska_oso_pht_services.api
"""


from http import HTTPStatus
import datetime
from unittest import mock

from .util import (
    VALID_MOCKED_DATA_JSON,
    VALID_MOCKED_DATA_LIST_JSON,
    VALID_PROPOSAL_DATA_JSON,
    assert_json_is_equal,
)


# def test_proposal_get(client):
#     result = client.get(
#         "/ska-oso-pht-services/pht/api/v1/proposals/prsl-123"
#     )

#     assert result.status_code == HTTPStatus.OK
#     assert_json_is_equal(result.text, VALID_MOCKED_DATA_JSON)


# def test_proposal_get_list(client):
#     result = client.get("/ska-oso-pht-services/pht/api/v1/proposals/list/DefaultUser")

#     assert result.status_code == HTTPStatus.OK
#     assert_json_is_equal(result.text, VALID_MOCKED_DATA_LIST_JSON)


def test_proposal_create(client):
    result = client.post("/ska-oso-pht-services/pht/api/v1/proposals", data={})

    assert result.status_code == HTTPStatus.OK
    assert result.text == f"prsl-t0001-{datetime.datetime.today().strftime('%Y%m%d')}-00002"
    
@mock.patch("ska_oso_pht_services.api.oda")
def test_proposal_create_with_mock(mock_oda, client):
    """
    TODO: learn pytest mock data
    Check the proposal_create method returns the expected prsl_id and status code
    """
    
    uow_mock = mock.MagicMock()
    uow_mock.prsls.add.return_value = None
    uow_mock.prsls.get.return_value = f"prsl-t0001-{datetime.datetime.today().strftime('%Y%m%d')}-00002"
    mock_oda.uow.__enter__.return_value = uow_mock
    
    response = client.post(
        "/ska-oso-pht-services/pht/api/v1/proposals", 
        data=VALID_PROPOSAL_DATA_JSON,
        headers={"Content-type": "application/json"},
    )
            
    assert response.status_code == HTTPStatus.OK
    assert response.text == f"prsl-t0001-{datetime.datetime.today().strftime('%Y%m%d')}-00002"

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
