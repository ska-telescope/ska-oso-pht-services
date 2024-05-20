import json
import requests
#import yaml
# from os import getenv

# KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-ost-osd")
# OSD_URL = getenv(
#     "OSD_URL", f"http://ska-oso-pht-services:5000/{KUBE_NAMESPACE}"
# )
# print('OSD_URL', OSD_URL)




# Load the configuration value from the Helm chart values file
#with open("../../../charts/ska-oso-pht-services/values.yaml", "r") as f:
    #config = yaml.safe_load(f)

# Extract the OSD API endpoint URL from the configuration value
#osd_url = config["osd"]["apiUrl"]

#print('osd_url::: ', osd_url)


import yaml
from os import getenv

#with open("../../../charts/ska-oso-pht-services/values.yaml", "r") as f:
    #config = yaml.safe_load(f)

# Load the OSD API URL from the environment variables
KUBE_NAMESPACE = getenv("KUBE_NAMESPACE", "ska-ost-osd")
#osd_url = getenv("OSD_API_URL", f"http://ska-oso-pht-services:5000/{KUBE_NAMESPACE}/osd/api/v1/osd")
osd_url = getenv("OSD_API_URL", f"http://192.168.49.2/{KUBE_NAMESPACE}/osd/api/v1/osd")
#osd_url = config["osd"]["apiUrl"]
print('osd_url', osd_url)
#http://192.168.49.2/ska-ost-osd/osd/api/v1/osd?
#KUBE_NAMESPACE = os.getenv("KUBE_NAMESPACE", "ska-oso-pht-services")
#API_PATH = f"/{KUBE_NAMESPACE}/pht/api/v1"

SKA_OSD_API_URL = "http://192.168.49.2/ska-ost-osd/osd/api/v1/osd"

url_path = "/osd/api/v1/osd"
endpoint = "/osd"


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
    
    response = requests.get(f"{osd_url}?cycle_id={cycle_id}")
    #print('full url', f"{osd_url}{endpoint}?cycle_id={cycle_id}")
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
