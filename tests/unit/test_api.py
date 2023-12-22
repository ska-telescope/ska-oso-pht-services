"""
Unit tests for ska_oso_pht_services.api
"""


from http import HTTPStatus

from .util import (
    VALID_MOCKED_DATA_JSON,
    VALID_MOCKED_DATA_LIST_JSON,
    assert_json_is_equal,
)


def test_hello_world(client):
    result = client.get("/ska-oso-pht-services/pht/api/v1/hello-world")

    assert result.status_code == HTTPStatus.OK
    assert result.text == "Hello, world!"


def test_proposal_get(client):
    result = client.get("/ska-oso-pht-services/pht/api/v1/proposal")

    assert result.status_code == HTTPStatus.OK
    assert_json_is_equal(result.text, VALID_MOCKED_DATA_JSON)


def test_proposal_get_list(client):
    result = client.get("/ska-oso-pht-services/pht/api/v1/proposal/list")

    assert result.status_code == HTTPStatus.OK
    assert_json_is_equal(result.text, VALID_MOCKED_DATA_LIST_JSON)


def test_proposal_edit(client):
    result = client.put("/ska-oso-pht-services/pht/api/v1/proposal", data={})

    assert result.status_code == HTTPStatus.OK
    assert result.text == "put /proposal"


def test_proposal_validate(client):
    result = client.post("/ska-oso-pht-services/pht/api/v1/proposal/validate", data={})

    assert result.status_code == HTTPStatus.OK
    assert result.text == "post /proposal/validate"


def test_upload_pdf(client):
    result = client.post("/ska-oso-pht-services/pht/api/v1/upload/pdf", data={})

    assert result.status_code == HTTPStatus.OK
    assert result.text == "post /upload/pdf"
