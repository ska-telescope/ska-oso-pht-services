import json
import requests

api_url = "http://192.168.49.2/ska-ost-osd/osd/api/v1/osd?cycle_id=1&osd_version=1.0.0&source=file&capabilities=mid"

def get_osd():
    """
    Create something
    """
    print('::: in get_something()')
    response = requests.get(api_url)
    if response.status_code == 200:
        # Successful response
        print('Request was successful')
        # ... Handle the response data
        data = json.loads(response.text)
        print(data)
        print('###### test #####', data['capabilities']['mid']['AA2']['available_bandwidth_hz'])
    elif response.status_code == 404:
        # Resource not found
        print('Requested resource not found')
    else:
        # Other error occurred
        print('An error occurred:', response.status_code)
