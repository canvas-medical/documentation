---
title: "Authentication"
layout: documentation
---
[block:api-header]
{
  "title": "Introduction"
}
[/block]
* Canvas is an OAuth 2.0 authorization server.
This page contains information about how you can create third-party applications within your Canvas EHR instance and use those applications to access the FHIR API.

Canvas supports most OAuth flows, but this document will focus on two of the most used:
* **Client Credentials** - Mostly used for Machine-to-Machine authentication (e.g., CLIs, Daemons)
* **Authorization Code** - Usually used for web/native applications, since it requires a user to log in to the system.

[block:api-header]
{
  "title": "Registering a third-party application on Canvas"
}
[/block]
Registering a third-party application is always the first step.
In order to do so, you'll need to:
1. Go to `{YOUR_CANVAS_EHR_INSTANCE}/auth/applications/` where you'll see the following page:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ed67823-Screenshot_2021-10-26_at_16.22.31.png",
        "Screenshot 2021-10-26 at 16.22.31.png",
        645,
        201,
        "#f6f6f7"
      ]
    }
  ]
}
[/block]
2. Once you click the link in that page, you'll see the following:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8b49344-Screenshot_2021-10-26_at_16.24.01.png",
        "Screenshot 2021-10-26 at 16.24.01.png",
        652,
        822,
        "#fafafa"
      ]
    }
  ]
}
[/block]
You'll need to set a name for the app, set the `Client type` to `Confidential`, choose one of the `Authorization grant type`s and set the `Redirect uris` if needed. Leave the `Algorithm` at `No OIDC support` for now.

Here's how it should look if you created a new "Test Application" with the `client-credentials` grant type:
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/6190a01-Screenshot_2021-10-26_at_16.26.59.png",
        "Screenshot 2021-10-26 at 16.26.59.png",
        651,
        597,
        "#f4f4f5"
      ]
    }
  ]
}
[/block]
And that's it. Take note of your `Client id` and `Client secret`, and jump into the section related to the `Authorization Grant Type` you chose!
[block:api-header]
{
  "title": "Client Credentials"
}
[/block]
The Client Credentials flow assumes that everyone involved is capable of securely storing the `Client Id` and `Client secret`. 

In order to get a token you just need to:
[block:code]
{
  "codes": [
    {
      "code": "curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \\                                          127 ↵\n--header 'Content-Type: application/x-www-form-urlencoded' \\\n--data-urlencode 'grant_type=client_credentials' \\\n--data-urlencode 'client_id={YOUR_CLIENT_ID}' \\\n--data-urlencode 'client_secret={YOUR_CLIENT_SECRET}'",
      "language": "curl"
    }
  ]
}
[/block]
and you'll get back a JSON which will contains an `access_token` that'll be valid for 10 hours.
[block:api-header]
{
  "title": "Authorization Code"
}
[/block]
The Authorization Code flow has a lot more steps to ensure a user of the Canvas EHR explicitly approves the token request.
It's also typically used by web/mobile applications, due to the need of requiring explicit permission from a user logged in into the Canvas EHR.

The basic steps are:
* The application opens a browser to the Canvas EHR instance
* The logged in user sees the authorization prompt and approves the request
* The user is redirected back to the `redirect_url` with an authorization code in the query string
* The application exchanges the authorization code for an access token

Note that if you use this Flow, you will need to add redirect uris` when creating an application. That's the uri that will receive the authorization code.

If you're using Postman you can do this flow automatically if go to the `Authorization` tab on the request you're using and set the type to `OAuth 2.0` and set the parameters like in the following image.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4cafddd-Screenshot_2021-10-26_at_18.41.58.png",
        "Screenshot 2021-10-26 at 18.41.58.png",
        1154,
        891,
        "#fcfbfb"
      ]
    }
  ]
}
[/block]
Caveat: Your application needs to set `https://oauth.pstmn.io/v1/callback` as the redirect uri.

After you press "Get New Access Token", you'll be redirected to your Canvas EHR instance to accept the request, and once you do you'll get a new access token in Postman (that you can use wherever)

If you want to do the flow manually, then the steps are as follow:
1. On your browser, open `{YOUR_CANVAS_EHR_INSTANCE}/auth/authorize/?response_type=code&client_id={CLIENT_ID}&scope={LIST_OF_SCOPES}&redirect_uri={REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION}`
This will prompt the logged in user to authorize the Application. Upon authorization, the flow will redirect to the {REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION} with a code on the query string. You'll need that code next.
2. Now you need to exchange the code received in the previous step for an access token. For that, run the following:
[block:code]
{
  "codes": [
    {
      "code": "curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \\\n--header 'Content-Type: application/x-www-form-urlencoded' \\\n--data-urlencode 'grant_type=authorization_code' \\\n--data-urlencode 'client_id={CLIENT_ID}' \\\n--data-urlencode 'client_secret={CLIENT_SECRET}'\\\n--data-urlencode 'redirect_uri={REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION}' \\\n--data-urlencode 'code={CODE_FROM_PREVIOUS_STEP}'",
      "language": "curl"
    }
  ]
}
[/block]
And you'll get back an access token JSON that looks like the following:
[block:code]
{
  "codes": [
    {
      "code": "{\n  \"access_token\": \"AN ACCESS TOKEN\",\n  \"expires_in\": 36000,\n  \"token_type\": \"Bearer\",\n  \"scope\": \"List of accepted scopes here\",\n  \"refresh_token\": \"A REFRESH TOKEN\"\n}",
      "language": "json"
    }
  ]
}
[/block]

Notice the refresh token there, which doesn't exist for the Client Credentials flow. 

Since the `code` granted when the user authorizes the application is very short-lived, the refresh token allows for seamless revalidation of a token. This refresh token never expires, but can only be used once.
In order to request a new token you need to issue the following request:
[block:code]
{
  "codes": [
    {
      "code": "curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \\\n--header 'Content-Type: application/x-www-form-urlencoded' \\\n--data-urlencode 'grant_type=refresh_token' \\\n--data-urlencode 'client_id={CLIENT_ID}' \\\n--data-urlencode 'client_secret={CLIENT_SECRET}'\\\n--data-urlencode 'redirect_uri={REDIRECT_URI_AS_DEFINED_ON_THE_APPLICATION}' \\\n--data-urlencode 'refresh_token={REFRESH_TOKEN}'",
      "language": "curl"
    }
  ]
}
[/block]
 and you'll get a brand new access token.

[block:api-header]
{
  "title": "Scopes"
}
[/block]
Scopes are useful to prevent access to unwanted parts of the Api. 
If you're using the Client Credentials Flow, Scopes are optional and if omitted you'll have full access to the FHIR Api. Be mindful of that.

If you're using the Authorization Code Flow, you need to pass scopes as part of your first request to get an authorization code. 

These scopes follow the [Clinical Scope Syntax](https://www.hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html#clinical-scope-syntax) set by HL7. 

Since Canvas currently works on a User level (e.g., the logged in user isn't a Patient), the most relevant scopes can be found [here](https://www.hl7.org/fhir/smart-app-launch/scopes-and-launch-context.html#user-level-scopes).

In short, they have the form: `user/resourceType.(read|write|*)`.  where `resourceType` can be one of the supported resources (e.g., `Patient, Practitioner, etc) or a wildcard `*`.
