import requests

def send_query_to_endpoint(query):
    endpoint_url = 'https://your-api-endpoint.com/query'
    payload = {'query': query}

    try:
        response = requests.post(endpoint_url, json=payload)
        if response.status_code == 200:
            # Handle successful response
            print("Query sent successfully")
            print("Response:", response.json())  # If expecting JSON response
        else:
            # Handle unsuccessful response
            print("Failed to send query. Status code:", response.status_code)
            print("Error:", response.text)
    except requests.exceptions.RequestException as e:
        # Handle connection errors or exceptions
        print("Connection Error:", e)

# Example usage:
query = "SELECT * FROM users WHERE id = 1"
send_query_to_endpoint(query)
