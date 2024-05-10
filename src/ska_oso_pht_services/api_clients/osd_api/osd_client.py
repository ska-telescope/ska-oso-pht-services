import json
import requests

SKA_OSD_API_URL = "http://192.168.49.2/ska-ost-osd"

class APIError(Exception):
    pass

def get_osd(cycle_id):
    """
    get osd data
    """
    url_path = f"/osd/api/v1/osd"
    response = requests.get(f"{SKA_OSD_API_URL}{url_path}?cycle_id={cycle_id}")
    if response.status_code == 200:
        # Successful response
        print('Request was successful')
        # ... Handle the response data
        data = json.loads(response.text)
        return data
    elif response.status_code == 404:
        # Resource not found
        raise APIError("Requested resource not found")
    else:
        # Other error occurred
        raise APIError(f"An error occurred: {response.status_code}")
