import json
from os import getenv

import requests

# KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
OSD_API_URL = getenv(
    "OSD_API_URL",
    "http://ska-ost-osd-rest-test:5000/{KUBE_NAMESPACE}/osd/api/v1/osd",
)
# OSD_API_URL = getenv('OSD_API_URL')
print("OSD_API_URL", OSD_API_URL)

ODA_BACKEND_TYPE = getenv("ODA_BACKEND_TYPE")
print("ODA_BACKEND_TYPE", ODA_BACKEND_TYPE)

ODA_URL = getenv("ODA_URL")
print("ODA_URL", ODA_URL)

# SKA_OSD_API_URL = "http://192.168.49.2/ska-ost-osd/osd/api/v1/osd"


class APIError(Exception):
    pass


def get_osd(cycle_id):
    """
    Functionality:
    The get_osd function is used to fetch the OSD data for a specified cycle
    ID. It makes a GET request to the OSD API endpoint with the specified cycle
    ID as a query parameter. If the request is successful, it returns the OSD data
    in the form of a dictionary. If the requested resource is not found, it raises
    an APIError with an appropriate message. If any other error occurs, it raises
    an APIError with an appropriate message.

    Parameter:
    cycle_id (str): A string representing the cycle ID for which the OSD data
    is to be fetched.

    Returns:
    dict: A dictionary containing the OSD data for the specified cycle ID.

    Raises:
    APIError: If the requested resource is not found or any other error occurs.
    """

    response = requests.get(f"{OSD_API_URL}?cycle_id={cycle_id}")
    if response.status_code == 200:
        # Successful response
        data = json.loads(response.text)
        myobject = {
            "data": data,
            "OSD_API_URL": OSD_API_URL,
            "ODA_BACKEND_TYPE": ODA_BACKEND_TYPE,
            "ODA_URL": ODA_URL,
        }
        #return data
        return myobject
    elif response.status_code == 404:
        # Resource not found
        raise APIError(f"Requested resource not found: {response.status_code}")
    else:
        # Other error occurred
        raise APIError(f"An error occurred: {response.status_code}")
