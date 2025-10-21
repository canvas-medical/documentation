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
    Example: `"?date=eq2021-01-01"`

- `ne`
    Not equal to the date. <br>
    Example: `"?date=ne2021-01-01"`<br><br>

You can supply multiple date search parameters to search in a range. For example if we want to find all the records within 2024-04-11 and 2024-04-20, we can pass `?date=ge2024-04-11&date=le2024-04-20`

The API endpoints that support date search parameters include:
* [AllergyIntolerance](/api/allergyintolerance/) (/AllergyIntolerance) - Filter by recorded date
* [Appointment](/api/appointment/) (/Appointment) - Filter by appointment date
* [CarePlan](/api/careplan/) (/CarePlan) - Filter by care plan date/period
* [CareTeam](/api/careteam/) (/CareTeam) - Filter by care team period
* [Consent](/api/consent/) (/Consent) - Filter by consent date
* [DiagnosticReport](/api/diagnosticreport/) (/DiagnosticReport) - Filter by report date
* [DocumentReference](/api/documentreference/) (/DocumentReference) - Filter by document date
* [Encounter](/api/encounter/) (/Encounter) - Filter by encounter date/period
* [Immunization](/api/immunization/) (/Immunization) - Filter by immunization date
* [Observation](/api/observation/) (/Observation) - Filter by observation date/time
* [Procedure](/api/procedure/) (/Procedure) - Filter by procedure date

