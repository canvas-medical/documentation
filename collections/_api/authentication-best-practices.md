---
title: "Authentication - Best Practices"
layout: apipage
author: "Josh Myers"
---

## Introduction

The OAuth 2.0 authentication/authorization flow differs from the traditional username/password flow
still heavily used in healthcare interoperability.  To help users new to writing applications using 
OAuth, here are some best practices recommended by Canvas.

### The Access Token: Don't lose it, reuse it

#### Instead of this

For some connections requiring a username and password, it may be necessary to use those credentials
every time a message is sent to that system.  In that type of flow, you might need to write 
something like:

```python
import requests

token = get_new_auth_token()
patient = get_patient(token, patient_id)

updated_patient_body = update_patient(patient, name="Frank")

token = get_new_auth_token()
update_patient(token, updated_patient_body)

token = get_new_auth_token()
schedule_appointment(token, patient=patient, type="telehealth")

...
```

Repeated, unnecessary calls to a token request function double the number of requests this script
generates.

#### Do this

Regardless of the authentication method used, a successful request includes `"expires_in": ` in the
response body.  The corresponding value will be an integer for the number of seconds until
the token will be expired in Canvas.  By reusing the token and eliminating redundant token requests,
there is a **performance** gain from reducing the overall number of requests. The system is also more
**secure** - having fewer tokens reduces the overall surface area for illegitamate access

**General Guidelines:**
- store the access token as securely as the client id and secret
- depending on your use case, it may be best to store a token just for that session or to reuse
    it until it nears expiration
- store the expiration datetime as well and check it before requesting a new token
- use a refresh token if you provided in the authentication response for the authentication flow being used

There's any number of ways to do this in your language of choice.  In Python, your code may look more like:

```python
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

```

#### Takeaway
- **Safely stored access tokens can and should be reused!**<br>
- Additional reading:
    - [Token Best Practices from Auth0](https://auth0.com/docs/secure/tokens/token-best-practices)