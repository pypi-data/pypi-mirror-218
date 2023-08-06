import os
import requests

test_url = os.getenv("TEST_URL")


class URLWrapperClass:
    # def __init__(self, api_key):
    #     self.api_key = api_key
    #     self.base_url = "https://api.example.com"

    def wrap_url(config, payload):
        config_data = config
        headers = {
            "Content-Type": "application/json",
            "Authorization": "None",
        }
        requestOptions = {
            "method": "GET",
            "headers": headers,
        }

        response = requests.get(test_url, **requestOptions)
        response.raise_for_status()
        response_data = {
            "response": response,
            "config": config_data,
            "payload": payload,
        }
        return response_data
