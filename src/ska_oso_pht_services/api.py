"""
These functions map to the API paths, with the returned value being the API response

Connexion maps the function name to the operationId in the OpenAPI document path
"""

import logging
import traceback
from functools import wraps
from http import HTTPStatus
from typing import Callable, Tuple, Union

from ska_oso_pdm.generated.models.sb_definition import SBDefinition

Response = Tuple[Union[SBDefinition], int]

LOGGER = logging.getLogger(__name__)


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
