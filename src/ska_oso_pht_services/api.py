"""
These functions map to the API paths, with the returned value being the API response

Connexion maps the function name to the operationId in the OpenAPI document path
"""

import json
import logging
import os.path
import traceback
from functools import wraps
from http import HTTPStatus
from typing import Callable, Tuple, Union

from ska_oso_pdm.generated.models.sb_definition import SBDefinition

Response = Tuple[Union[SBDefinition], int]

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


def error_handler(api_fn: Callable[[str], Response]) -> Callable[[str], Response]:
    """
    A decorator function to catch general errors and wrap in the correct HTTP response,
    otherwise Flask just returns a generic error messgae which isn't very useful.

    :param api_fn: A function which an HTTP request is mapped
        to and returns an HTTP response
    """

    @wraps(api_fn)
    def wrapper(*args, **kwargs):
        try:
            return api_fn(*args, **kwargs)
        except Exception as err:  # pylint: disable=broad-except
            return error_response(err)

    return wrapper


@error_handler
def hello_world() -> Response:
    """
    Function that requests to /hello-world are mapped to
    """
    return "Hello, world!"


@error_handler
def proposal_get() -> Response:
    """
    Function that requests to /proposal are mapped to
    """
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
def proposal_edit() -> Response:
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


def error_response(err: Exception) -> Response:
    """
    Creates a general sever error response, without exposing internals to client

    :return: HTTP response server error
    """
    LOGGER.exception("Exception occurred while executing API function")
    response_body = {
        "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        "title": "Internal Server Error",
        "detail": str(err.args),
        "traceback": {
            "key": err.args[0],
            "type": str(type(err)),
            "full_traceback": traceback.format_exc(),
        },
    }

    return response_body, HTTPStatus.INTERNAL_SERVER_ERROR
