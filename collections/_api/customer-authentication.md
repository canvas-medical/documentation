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
  # Encode a launch context with a patient key
  echo -n '{"patient":"PATIENT_KEY_HERE"}' | base64
  # Result: eyJwYXRpZW50IjoiUEFUSUVOVF9LRVlfSEVSRSJ9

  # Or with an empty patient (if no specific patient context is needed)
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

## Scopes

Scopes control which parts of the API the token can access.

- **Client Credentials Flow:** Scopes are optional. If omitted, you'll have full access to the FHIR API.
- **Authorization Code Flow:** Scopes are required and must be passed in the authorize URL.

Scopes follow the [SMART on FHIR Clinical Scope Syntax](https://hl7.org/fhir/smart-app-launch/STU2/scopes-and-launch-context.html#clinical-scope-syntax). They have the form: `(patient|user|system)/(resourceType|*).(c|r|u|d|s)`, where:

- The prefix selects the access context: `user/` (current user's permissions), `patient/` (a specific patient's compartment, established at launch), or `system/` (system-level/backend access, used for bulk-data export).
- `resourceType` can be a specific resource (e.g., `Patient`, `Practitioner`) or a wildcard `*`.
- Permissions: `c` (create), `r` (read), `u` (update), `d` (delete), `s` (search).
- Legacy SMART v1 permissions are also accepted and converted internally: `read` → `rs`, `write` → `cud`, and `*` → `cruds`. For example, `user/Patient.read` is equivalent to `user/Patient.rs`.

Multiple scopes are separated by spaces. Common examples:

| Scope | Description |
|---|---|
| `user/*.read` | Read access to all resources |
| `user/*.write` | Write access to all resources |
| `user/*.*` | Full access to all resources |
| `user/Patient.read` | Read Patient resources only |
| `system/*.read` | System-level read access to all resources (used for bulk-data export, e.g., `Group/{id}/$export`) |
| `openid` | OpenID Connect scope |
| `offline_access` | Request a refresh token |

**URL encoding reminder:** When passing scopes in a URL, encode `/` as `%2F` and spaces as `%20`. For example: `scope=user%2F*.read%20user%2F*.write`

## SMART on FHIR discovery

The FHIR API exposes a SMART on FHIR configuration document at `GET {FUMAGE_BASE_URL}/.well-known/smart-configuration`. Clients can fetch this document at runtime to discover the supported authorization endpoints, token endpoint, and capabilities. Returned fields include:

- `issuer` — the issuer URL.
- `authorization_endpoint` — the URL to send users to for authorization (Authorization Code flow).
- `token_endpoint` — the URL to exchange an authorization code or client credentials for an access token.
- `jwks_uri` — the URL of the JSON Web Key Set used to verify tokens.
- `capabilities` — supported SMART capabilities, including `launch-standalone`, `client-confidential-symmetric`, and supported response types.
- `grant_types_supported` — the supported OAuth grant types (e.g., `authorization_code`, `client_credentials`, `refresh_token`).
- `scopes_supported` — the supported scope strings.

## Additional reading
- [Authentication Best Practices](/api/authentication-best-practices)
- [Event Actor](/sdk/events/#event-actor) — how plugins identify the authenticated user
