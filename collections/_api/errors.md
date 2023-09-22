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
| 401 - Unauthorized         | No valid Bearer token provided.                                        |
| 403 - Forbidden            | Token bearer is forbidden from performing the operation.               |
| 404 - Not Found            | The requested resource doesn't exist.                                  |
| 422 - Unprocessable Entity | There operation cannot be completed because of an error in the request body; details are provided in the returned OperationOutcome |
| 5xx - Server Error         | Something went wrong on Canvas's end.                                  |



**401**
```
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
```
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
```
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

**422**

```
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
