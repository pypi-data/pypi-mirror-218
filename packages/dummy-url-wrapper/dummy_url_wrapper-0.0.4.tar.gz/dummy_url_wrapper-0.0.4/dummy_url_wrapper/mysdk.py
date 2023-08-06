import os
import requests
from dotenv import load_dotenv


test_url = os.getenv("TEST_URL")


class URLWrapperClass:
    def __init__(self, env_path=None):
        load_dotenv()

    def wrap_url(config, payload):
        config_data = config
        headers = {
            "Content-Type": "application/json",
            "Authorization": "None",
        }
        requestOptions = {
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
