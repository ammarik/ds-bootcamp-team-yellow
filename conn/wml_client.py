"""
This is the module to connect to the WML instance
"""

import logging
import requests
import typing as th

from utils.get_logger import get_logger
from utils.get_config import get_api_key, get_endpoint

logger: logging.Logger = get_logger()


class WMLClient:
    """
    This is the class to deal with all the communication with the WML endpoint
    """

    def __init__(self) -> None:
        """
        Set up all the tokens and headers required for the WML endpoint

        NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
        We either retrieve it from a local config when using locally or a secret set in OC

        """
        # get the api key from local config or from secret
        self.API_KEY = get_api_key()
        self.token_response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={
                "apikey": self.API_KEY,
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            },
        )
        self.mltoken = self.token_response.json()["access_token"]
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.mltoken,
        }
        logger.info("Connected to WML succesfully!")

    # TODO change input fields and default input fields
    def get_predictions(
        self,
        array_of_input_fields: th.List = ["users"],
        array_of_values_to_be_scored: th.List = [12],  # if user is logged in
        # default user --> cold start user
        another_array_of_values_to_be_scored: th.List = [-1],
    ) -> th.Dict:
        """
        Sends a payload to the endpoint, returns a response

        """
        logger.info("Getting predictions")
        # send the payload
        payload_scoring = {
            "input_data": [
                {
                    "fields": array_of_input_fields,
                    "values": [
                        array_of_values_to_be_scored,
                        another_array_of_values_to_be_scored,
                    ],
                }
            ]
        }

        # get the response
        response_scoring = requests.post(
            get_endpoint(),
            json=payload_scoring,
            headers={"Authorization": "Bearer " + self.mltoken},
        )

        # finally, return the response
        logger.info("Scoring response")
        logger.info(response_scoring.json())
        return response_scoring.json()


# NOTE for testing purpose only - if you want to test connection then run this
if __name__ == "__main__":
    test_class = WMLClient()
    test_class.get_predictions(["users"], [12], [-1])
