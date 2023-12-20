"""
Unit tests for ska_oso_pht_services.api
"""


from http import HTTPStatus


def test_hello_world(client):
    """
    TODO
    """

    result = client.get("/ska-oso-pht-services/pht/api/v1/hello-world")

    assert result.status_code == HTTPStatus.OK
    assert result.text == "Hello, world!!"


def test_proposal_edit(client):
    """
    TODO
    """

    result = client.put("/ska-oso-pht-services/pht/api/v1/proposal")

    assert result.status_code == HTTPStatus.OK
    assert result.text == "put /proposal"
