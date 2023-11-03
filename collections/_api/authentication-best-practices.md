---
title: "Authentication - Best Practices"
layout: apipage
---

## Introduction

The Oauth 2.0 authentication/authorization flow differs from the traditional username/password flow
still heavily used in healthcare interoperability.  To help users new to writing applications using 
Oauth, here are some best practices recommended by Canvas.

### The Access Token: Don't lose it, reuse it

#### Don't do this

For some connections requiring a username and password, it may be necessary to use those credentials
every time a message is sent to that system.  In that type of flow, you might need to write 
something like:

```text
# psuedocode only

authenticate()
patient = read_patient()

updated_patient = update_patient(patient, name="Frank")

authenticate()
update_patient(updated_patient)

...
```

#### Do this instead

Regardless of the authentication method used, a successful request includes `"expires_in": ` in the
response body.  The value will be some integer value like 36000, which is the number of seconds until
that token will be set to expired in Canvas.  Processing time is reduced and the system is more 
secure when re-using the non-expired access token instead of always requesting a new one first:
  - **Client Credentials** flow:  
    - store the access token and expiration datetime as securely as the client id and secret
    - only request a new token when the current time is past the expiration datetime
  - **Authorization Code** flow:
    - securely store the access token and expiration datetime during the user's session
    - only request an access token at the beginning of a user's session
    - consider using the refresh token when the access token needs to be renewed

Now, your code can be more like:

```text
# psuedocode only

authenticate() if needed else resuse access_token
patient = read_patient()
updated_patient = update_patient(patient, name="Frank")
update_patient(updated_patient)

```

There's any number of ways to do this in your language of choice.  Here is an oversimplified way in
Python (for example purposes only - far from the best implementation):

```python
import os
import requests

from datetime import datetime, timedelta

# we should get these from environment variables or a secure location at runtime, not in the code
CLIENT_ID = os.getenv("CANVAS_API_CLIENT_ID")
CLIENT_SECRET = os.getenv("CANVAS_API_CLIENT_SECRET")

# These should be securely stored as well so you can reuse the token later or know when to request again
access_token = os.getenv("CANVAS_API_ACCESS_TOKEN")
if expiration_date := os.getenv("CANVAS_ACCESS_TOKEN_EXPIRATION_DATE"):
    expiration_date = datetime.strptime(expiration_date, "%m/%d/%y %H:%M:%S")
else:
    expiration_date = datetime.now()

if not access_token or expiration_date <= datetime.now():
    # only request a new token when we do not have a token or the one we have has expired
    payload = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    headers = { "Content-Type": "application/x-www-form-urlencoded", }

    response = requests.request("POST", "http://localhost:8000/auth/token/", headers=headers, data=payload)
    access_token = response.json()["access_token"]
    expiration_date = datetime.now() + timedelta(seconds=response.json()["expires_in"])

    os.environ["CANVAS_API_ACCESS_TOKEN"] = access_token
    os.environ["CANVAS_ACESS_TOKEN_EXPIRATION_DATE"] = expiration_date.strftime("%m/%d/%y %H:%M:%S")

headers = { "Authorization": f"Bearer {access_token}" }

response = requests.request("GET", "http://localhost:8888/Patient?name=Briddle", headers=headers, data=payload)
patients = response.json()["entry"]
for patient in patients:
    patient_id = patient["resource"]["id"]
    
    appointments = requests.request("GET", f"http://localhost:8888/Appointment?patient=Patient/{patient_id}")
    # do something with the appointments - save locally, modify and update, etc.

```

#### Takeaway:
Safely stored access tokens can and should be reused!!!<br>
Additional reading:
- [Token Best Practices from Auth0](https://auth0.com/docs/secure/tokens/token-best-practices)