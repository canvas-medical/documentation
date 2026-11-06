---
title: "Retrieving C-CDA via API"
layout: apipage
---

## Software Requirements
Software requirements for retrieving C-CDA via API calls can be found [here](/api/software-requirements)

## Authentication

If you have a Canvas Production instance, you will need to request a token and refresh it periodically. You can refer to our [Authentication Documentation](/api/customer-authentication) to get you set up.

If you use a [client credentials](/api/customer-authentication/#client-credentials) token, request it with the `system/*.*` scope. Canvas refuses a client credentials token with narrower scopes on this endpoint with `403 Forbidden`.

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

## Concurrent requests

Each C-CDA renders the patient's full clinical record, so an instance generates only a few at a time. A request that arrives while every slot is in use gets `429 Too Many Requests` with a `Retry-After` header (in seconds) instead of a document. The request did nothing, so it is safe to send again.

When exporting many patients:
* send a few requests at a time rather than all at once;
* on a `429`, wait for the `Retry-After` interval before retrying that patient;
* do not retry a `400`, which means the patient's record is missing data the document needs.

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
      <td>400 - Bad Request</td>
      <td>The patient is missing data a C-CDA requires (for example, a Team Lead). The plain-text body names what is missing. Retrying will not succeed until the patient's record changes.</td>
    </tr>
    <tr>
      <td>403 - Forbidden</td>
      <td>No valid Bearer token provided.</td>
    </tr>
    <tr>
      <td>404 - Not Found</td>
      <td>The requested resource doesn't exist.</td>
    </tr>
    <tr>
      <td>429 - Too Many Requests</td>
      <td>The instance is already generating as many C-CDAs as it allows at once. Wait the number of seconds in the <code>Retry-After</code> header, then retry. See <a href="#concurrent-requests">Concurrent requests</a>.</td>
    </tr>
    <tr>
      <td>500 - Server Error</td>
      <td>Something went wrong on Canvas's end.</td>
    </tr>
  </tbody>
</table>
