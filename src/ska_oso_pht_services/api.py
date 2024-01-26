"""
These functions map to the API paths, with the returned value being the API response

Connexion maps the function name to the operationId in the OpenAPI document path
"""

import json
import logging
import os.path
from functools import wraps

from astroquery.exceptions import RemoteServiceError
from flask import jsonify

from ska_oso_pht_services.constants.model import ProposalDefinition
from ska_oso_pht_services.utils import coordinates

Response = ProposalDefinition

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
def hello_world() -> Response:
    """
    Function that requests to /hello-world are mapped to
    """
    return "Hello, world!"


@error_handler
def proposal_get(proposal_id: str) -> Response:
    """
    Function that requests to /proposal are mapped to
    """
    if proposal_id =="mock":
        data = {"pop":"good"}
    else:
        MOCKED_DATA = load_string_from_file("constants/data.json")
        data = json.loads(MOCKED_DATA)
    return data


@error_handler
def proposal_get_list() -> Response:
    """
    Function that requests to /proposal/list are mapped to
    """
    MOCKED_DATA = load_string_from_file("constants/data.json")
    data = json.loads(MOCKED_DATA)
    return [data for x in range(5)]


@error_handler
def proposal_create() -> Response:
    """
    Function that requests to /proposal are mapped to
    """
    return "post /proposal"


@error_handler
def proposal_edit(proposal_id: str) -> Response:
    """
    Function that requests to /proposal are mapped to
    """
    return "put /proposal"


@error_handler
def proposal_validate() -> Response:
    """
    Function that requests to /proposal/validate are mapped to
    """
    return "post /proposal/validate"


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
