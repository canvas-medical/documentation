import os
import requests

from datetime import datetime, timedelta
from urllib.parse import urlencode

# we should get these from environment variables or a secure location at runtime, not in the code
CLIENT_ID = os.getenv("CANVAS_API_CLIENT_ID")
CLIENT_SECRET = os.getenv("CANVAS_API_CLIENT_SECRET")
FUMAGE_BASE_URL = os.getenv("FUMAGE_BASE_URL")

def get_new_auth_token():
    # Auth tokens are requested from the EMR instance, not the FHIR API.
    url = FUMAGE_BASE_URL.replace("fumage-", "")

    payload = urlencode(
        {
            "grant_type": "client_credentials",
            "client_id": f"{CLIENT_ID}",
            "client_secret": f"{CLIENT_SECRET}"
        }
    )
    headers = { "Content-Type": "application/x-www-form-urlencoded", }

    response = requests.request("POST", f"{url}/auth/token/", headers=headers, data=payload)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        expiration_date = datetime.now() + timedelta(seconds=response.json()["expires_in"])

        os.environ["CANVAS_API_ACCESS_TOKEN"] = access_token
        os.environ["CANVAS_ACESS_TOKEN_EXPIRATION_DATE"] = expiration_date.strftime("%m/%d/%y %H:%M:%S")

        return response.json()["access_token"]
    else:
        raise Exception(f"Could not acquire new auth token: {response.text}")

if __name__ == '__main__':
    access_token = os.getenv("CANVAS_API_ACCESS_TOKEN")
    if expiration_date := os.getenv("CANVAS_ACCESS_TOKEN_EXPIRATION_DATE"):
        expiration_date = datetime.strptime(expiration_date, "%m/%d/%y %H:%M:%S")
    else:
        expiration_date = datetime.now()

     # only request a new token when we do not have a token or the one we have has expired
    if not access_token or expiration_date <= datetime.now():
        access_token = get_new_auth_token()

    headers = { "Authorization": f"Bearer {access_token}" }

    response = requests.request("GET", f"{FUMAGE_BASE_URL}/Patient?name=Briddle", headers=headers)

    if response.status_code == 401:
        # attempt to acquire a new token 1 time if we get a 401 - maybe it was manually expired or
        # we have the wrong expiration date
        access_token = get_new_auth_token()
        headers = { "Authorization": f"Bearer {access_token}" }
        response = requests.request("GET", f"{FUMAGE_BASE_URL}/Patient?name=Briddle", headers=headers)

        if response.status_code == 401:
            # limit retries but throw a specific exception for authentication related issues
            raise Exception(f"Cannot authenticate to Canvas after 1 retry: {response.text}")
        elif response.status_code != 200:
            # capture other issues as well
            raise Exception(f"{response.text}")

    patients = response.json()["entry"]
    for patient in patients:
        patient_id = patient["resource"]["id"]
        response = requests.request("GET", f"{FUMAGE_BASE_URL}/Appointment?patient=Patient/{patient_id}")

        # do something with the appointments - save locally, modify and update, etc.