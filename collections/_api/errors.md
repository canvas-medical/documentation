---
title: "Errors"
layout: apipage
---
Canvas uses conventional HTTP response codes to indicate success or failure of an API request.
In general: Codes in the `2xx` range indicate success. Codes in the `4xx` range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a request wasn't found, etc.). Codes in the `5xx` range indicate an error with Canvas' server.

All `4xx` errors that could be handled programmatically (e.g., resource not found) include an [OperationOutcome](https://www.hl7.org/fhir/operationoutcome.html) that explains the error reported


| Error Code                 | Description                                                            |
|----------------------------| ---------------------------------------------------------------------- |
| 200 - OK                   | Everything worked as expected.                                         |
| 400 - Bad Request          | The request was malformed or rejected by validation. |
| 401 - Unauthorized         | No valid Bearer token provided.                                        |
| 403 - Forbidden            | Token bearer is forbidden from performing the operation.               |
| 404 - Not Found            | The requested resource doesn't exist.                                  |
| 412 - Precondition Failed  | A conditional request failed because the resource has been modified since the precondition was specified. |
| 422 - Unprocessable Entity | The request was syntactically correct but failed due to request semantics, database state, or a business rule. |
| 504 - Gateway Timeout      | Canvas didn't respond within 60 seconds. The request may still have completed. See [Timeouts](#timeouts). |
| 5XX - Server Error         | Something went wrong on Canvas's end.                                  |



**400**
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "invalid",
      "details": {
        "text": "The request was malformed or failed validation."
      }
    }
  ]
}
```
<br>

**401**
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "unknown",
      "details": {
        "text": "Authentication failed"
      }
    }
  ]
}
```
<br>

**403**
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "forbidden",
      "details": {
        "text": "Authorization failed"
      }
    }
  ]
}
```
<br>


**404**
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "details": {
        "text": "Unknown Patient resource 'a47c7b0ebbb442cdbc4adf259d148ea1'"
      }
    }
  ]
}
```
<br>

**412**
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "conflict",
      "details": {
        "text": "The resource has been modified since the precondition was specified."
      }
    }
  ]
}
```
<br>

**422**

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "business-rule",
      "details": {
        "text": "This appointment time is no longer available."
      }
    }
  ]
}
```

**5XX**

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "exception",
      "details": {
        "text": "Internal server error"
      }
    }
  ]
}
```

## Timeouts

If the FHIR API doesn't respond within 60 seconds, the proxy in front of it returns a `504 Gateway Timeout` response. This response comes from the proxy, so its body isn't an OperationOutcome and it has no `Fumage-Correlation-ID` header.

Canvas keeps processing the request after the proxy returns the 504. A create or update that returned a 504 may have completed, and retrying it can create a duplicate record. Before you retry, search for the record, such as an Appointment search for the patient and date, and retry only if the search doesn't find it.

## Correlation IDs

Responses from the FHIR API, including error responses, have a `Fumage-Correlation-ID` header that identifies the request. Include this ID when you contact Canvas support about a failed request.

A `504` response from the proxy has no correlation ID. To know a request's ID even when it times out, send your own: set the `Fumage-Correlation-ID` request header to a new UUID version 4 for each request, and log it with the request. The FHIR API uses that value as the request's correlation ID and returns it in the response header. If the value isn't a valid UUID version 4, the FHIR API generates a new ID instead.

```python
import uuid

import requests

url = "https://fumage-example.canvasmedical.com/Patient/<patient ID>"
correlation_id = str(uuid.uuid4())

headers = {
    "accept": "application/json",
    "Authorization": "Bearer <token>",
    "Fumage-Correlation-ID": correlation_id,
}

response = requests.get(url, headers=headers)
if not response.ok:
    print(f"Request failed with status {response.status_code}. Correlation ID: {correlation_id}")
```
