"""
These functions map to the API paths, with the returned value being the API response

Connexion maps the function name to the operationId in the OpenAPI document path
"""

import json
import logging
import os.path
import datetime
from functools import wraps
from http import HTTPStatus

from astroquery.exceptions import RemoteServiceError
from flask import jsonify
from ska_oso_pdm.generated.models.metadata import Metadata
from ska_oso_pdm.generated.models.proposal import Proposal, ProposalInfo
from ska_oso_pdm.generated.models.proposal_info import (
    Investigators,
    ProposalInfoProposalType,
    ScienceProgrammes,
    Targets,
)
from ska_ser_skuid.client import SkuidClient
from ska_oso_pdm.openapi import CODEC as OPENAPI_CODEC

from ska_oso_pht_services import oda
from ska_oso_pht_services.utils import coordinates

from ska_db_oda.domain.query import DateQuery, MatchType, UserQuery

Response = Proposal

LOGGER = logging.getLogger(__name__)

# The real SKUID URL depends on Kubernetes namespace and Helm release and is
# set at deployment time in the configmap
SKUID_URL = os.environ.get("SKUID_URL", "http://ska-ser-skuid-test-svc:9870")


def load_string_from_file(filename):
    """
    Return a file from the current directory as a string
    """
    cwd, _ = os.path.split(__file__)
    path = os.path.join(cwd, filename)
    with open(path, "r", encoding="utf-8") as json_file:
        json_data = json_file.read()
        return json_data


def error_handler(api_func):
    """
    A decorator that wraps the passed in function and executes it.
    Any unhandled exceptions that are raised within the function are caught
    and handled by returning a JSON response with an appropriate error message
    and HTTP status code.

    Args:
        f (function): The function to be wrapped by the decorator.

    Returns:
        function: The decorated function which includes error handling.
    """

    @wraps(api_func)
    def decorated_function(*args, **kwargs):
        try:
            return api_func(*args, **kwargs)
        except RemoteServiceError as ve:
            return (
                jsonify(
                    {
                        "error": "Get Coordinates Value Error",
                        "status": 400,
                        "message": str(ve),
                    }
                ),
                400,
            )
        except ValueError as ve:
            return (
                jsonify({"error": "Value Error", "status": 400, "message": str(ve)}),
                400,
            )
        except Exception as e:  # pylint: disable=broad-except
            return (
                jsonify(
                    {"error": "Internal Server Error", "status": 500, "message": str(e)}
                ),
                500,
            )

    return decorated_function


@error_handler
def proposal_get(identifier: str) -> Response:
    """
    Function that requests to /proposals are mapped to
    """

    try:
        LOGGER.debug("GET PROPOSAL prsl_id: %s", identifier)
        with oda.uow as uow:
            prsl = uow.prsls.get(identifier)
        return prsl.to_dict(), HTTPStatus.OK
    except KeyError:
        LOGGER.exception("KeyError when adding Proposal to the ODA")
        return (
            {"error": f"Proposal with ID {identifier} not found "},
            HTTPStatus.NOT_FOUND,
        )



@error_handler
def proposal_get_list(identifier: str) -> Response:
    """
    Function that requests to /proposals/list are mapped to
    currently only search for User Equals
    """

    try:
        LOGGER.debug("GET PROPOSAL LIST query: %s", identifier)
        with oda.uow as uow:
            query_param = UserQuery(user=identifier, match_type=MatchType.EQUALS)
            prsl = uow.prsls.query(query_param)
        return [x.to_dict() for x in prsl] , HTTPStatus.OK
    except KeyError:
        LOGGER.exception("KeyError when adding Proposal to the ODA")
        return (
            {"error": f"Proposal List with query {identifier} not found "},
            HTTPStatus.NOT_FOUND,
        )


@error_handler
def proposal_create(body) -> Response:
    """
    Function that requests to /proposals are mapped to
    """
    LOGGER.debug("POST PROPOSAL create")
    try:        
        prsl = OPENAPI_CODEC.loads(
            Proposal, json.dumps(body)
        )
        with oda.uow as uow:
            updated_prsl = uow.prsls.add(prsl)
            uow.commit()
        return (
            updated_prsl.prsl_id,
            HTTPStatus.OK,
        )
    except ValueError as err:
        LOGGER.exception("ValueError when adding Proposal to the ODA")
        return (
            {"error": f"Bad Request '{err.args[0]}'"},
            HTTPStatus.BAD_REQUEST,
        )


@error_handler
def proposal_edit(proposal_id: str) -> Response:
    """
    Function that requests to /proposals are mapped to
    """
    return "put /proposals"


@error_handler
def proposal_validate() -> Response:
    """
    Function that requests to /proposals/validate are mapped to
    """
    return "post /proposals/validate"


@error_handler
def upload_pdf() -> Response:
    """
    Function that requests to /upload/pdf are mapped to
    """
    return "post /upload/pdf"


@error_handler
def get_coordinates(identifier: str) -> Response:
    """
    Function that requests to /coordinates are mapped to
    """

    return coordinates.get_coordinates(identifier)