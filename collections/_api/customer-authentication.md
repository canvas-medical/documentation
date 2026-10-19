---
title: "Customer Authentication"
layout: apipage
---

## Introduction

- Canvas is an OAuth 2.0 authorization server.
- This page contains information about how you can create third-party applications within your Canvas EHR instance and use those applications to access the FHIR API.
- Canvas supports most OAuth flows, but this document will focus on two of the most used:
  - **Client Credentials**: Mostly used for Machine-to-Machine authentication (e.g., CLIs, Daemons).
  - **Authorization Code**: Usually used for web/native applications since it requires a user to log in to the system.

## Registering a third-party application on Canvas

- Registering a third-party application is always the first step.
- To register, view, edit, or delete applications, you need the Administrative Developer or Clinical Developer role. Without one of these roles, the application pages below return `403 Forbidden`.
- Any user can review and revoke the tokens they approved for an application at `{YOUR_CANVAS_EHR_INSTANCE}/auth/authorized_tokens/`.
- In order to do so, you'll need to:
  1. Go to `{YOUR_CANVAS_EHR_INSTANCE}/auth/applications/` where you'll see the following page:
  <img src="/assets/images/ed67823-Screenshot_2021-10-26_at_16.22.31.png" alt="Authorization Page" style="width: 50%;" />


  2. Once you click the link on that page, you'll see the following:
  <img src="/assets/images/8b49344-Screenshot_2021-10-26_at_16.24.01.png" alt="Application Registration" style="width: 50%;" />


  - You'll need to set a name for the app, set the `Client type` to `Confidential`, choose one of the `Authorization grant types`, and set the `Redirect URIs` if needed. Leave the `Algorithm` at `No OIDC support` for now.
  - Here's how it should look if you created a new "Test Application" with the `client-credentials` grant type:
<img src="/assets/images/6190a01-Screenshot_2021-10-26_at_16.26.59.png" alt="Application Example" style="width: 50%;" />

  - That's it. Take note of your `Client ID` and `Client Secret`, and proceed to the section related to the `Authorization Grant Type` you chose.

## Client Credentials

- The Client Credentials flow assumes that everyone involved is capable of securely storing the `Client ID` and `Client Secret`.
- In order to get a token, you just need to:

```shell
curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id={YOUR_CLIENT_ID}' \
--data-urlencode 'client_secret={YOUR_CLIENT_SECRET}'
```

and you'll get back a JSON which will contain an `access_token` that'll be valid for 10 hours.

The `/api` endpoints check no scopes, and a client credentials token acts there with every permission of the application's owner. For that reason, a client credentials token must carry the `system/*.*` scope to call `/api`. Canvas refuses a token with narrower scopes there with `403 Forbidden`. The [Note API](/api/note/), the [Letter API](/api/letter/), and the plugin endpoints check scopes, so they accept narrower tokens.

### Authenticate with a signed JWT instead of a client secret

