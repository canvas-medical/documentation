---
title: "Customer Authentication"
layout: apipage
---
If you are using a [Canvas Sandbox Environment](/guides/sandbox), you can skip this step and use your Bearer Token shown on your Dashboard.

For our Customers that have development, staging, or production instances, you can continue below to set up authentication.

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
  <img src="https://files.readme.io/ed67823-Screenshot_2021-10-26_at_16.22.31.png" alt="Authorization Page" style="width: 50%;" />


  2. Once you click the link on that page, you'll see the following:
  <img src="https://files.readme.io/8b49344-Screenshot_2021-10-26_at_16.24.01.png" alt="Application Registration" style="width: 50%;" />


  - You'll need to set a name for the app, set the `Client type` to `Confidential`, choose one of the `Authorization grant types`, and set the `Redirect URIs` if needed. Leave the `Algorithm` at `No OIDC support` for now.
  - Here's how it should look if you created a new "Test Application" with the `client-credentials` grant type:
<img src="https://files.readme.io/6190a01-Screenshot_2021-10-26_at_16.26.59.png" alt="Application Example" style="width: 50%;" />

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

The Authorization Code flow has a lot more steps to ensure a user of the Canvas EHR explicitly approves the token request. It's also typically used by web/mobile applications, due to the need for requiring explicit permission from a user logged into the Canvas EHR.

The basic steps are:
* The application opens a browser to the Canvas EHR instance.
* The logged-in user sees the authorization prompt and approves the request.
* The user is redirected back to the `redirect_url` with an authorization code in the query string.
* The application exchanges the authorization code for an access token.

Note that if you use this Flow, you will need to add redirect URIs when creating an application. That's the URI that will receive the authorization code.

If you're using Postman, you can do this flow automatically by going to the `Authorization` tab on the request you're using and set the type to `OAuth 2.0` and set the parameters like in the following image:

<img src="https://files.readme.io/4cafddd-Screenshot_2021-10-26_at_18.41.58.png" alt="Postman Authorization" style="width: 80%;" />

Caveat: Your application needs to set `https://oauth.pstmn.io/v1/callback` as the redirect URI.

After you press "Get New Access Token," you'll be redirected to your Canvas EHR instance to accept the request, and once you do, you'll get a new access token in Postman (that you can use wherever).

If you want to do the flow manually, then the steps are as follows:

1. On your browser, open `{YOUR_CANVAS_EHR_INSTANCE}/auth/authorize/?response_type=code&client_id={CLIENT_ID}&scope={LIST_OF_SCOPES}&redirect_uri={REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION}`. This will prompt the logged-in user to authorize the Application. Upon authorization, the flow will redirect to the {REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION} with a code on the query string. You'll need that code next.

2. Now you need to exchange the code received in the previous step for an access token. For that, run the following:

```shell
curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=authorization_code' \
--data-urlencode 'client_id={CLIENT_ID}' \
--data-urlencode 'client_secret={CLIENT_SECRET}' \
--data-urlencode 'redirect_uri={REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION}' \
--data-urlencode 'code={CODE_FROM_PREVIOUS_STEP}'
```

And you'll get back an access token JSON that looks like the following:

```json
{
  "access_token": "AN ACCESS TOKEN",
  "expires_in": 36000,
  "token_type": "Bearer",
  "scope": "List of accepted scopes here",
  "refresh_token": "A REFRESH TOKEN"
}
```

Notice the refresh token there, which doesn't exist for the Client Credentials flow.

Since the `code` granted when the user authorizes the application is very short-lived, the refresh token allows for seamless revalidation of a token. This refresh token never expires but can only be used once. In order to request a new token, you need to issue the following request:

```shell
curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=refresh_token' \
--data-urlencode 'client_id={CLIENT_ID}' \
--data-urlencode 'client_secret={CLIENT_SECRET}' \
--data-urlencode 'redirect_uri={REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION}' \
--data-urlencode 'refresh_token={REFRESH_TOKEN}'
```
and you'll get a brand new access token.

## Scopes

Scopes are useful to prevent access to unwanted parts of the API. If you're using the Client Credentials Flow, Scopes are optional, and if omitted, you'll have full access to the FHIR API. Be mindful of that.

If you're using the Authorization Code Flow, you need to pass scopes as part of your first request to get an authorization code. These scopes follow the [Clinical Scope Syntax](https://www.hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html#clinical-scope-syntax) set by HL7.

Since Canvas currently works on a User level (e.g., the logged-in user isn't a Patient), the most relevant scopes can be found [here](https://www.hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html#user-level-scopes).

In short, they have the form: `user/resourceType.(read|write|*)`, where `resourceType` can be one of the supported resources (e.g., `Patient, Practitioner, etc) or a wildcard `*`.