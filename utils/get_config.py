"""
Script to get the api key needed to connect to WML
If running locally, it takes a key stored in a local config file
If running on OC, it takes the API key that is mounted as a secret
"""

import os
import json
import logging

from utils.get_logger import get_logger

logger: logging.Logger = get_logger()


def get_local_config_file() -> dict:
    """
    Read local config
    """
    # NOTE hard-coded for now
    config_path = "config/config.local.json"
    with open(config_path, "r") as json_data:
        local_config = json.loads(json_data.read())
    return local_config


def get_api_key() -> str:
    """
    Function for getting the API key
    """
    # Set ENV to LOCAL to read values directly from config file
    if os.getenv("ENV").upper() == "LOCAL":
        local_config = get_local_config_file()
        api_key = local_config["API_KEY"]
    # Not in local ENV, get API key from secret
    else:
        api_key = os.environ.get("API_KEY")
    return api_key


def get_endpoint() -> str:
    """
    Function for getting the endpoint to connect tos
    """
    # Set ENV to LOCAL to read values directly from config file
    if os.getenv("ENV").upper() == "LOCAL":
        local_config = get_local_config_file()
        endpoint = local_config["ENDPOINT"]
    # Not in local ENV, get API key from secret
    else:
        endpoint = os.environ.get("ENDPOINT")
    return endpoint


if __name__ == "__main__":
    get_api_key()
    get_endpoint()
