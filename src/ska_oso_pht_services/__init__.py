"""
ska_oso_pht_services
"""

import os
from typing import Any, Dict

import prance
from connexion import App
from flask import Flask, Response
from ska_db_oda.rest.flask_oda import FlaskODA

KUBE_NAMESPACE = os.getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
API_PATH = f"/{KUBE_NAMESPACE}/pht/api/v1"

oda = FlaskODA()


def resolve_openapi_spec() -> Dict[str, Any]:
    """
    Resolves the $ref in the OpenAPI spec before it is used by Connexion,
    as Connexion can't parse them.
    See https://github.com/spec-first/connexion/issues/967
    """
    cwd, _ = os.path.split(__file__)
    path = os.path.join(cwd, "./openapi/pht-openapi-v1.yaml")
    parser = prance.ResolvingParser(path, lazy=True, strict=True)
    parser.parse()
    return parser.specification


class CustomRequestBodyValidator:  # pylint: disable=too-few-public-methods
    """
        There is a (another) issue with Connexion where it cannot validate against a
        spec with polymorphism, like the SBDefinition.
    See https://github.com/spec-first/connexion/issues/1569
    As a temporary hack, this basically turns off the validation
    """

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, function):
        return function


def set_default_headers_on_response(response: Response) -> Response:
    """
    Set default headers on the Flask response object
    """
    # Set CORS headers
    response.headers["Access-Control-Allow-Origin"] = (
        "*"  # solves POST request issue in frontend
    )
    #
    # TODO: once app more mature and login capability in place,
    # may need to modify setting bellow accordingly for better security
    #
    response.headers["Access-Control-Allow-Methods"] = (
        "*"  # solves PUT request issue from frontend
    )
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Authorization"  # solves POST request issue from frontend
    )
    return response


def create_app(open_api_spec=None) -> App:
    """
    Create the Connexion application with required config
    """

    if open_api_spec is None:
        open_api_spec = resolve_openapi_spec()

    app = App(__name__, specification_dir="openapi/")

    validator_map = {
        "body": CustomRequestBodyValidator,
    }
    app.add_api(
        open_api_spec,
        arguments={"title": "OpenAPI PHT"},
        # The base path includes the namespace which is known at runtime
        # to avoid clashes in deployments, for example in CICD
        base_path=API_PATH,
        pythonic_params=True,
        validator_map=validator_map,
    )

    oda.init_app(app.app)

    app.app.after_request(set_default_headers_on_response)

    return app
