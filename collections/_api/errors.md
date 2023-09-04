---
title: "Errors"
layout: apipage
---
Canvas uses conventional HTTP response codes to indicate success or failure of an API request.
In general: Codes in the `2xx` range indicate success. Codes in the `4xx` range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a request wasn't found, etc.). Codes in the `5xx` range indicate an error with Canvas' server.

All `4xx` errors that could be handled programmatically (e.g., resource not found) include an [OperationOutcome](https://www.hl7.org/fhir/operationoutcome.html) that explains the error reported


| Error Code         | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| 200 - OK           | Everything worked as expected.                                         |
| 401 - Unauthorized | No valid Bearer token provided.                                        |
| 404 - Not Found    | The requested resource doesn't exist.                                  |
| 5xx - Server Error | Something went wrong on Canvas's end.                                  |
| 422 - Unprocessable Entity | Outcome of FHIR Appointment Create/Update when double booking is disabled, you may see  `This appointment time is no longer available.` [See here](/api/appointment) |


**401**
```
{
    "resourceType": "OperationOutcome",
    "id": "469ea864-5127-4765-8a76-8ef97c980de8",
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><hr/><ul><li><span style=\"font-weight: bold;\">FATAL</span><ul><li> Type: <span>FORBIDDEN</span></li><li> Details: <pre>Unauthorized</pre>\n\t\t\t\t</li>\n\t\t\t\t\n\t\t\t\t\n\t\t\t</ul>\n\t\t</li>\n\t</ul>\n</div>"
    },
    "issue": [
        {
            "severity": "fatal",
            "code": "forbidden",
            "details": {
                "text": "Unauthorized"
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
    "id": "00000000-0000-0000-0000-000000000000",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2022-03-23T16:18:57.188+00:00"
    },
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><hr/><ul><li><span style=\"font-weight: bold;\">ERROR</span><ul><li> Type: <span>PROCESSING</span></li><li> Details: <pre>Resource not found</pre>\n\t\t\t\t</li>\n\t\t\t\t\n\t\t\t\t\n\t\t\t</ul>\n\t\t</li>\n\t</ul>\n</div>"
    },
    "issue": [
        {
            "severity": "error",
            "code": "processing",
            "details": {
                "text": "Resource not found"
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
    "id": "00000000-0000-0000-0000-000000000000",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2022-06-21T20:20:00.523+00:00"
    },
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><hr/><ul><li><span style=\"font-weight: bold;\">ERROR</span><ul><li> Type: <span>PROCESSING</span></li><li> Details: <pre>{&quot;error&quot;:&quot;This appointment time is no longer available.&quot;}</pre>\n\t\t\t\t</li>\n\t\t\t\t\n\t\t\t\t\n\t\t\t</ul>\n\t\t</li>\n\t</ul>\n</div>"
    },
    "issue": [
        {
            "severity": "error",
            "code": "processing",
            "details": {
                "text": "{\"error\":\"This appointment time is no longer available.\"}"
            }
        }
    ]
}
```