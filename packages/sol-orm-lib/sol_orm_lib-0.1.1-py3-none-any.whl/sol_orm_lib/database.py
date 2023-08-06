import os
import requests
import models

DB_API_URL = os.getenv("DB_API_URL")

# =========================================================================== #
#  TICs
# =========================================================================== #
def post_tics_data(data: models.TICs):
    response = requests.post(f"{DB_API_URL}/TICs", json=data.model_dump())
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")
    return response.json()

