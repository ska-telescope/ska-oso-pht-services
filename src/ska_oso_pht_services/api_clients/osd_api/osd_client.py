import json
import requests

api_url = "https://jsonplaceholder.typicode.com/todos/1"

def get_something():
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
        print(data['title'])
    elif response.status_code == 404:
        # Resource not found
        print('Requested resource not found')
    else:
        # Other error occurred
        print('An error occurred:', response.status_code)
