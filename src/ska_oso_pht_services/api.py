"""
These functions map to the API paths, with the returned value being the API response

Connexion maps the function name to the operationId in the OpenAPI document path
"""

import json
import logging
import os.path
from functools import wraps
from http import HTTPStatus

from astroquery.exceptions import RemoteServiceError
from flask import jsonify
from ska_db_oda.domain.query import MatchType, UserQuery
from ska_oso_pdm import Proposal

from ska_oso_pht_services import oda
from ska_oso_pht_services.connectors.pht_handler import (
    transform_create_proposal,
    transform_update_proposal,
)
from ska_oso_pht_services.utils import (  # pylint: disable=W0611
    coordinates,
    s3_bucket,
    validation,
)

Response = Proposal

LOGGER = logging.getLogger(__name__)


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
    Function that requests to GET /proposals are mapped to

    Retrieves the Proposal with the given identifier from the
    underlying data store, if available

    :param identifier: identifier of the Proposal
    :return: a tuple of an Proposal and a
        HTTP status, which the Connexion will wrap in a response
    """

    try:
        LOGGER.debug("GET PROPOSAL prsl_id: %s", identifier)
        with oda.uow as uow:
            retrieved_prsl = uow.prsls.get(identifier)
        # TODO: revisit Url is not JSON serializable error using model_dump()
        return json.loads(retrieved_prsl.model_dump_json()), HTTPStatus.OK
    except KeyError:
        LOGGER.exception("KeyError when adding Proposal to the ODA")
        return (
            {"error": f"Proposal with ID {identifier} not found "},
            HTTPStatus.NOT_FOUND,
        )


@error_handler
def proposal_get_list(identifier: str) -> Response:
    """
    Function that requests to GET /proposals/list are mapped to

    Retrieves the Proposals with the given identifier as a user query from the
    underlying data store, if available

    :param identifier: identifier of the Proposal
    :return: a tuple of a list of Proposal and a
        HTTP status, which the Connexion will wrap in a response
    """

    try:
        LOGGER.debug("GET PROPOSAL LIST query: %s", identifier)
        with oda.uow as uow:
            query_param = UserQuery(user=identifier, match_type=MatchType.EQUALS)
            prsl = uow.prsls.query(query_param)
        # TODO: revisit Url is not JSON serializable error using model_dump()
        return [json.loads(x.model_dump_json()) for x in prsl], HTTPStatus.OK
    except KeyError:
        LOGGER.exception("KeyError when adding Proposal to the ODA")
        return (
            {"error": f"Proposal List with query {identifier} not found "},
            HTTPStatus.NOT_FOUND,
        )


@error_handler
def proposal_create(body) -> Response:
    """
    Function that requests to POST /proposals are mapped to

    Stores the Proposal in the underlying data store.

    The ODA is responsible for populating the prsl_id and metadata

    :param identifier: identifier of the Proposal
    :return: a tuple of an Proposal as it exists in the ODA or error
        response and a HTTP status, which the Connexion will wrap in a response
    """
    LOGGER.debug("POST PROPOSAL create")

    try:
        transform_body = transform_create_proposal(body)

        prsl = Proposal.model_validate(transform_body)  # test transformed

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
def proposal_edit(body: dict, identifier: str) -> Response:
    """
    Function that requests to PUT /proposals are mapped to

    Stores the Proposal with the given identifier
    in the underlying data store.

    :param identifier: identifier of the Proposal
    :return: a tuple of an Proposal or error response and a HTTP status,
        which the Connexion will wrap in a response
    """
    LOGGER.debug("PUT PROPOSAL edit prsl_id: %s", identifier)

    try:
        transform_body = transform_update_proposal(body)

        prsl = Proposal.model_validate(transform_body)  # test transformed

        if prsl.prsl_id != identifier:
            return (
                {"error": "Unprocessable Entity, mismatched Proposal ID"},
                HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        with oda.uow as uow:
            persisted_prsl =uow.prsls.add(prsl)
            uow.commit()
            
        return persisted_prsl, HTTPStatus.OK

    except ValueError as err:
        LOGGER.exception("ValueError when adding Proposal to the ODA")
        return (
            {"error": f"Bad Request '{err.args[0]}'"},
            HTTPStatus.BAD_REQUEST,
        )


@error_handler
def proposal_validate(body: dict) -> Response:  # pylint: disable=W0613
    """
    Function that requests to dummy endpoint POST /proposals/validate are mapped to

    Input Parameters: None

    Returns:
    a tuple of a boolean of result and
        an array of message if result is False
    """
    LOGGER.debug("POST PROPOSAL validate")

    try:
        # TODO: remove mocked result after refactoring validate function
        # and remove pylint disable
        # result = validation.validate_proposal(body)

        result = {"result": True, "validation_errors": []}
        return (
            result,
            HTTPStatus.OK,
        )
    except ValueError as err:
        LOGGER.exception("ValueError when validaing proposal")
        return (
            {"error": f"Bad Request '{err.args[0]}'"},
            HTTPStatus.BAD_REQUEST,
        )


@error_handler
def upload_pdf(filename: str) -> Response:
    """
    Function that requests to endpoint GET /upload/signedurl/{filename}
    are mapped to

    :param filename: filename of the uploaded document
    :return: a string "/upload/signedurl/{filename}"
    """
    LOGGER.debug("GET Upload Signed URL")
    s3_client = s3_bucket.get_aws_client()
    upload_signed_url = s3_bucket.create_presigned_url_upload_pdf(
        filename, s3_client, 60
    )

    return (
        upload_signed_url,
        HTTPStatus.OK,
    )


@error_handler
def download_pdf(filename: str) -> Response:
    """
    Function that requests to endpoint GET /download/signedurl/{filename}
    are mapped to

    :param filename: filename of the uploaded document
    :return: a string "/download/signedurl/{filename}"
    """
    LOGGER.debug("GET Download Signed URL")
    s3_client = s3_bucket.get_aws_client()
    download_signed_url = s3_bucket.create_presigned_url_download_pdf(
        filename, s3_client, 60
    )

    return (
        download_signed_url,
        HTTPStatus.OK,
    )


@error_handler
def get_systemcoordinates(identifier: str, reference_frame: str) -> Response:
    """
    Function that requests to /coordinates are mapped to

    Query celestial coordinates for a given object name from SIMBAD and NED databases.
    If the object is not found in SIMBAD database
    it then queries the NED (NASA/IPAC Extragalactic Database).

    :param identifier: A string representing the name of the object to query.
    :param reference_frame: A string representing the reference frame
    to return the coordinates in ("galactic" or "equatorial").
    :return: A dictionary with one key "equatorial" or "galactic",
             containing a nested dictionary with galactic or equatorial coordinates:
             {"galactic":
                {"latitude": 78.7068,"longitude": 42.217}
             } or {"equatorial":
                {"right_ascension": "+28:22:38.200",
                "declination": "13:41:11.620"}
             }
             In case of an error, an error response is returned.
    :rtype: dict
    """
    LOGGER.debug("POST PROPOSAL get coordinates: %s", identifier)
    response = coordinates.get_coordinates(identifier)
    if reference_frame.lower() == "galactic":
        return coordinates.convert_to_galactic(
            response["ra"], response["dec"], response["velocity"], response["redshift"]
        )
    else:
        return coordinates.round_coord_to_3_decimal_places(
            response["ra"], response["dec"], response["velocity"], response["redshift"]
        )
