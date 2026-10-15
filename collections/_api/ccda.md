---
title: "Retrieving C-CDA via API"
layout: apipage
---

## Software Requirements
Software requirements for retrieving C-CDA via API calls can be found [here](/api/software-requirements)

## Authentication

If you have a Canvas Production instance, you will need to request a token and refresh it periodically. You can refer to our [Authentication Documentation](/api/customer-authentication) to get you set up.

A C-CDA carries the patient's whole clinical record. The export therefore requires a wildcard read [scope](/api/customer-authentication/#scopes) at the `patient/`, `user/`, or `system/` level. Canvas accepts the SMART v1 forms `*.read` and `*.*`, and SMART v2 forms that include read, such as `*.r`, `*.rs`, and `*.cruds`. For example, a [client credentials](/api/customer-authentication/#client-credentials) token with `system/*.read` can export a C-CDA. A token with only `system/Appointment.read` cannot. Canvas refuses a token without a wildcard read scope with `403 Forbidden`.

An application can also send its client ID and secret with the request instead of a token. In that case, the OAuth application's allowed scopes must include a wildcard read scope.

A token bound to one patient returns only that patient's record, whatever patient key the URL names. A token is bound to a patient when its [SMART launch context](/api/customer-authentication/#authorization-code) names that patient. A token issued to a patient's own login is bound to that patient too. Staff and client credentials tokens export the patient the URL names.

## Request and Parameters

In order to generate a CCDA for a known patient id, you'll need to do a GET request to the endpoint `{YOUR_EHR_INSTANCE}/api/data-export/ccda/{patient_id}?document={document_type}`, where `document_type` can be either `continuity` or `referral`. You can check all parameters in the table below.

<table border="1">
  <thead>
    <tr>
      <th>Parameter Name</th>
      <th>Description</th>
      <th>Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>document</td>
      <td>Document type to be generated.<br>Should be either `continuity` or `referral`</td>
      <td>Mandatory</td>
    </tr>
    <tr>
      <td>start_date</td>
      <td>Filter for the start date of the sections within the document.<br>Format should be `YYYY-MM-DD`</td>
      <td>Optional</td>
    </tr>
    <tr>
      <td>end_date</td>
      <td>Filter for the end date of the sections within the document.<br>Format should be `YYYY-MM-DD`</td>
      <td>Optional</td>
    </tr>
    <tr>
      <td>generation_date</td>
      <td>Overrides the generation date of the document.<br>Format should be `YYYY-MM-DDTHH:mm:ss`, in UTC timezone</td>
      <td>Optional</td>
    </tr>
  </tbody>
</table>

## Filtering

`start_date` and `end_date` filter can be used to:
* filter by a range of dates by inputing both parameters;
* filter by a single date in the past by making `start_date` and `end_date` the same;
* filter starting at a date in the past up until present time by only setting `start_date`;
* filter from the beginning of time up to any date by only setting `end_date`;

## Example and Response

Here's a cURL example of a request for a continuity of care document, filtered for 2020-01-01 to 2020-12-31, and with a generation date of 2022-01-01, at 16:30 UTC:
```shell
curl --request GET --header "Authorization: Bearer <token>" "<practice_subdomain>.canvasmedical.com/api/data-export/ccda/{PATIENT_ID}?document=continuity&start_date=2024-01-01&end_date=2024-12-31&generation_date=2025-07-31T16:30:00"
```

A valid request will always return XML with the requested document as the response. 
If the `document` param is omitted, an empty XML will be returned. 

## Errors

Canvas uses conventional HTTP response codes to indicate success or failure of an API request.
In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a request wasn't found, etc.). Codes in the 5xx range indicate an error with Canvas' server.

<table border="1">
  <thead>
    <tr>
      <th>Error</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>200 - OK</td>
      <td>Everything worked as expected.</td>
    </tr>
    <tr>
      <td>403 - Forbidden</td>
      <td>No valid Bearer token provided, or the token has no wildcard read scope.</td>
    </tr>
    <tr>
      <td>404 - Not Found</td>
      <td>The requested resource doesn't exist.</td>
    </tr>
    <tr>
      <td>500 - Server Error</td>
      <td>Something went wrong on Canvas's end.</td>
    </tr>
  </tbody>
</table>
