---
title: "Date Filtering"
slug: "date-filtering"
layout: apipage
---
A few of the API Search endpoints support date search parameters. You have the ability to filter a Resources query result by a specific date or a date range. For more details, see https://hl7.org/fhir/search.html#prefix

We support the following date search modifiers:

- `ge` <br>
    Greater than or equal to the date.<br>
    Example: `"?date=ge2021-01-01"``

- `gt`
    Strictly greater than the date. <br>
    Example: `"?date=gt2021-01-01"`

- `le`
    Less than or equal to the date. <br>
    Example: `"?date=le2021-01-01"`

- `lt`
    Strictly less than the date. <br>
    Example: `"?date=lt2021-01-01"`

- `eq`
    Strictly equal to the date. <br>
    Example: `"?date=eq2021-01-01"`<br><br>

You can supply multiple date search parameters to search in a range. For example if we want to find all the records within 2024-04-11 and 2024-04-20, we can pass `?date=ge2024-04-11&date=le2024-04-20`

The API endpoints that support date search parameters include:
* [Appointment](/api/appointment/) (/Appointment) - Filter by appointment date
* [Consent](/api/consent/) (/Consent) - Filter by consent date
* [DetectedIssue](/api/detectedissue/) (/DetectedIssue) - Filter by identified date
* [DiagnosticReport](/api/diagnosticreport/) (/DiagnosticReport) - Filter by report date
* [DocumentReference](/api/documentreference/) (/DocumentReference) - Filter by document date
* [Encounter](/api/encounter/) (/Encounter) - Filter by encounter date/period
* [Observation](/api/observation/) (/Observation) - Filter by observation date/time
* [QuestionnaireResponse](/api/questionnaireresponse/) (/QuestionnaireResponse) - Filter by authored date
* [ServiceRequest](/api/servicerequest/) (/ServiceRequest) - Filter by authored date
* [Task](/api/task/) (/Task) - Filter by date