Your application can prove its identity with a short-lived JSON Web Token (JWT) that it signs with its own private key, instead of sending the `Client Secret`. Canvas verifies the signature against public keys that your application publishes. Your private key never leaves your system, and you rotate keys by updating the key set you publish. This is the client authentication method that [SMART Backend Services](https://hl7.org/fhir/smart-app-launch/backend-services.html) clients use, also called `private_key_jwt`.

Before you begin, you need:

- An application registered with the `client-credentials` grant type, as described in [Registering a third-party application on Canvas](#registering-a-third-party-application-on-canvas).
- A signing key pair: an EC key on the P-384 curve, which signs with `ES384`, or an RSA key, which signs with `RS384`. Canvas accepts no other signing algorithms.
- A JSON Web Key Set (JWKS) URL that serves your public key over HTTPS from a public address. Give each key in the set a `kid` (key ID).

#### Add your JWKS URL to the application

You add the JWKS URL after you register the application, because the registration form doesn't include it.

1. Go to `{YOUR_CANVAS_EHR_INSTANCE}/auth/applications/` and select your application.
2. Select **Edit**.
3. In **JSON Web Key Set URL**, enter your JWKS URL, such as `https://your-app.example.com/.well-known/jwks.json`.
4. Select **Save**.

Canvas fetches the key set from this URL each time it verifies an assertion, so a key you add to or remove from the set takes effect without changing the application. Canvas fetches it only under these conditions:

- The URL uses `https`, and its host resolves only to public IP addresses. Canvas refuses a URL that resolves to any non-public address, such as a private or loopback address.
- The URL returns the key set directly with `200 OK`. Canvas doesn't follow redirects.
- The full response arrives within 5 seconds and is no larger than 64 KB.

#### Build the client assertion

Sign a JWT with these header fields:

| Header field | Value |
|---|---|
| `alg` | `ES384` or `RS384`, matching your key. |
| `kid` | The key ID of the signing key in your JWKS. Canvas uses the key whose `kid` matches. That key's `use` must be `sig` or absent. |
| `jku` | Optional. If present, it must exactly match the application's **JSON Web Key Set URL**. |

The JWT must carry these claims:

| Claim | Value |
|---|---|
| `iss` | Your `Client ID`. |
| `sub` | Your `Client ID`, the same value as `iss`. |
| `aud` | The token endpoint URL, `{YOUR_CANVAS_EHR_INSTANCE}/auth/token/`, including the trailing slash. |
| `exp` | The expiration time, in seconds since the Unix epoch. Set it no more than five minutes after you create the assertion. |
| `jti` | A unique identifier for this assertion, up to 255 characters, such as a random UUID. |

Canvas rejects an assertion that is missing any of these claims. When it checks `exp`, and `iat` or `nbf` if you include them, Canvas allows up to 30 seconds of clock difference between your system and your Canvas instance. Canvas also rejects an assertion whose `exp` is more than 10 minutes in the future: the five-minute limit plus five minutes for clock difference.

Canvas accepts each `jti` only once, to prevent replay. It remembers a `jti` until five minutes after the assertion's `exp`, so create a new assertion with a new `jti` for every token request.

#### Request a token

Send the assertion to the token endpoint in place of the `client_secret`:

```shell
curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer' \
--data-urlencode 'client_assertion={SIGNED_JWT}' \
--data-urlencode 'scope={SCOPES}'
```

The `client_assertion_type` must be `urn:ietf:params:oauth:client-assertion-type:jwt-bearer`. Canvas returns `400 Bad Request` with an `invalid_request` error for any other value. The response matches a client credentials response that used a client secret. The same [scope rules](#scopes) apply.

The following Python example builds the assertion with [PyJWT](https://pyjwt.readthedocs.io/) and requests a token. It needs the `pyjwt`, `cryptography`, and `requests` packages, and reads the private key from a PEM file:

```python
import time
import uuid

import jwt
import requests

token_url = "{YOUR_CANVAS_EHR_INSTANCE}/auth/token/"
client_id = "{YOUR_CLIENT_ID}"

with open("private_key.pem") as key_file:
    private_key = key_file.read()

client_assertion = jwt.encode(
    {
        "iss": client_id,
        "sub": client_id,
        "aud": token_url,
        "exp": int(time.time()) + 300,
        "jti": str(uuid.uuid4()),
    },
    private_key,
    algorithm="ES384",  # Use "RS384" for an RSA key.
    headers={"kid": "{YOUR_KEY_ID}"},
)

response = requests.post(
    token_url,
    data={
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": client_assertion,
        "scope": "{SCOPES}",
    },
)
response.raise_for_status()
access_token = response.json()["access_token"]
```

If Canvas can't verify the assertion, it responds with `401 Unauthorized` and an `invalid_client` error. Check these causes:

- The `iss` doesn't match a registered `Client ID`, or `sub` differs from `iss`.
- The application has no **JSON Web Key Set URL**, or a `jku` header doesn't match it.
- Canvas can't fetch the key set. For example, the URL isn't `https`, resolves to a non-public address, redirects, takes longer than 5 seconds, or returns more than 64 KB.
- The key set has no signing key with the assertion's `kid`.
- The signature doesn't verify, or the JWT uses an algorithm other than `ES384` or `RS384`.
- The `aud` isn't the token endpoint URL, a required claim is missing, the assertion expired more than 30 seconds ago, or its `exp` is more than 10 minutes in the future.
- The `jti` was already used.

## Authorization Code

The Authorization Code flow ensures a user of the Canvas EHR explicitly approves the token request. It's typically used by web/mobile applications that act on behalf of a specific user (staff or patient).

The access token obtained through this flow carries the identity of the user who authorized it. This means:
- **FHIR API calls** are scoped to that user's permissions.
- **SimpleAPI plugin endpoints** receive the user as the [event actor](/sdk/events/#event-actor), allowing plugins to identify which user is making the request and enforce access controls.

### Basic Steps

1. The application opens a browser to the Canvas authorization endpoint.
2. The logged-in user sees the authorization prompt and approves the request.
3. The user is redirected back to the `redirect_uri` with an authorization code in the query string.
4. The application exchanges the authorization code for an access token and refresh token.

### Step 1: Redirect the User to Authorize

Open the following URL in the user's browser:

```text
{YOUR_CANVAS_EHR_INSTANCE}/auth/authorize/?response_type=code&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={REDIRECT_URI}&launch={LAUNCH_CONTEXT}
```

**Important notes:**

- **`launch` parameter (required for staff users):** Staff users must include a `launch` parameter containing a base64-encoded JSON object with context. Without this parameter, the authorization will be denied with `error=access_denied`.

  ```bash
  # Encode a launch context with a patient id
  echo -n '{"patient":"PATIENT_KEY_HERE"}' | base64
  # Result: eyJwYXRpZW50IjoiUEFUSUVOVF9LRVlfSEVSRSJ9

  # Or with an empty patient (if no specific patient context is needed,
  # or the token must call staff APIs such as the Note API)
  echo -n '{"patient":""}' | base64
  # Result: eyJwYXRpZW50IjoiIn0=
  ```

- **URL-encode special characters in scopes:** Scopes like `user/*.read` contain `/` which must be encoded as `%2F` in the URL. For example: `scope=user%2F*.read%20user%2F*.write`

- **Authorization codes expire quickly:** The code returned in the redirect is valid for approximately 60 seconds. Exchange it for tokens immediately.

**Example authorize URL:**

```text
{YOUR_CANVAS_EHR_INSTANCE}/auth/authorize/?response_type=code&client_id={CLIENT_ID}&scope=user%2F*.read%20user%2F*.write&redirect_uri=https://your-app.com/callback&launch=eyJwYXRpZW50IjoiIn0=
```

After the user clicks **Authorize**, they are redirected to your `redirect_uri` with a `code` parameter:

```text
https://your-app.com/callback?code=AUTHORIZATION_CODE
```

### Step 2: Exchange the Code for Tokens

```shell
curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=authorization_code' \
--data-urlencode 'client_id={CLIENT_ID}' \
--data-urlencode 'client_secret={CLIENT_SECRET}' \
--data-urlencode 'redirect_uri={REDIRECT_URI}' \
--data-urlencode 'code={CODE_FROM_PREVIOUS_STEP}'
```

**Response:**

```json
{
  "access_token": "AN_ACCESS_TOKEN",
  "expires_in": 36000,
  "token_type": "Bearer",
  "scope": "user/*.read user/*.write",
  "refresh_token": "A_REFRESH_TOKEN",
  "patient": ""
}
```

- **`access_token`**: Valid for 10 hours (36000 seconds). Use this as a `Bearer` token in API requests.
- **`refresh_token`**: Non-expiring but **single-use**. Each time you refresh, you receive a new refresh token — store it to maintain long-term access.

### Step 3: Use the Token

Use the access token as a Bearer token in the `Authorization` header:

```shell
# FHIR API example
curl --request GET '{FUMAGE_BASE_URL}/Patient' \
--header 'Authorization: Bearer {ACCESS_TOKEN}'

# SimpleAPI plugin endpoint example
curl --request GET '{YOUR_CANVAS_EHR_INSTANCE}/plugin-io/api/{plugin_name}/{endpoint}' \
--header 'Authorization: Bearer {ACCESS_TOKEN}'
```

When a SimpleAPI plugin receives a request with a Bearer token, Canvas validates the token, identifies the user, and sets them as the [event actor](/sdk/events/#event-actor). The plugin can then use `self.event.actor` to determine which user is making the request.

### Step 4: Refresh the Token

Access tokens expire after 10 hours. Use the refresh token to get a new access token without requiring the user to re-authorize:

```shell
curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=refresh_token' \
--data-urlencode 'client_id={CLIENT_ID}' \
--data-urlencode 'client_secret={CLIENT_SECRET}' \
--data-urlencode 'refresh_token={REFRESH_TOKEN}' \
--data-urlencode 'scope={SCOPES}'
```

**Note:** The `scope` parameter must match the scopes from the original authorization (or be a subset). If omitted, Canvas will attempt to use the application's default allowed scopes, but this may fail with `invalid_scope` if the defaults don't match the original grant.

This returns a new `access_token` and a **new** `refresh_token`. The previous refresh token is consumed and cannot be reused. Store the new refresh token for the next refresh cycle.

### Recommended Pattern for External Applications

For applications that need to make API calls on behalf of specific Canvas users (e.g., a provider portal calling plugin endpoints):

1. **One-time setup per user:** Each user authorizes the app via the browser flow. Store the refresh token per user in your backend.
2. **Ongoing access:** Before making API calls, check if the access token is still valid. If expired, use the stored refresh token to get a new one.
3. **Token storage:** Access tokens last 10 hours. Refresh tokens are non-expiring but single-use — always store the latest one returned from a refresh.

## Patient Scoped Tokens

Canvas supports patient scoped tokens. These are access tokens requested on behalf of a specific patient and have read/write access to that patient's records only.

To acquire a patient scoped token, you will need to include some parameters in the body of your token request:
- A `client_id` and `client_secret` that your application will use to [authenticate with Canvas](#client-credentials).
- The Canvas resource id for the `patient` the token will be scoped to
- A `scope` parameter with space separated patient level scopes requested for the token.
  - Additional requested scopes should follow the pattern `patient/<ResourceName>.<read/write/*>`
    - `patient/Appointment.*`
    - `patient/Appointment.read patient/Appointment.write`
    - `patient/Patient.read`
    - `patient/Practitioner.read`
  - Canvas provides support for the wildcard character, but highly recommends only requesting the minimal scopes and access needed and using it as a convenience when both read and write are truly required for the application.

See [Resources by context](#resources-by-context) for the full list of resources a `patient/` scope can read and write.

### Example curl request

```bash
curl --location --request POST \
      'https://<your_subdomain_here>.canvasmedical.com/auth/token/' \
      --header 'Content-Type: application/x-www-form-urlencoded' \
      --data-urlencode 'grant_type=client_credentials' \
      --data-urlencode 'client_id=<client_id_from_Canvas>' \
      --data-urlencode 'client_secret=<client_secret_from_Canvas>' \
      --data-urlencode 'patient=abc123' \
      --data-urlencode 'scope=patient/Patient.read patient/Appointment.* patient/Practitioner.read'
```

### Expected Response Body

```json
{
  "access_token": "<the_access_token_to_use_in_your_request>", 
  "expires_in": 36000, 
  "token_type": "Bearer", 
  "scope": "patient/Patient.read patient/Appointment.* patient/Practitioner.read", 
  "smart_style_url": "https://canvas-storages.s3.us-west-2.amazonaws.com/fhir-static-resources/smart-style.json", 
  "patient": "abc123", 
  "need_patient_banner": true
}
```

Using this access token in subsequent requests ensures that records referencing other patients cannot be retrieved through accidental or malicious misuse of the token. Canvas will also deny requests for any resource types which were not included in `scope` of the token request and requests for resource types which do not support patient-scoped tokens.

**Note:** A patient scoped token must include which patient scopes are being requested. Token requests that include the patient parameter but are missing scope or request invalid scopes will be rejected.

## Tokens with a patient context

A token carries a patient context in these cases:

- It's a [patient scoped token](#patient-scoped-tokens).
- It comes from an authorization code flow whose `launch` context names a patient.

These tokens work with the FHIR API, but Canvas refuses them on staff APIs. Staff APIs include the `/api` endpoints, the [Note API](/api/note/), the [Letter API](/api/letter/), and the plugin install and management endpoints. Canvas also refuses tokens on staff APIs when the user they act as isn't a staff member, such as a patient.

A refused token gets `403 Forbidden` on `/api`. On the Note and Letter APIs and the plugin endpoints, it gets `401 Unauthorized`. To call these APIs, request a separate token. Use the client credentials flow, or the authorization code flow with a `launch` context that names no patient.

## Scopes

Scopes control which parts of the API the token can access.

- **Client Credentials Flow:** Scopes are optional. If omitted, the token is issued with the OAuth application's configured allowed scopes.
- **Authorization Code Flow:** Scopes are required and must be passed in the authorize URL.

Every scope you request must be one of the application's allowed scopes, whatever the grant type. Canvas rejects a request that includes any other scope with an `invalid_scope` error. To use a scope the application doesn't have, add it to the application's allowed scopes first.

A patient who signs in through the authorization code flow can approve only `patient/` resource scopes, plus the launch and OpenID scopes. If the request includes a `user/` or `system/` scope, Canvas denies it and redirects with `error=access_denied`.

Canvas implements [SMART on FHIR scopes](https://hl7.org/fhir/smart-app-launch/STU2/scopes-and-launch-context.html).

### Scope syntax

Most scopes have the form `<context>/<resource>.<permission>`:

- **`<context>`** — `user/` (staff member; mirrors EHR permissions), `patient/` (limited to the launch-context patient), or `system/` (machine-to-machine, used with Client Credentials).
- **`<resource>`** — a FHIR resource (e.g., `Patient`) or `*` for any supported resource.
- **`<permission>`** — `read`, `write`, or `*` (v1 / legacy), or `c` (create), `r` (read), `u` (update), `s` (search) (v2 / granular). v2 letters can be combined, e.g., `Patient.crus`.

Separate multiple scopes with spaces, e.g., `user/Patient.read user/Observation.read`. URL-encode `/` as `%2F` and spaces as `%20`.

Common examples:

| Scope | Description |
|---|---|
| `user/*.read` | Read access to all resources |
| `user/*.write` | Write access to all resources |
| `user/*.*` | Full access to all resources |
| `user/Patient.read` | Read Patient resources only |
| `system/*.read` | System-level read access to all resources (used for bulk-data export, e.g., `Group/{id}/$export`) |

### Launch and OpenID scopes

| Scope | Description |
|---|---|
| `launch` | Allows external app launches |
| `launch/patient` | Allows patient context |
| `openid` | OpenID Connect scope |
| `fhirUser` | Returns the authenticated user's FHIR identity |
| `offline_access` | Requests a refresh token |

### Resources by context

Examples: `user/*.read`, `system/Patient.crus`, `patient/Appointment.write`.

**`user/`** — most clinical resources support `read`, `write`, `*`, and v2 `c r u s`. Read-only: `Coverage`, `MedicationDispense`, `Questionnaire`, `RelatedPerson`, `ServiceRequest`, `Specimen`. `Note` supports `read` and `write` only (no `*`). Resources: `*`, `AllergyIntolerance`, `CarePlan`, `CareTeam`, `Condition`, `Coverage`, `DetectedIssue`, `Device`, `DiagnosticReport`, `DocumentReference`, `Encounter`, `Goal`, `Immunization`, `Location`, `Medication`, `MedicationDispense`, `MedicationRequest`, `Note`, `Observation`, `Organization`, `Patient`, `Practitioner`, `PractitionerRole`, `Procedure`, `Provenance`, `Questionnaire`, `QuestionnaireResponse`, `RelatedPerson`, `ServiceRequest`, `Specimen`.

**`system/`** — same set as `user/` plus `Task` (full access). Read-only resources match `user/`. `system/Plugins.*` grants full access to plugin install/list/management endpoints. These endpoints accept only a client credentials token. Canvas refuses an authorization code token even when it carries `system/Plugins.*`.

**`patient/`** — restricted to the launch-context patient. Writable: `Appointment`, `Communication`, `Consent`, `Coverage`, `Media`, `MedicationStatement`, `Patient`, `PaymentNotice`, `QuestionnaireResponse`. All others read-only. Additional read-only resources beyond the user/system list: `Appointment`, `Communication`, `Consent`, `Media`, `MedicationStatement`, `PaymentNotice`, `Schedule`, `Slot`.

### Operation scopes

Some FHIR operations require a dedicated scope in addition to the resource scope. Available under both `user/` and `system/`:

| Scope suffix | Operation |
|---|---|
| `Claim.add-activity-log-item` | Add an activity log entry to a Claim |
| `DiagnosticReport.create-lab-report` | Create a lab report |
| `Practitioner.send-reset-password-email` | Send a password-reset email to a practitioner |

## Additional reading
- [Authentication Best Practices](/api/authentication-best-practices)
- [Event Actor](/sdk/events/#event-actor) — how plugins identify the authenticated user
