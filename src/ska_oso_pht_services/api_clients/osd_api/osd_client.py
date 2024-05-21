import json

import requests

import os

osd_api_url = os.environ['OSD_API_URL']
print('osd_api_url', osd_api_url)

SKA_OSD_API_URL = "http://192.168.49.2/ska-ost-osd/osd/api/v1/osd"


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

    response = requests.get(f"{SKA_OSD_API_URL}?cycle_id={cycle_id}")
    if response.status_code == 200:
        # Successful response
        data = json.loads(response.text)
        return data
    elif response.status_code == 404:
        # Resource not found
        raise APIError(f"Requested resource not found: {response.status_code}")
    else:
        # Other error occurred
        raise APIError(f"An error occurred: {response.status_code}")
