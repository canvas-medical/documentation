---
title: "DiagnosticReport Search"
slug: "diagnosticreport-search"
hidden: false
createdAt: "2022-03-23T13:40:18.945Z"
updatedAt: "2022-05-17T17:28:05.937Z"
---
This endpoint implements the US Core DiagnosticReport Profile for Report. The following USCDI data elements are retrievable from this endpoint:

Clinical Notes: 

* Imaging Narrative
* Laboratory Report Narrative
* Pathology Report Narrative
* Procedure Note

Laboratory:

* Tests
* Values/Results

## Date filtering
We support the following date search modifiers:
- `ge` Example: `"?date=ge2021-01-01"`
  - Greater than or equal to the date.
- `gt` Example: `"?date=gt2021-01-01"`
  - Strictly greater than the date.
- `le` Example: `"?date=le2021-01-01"`
  - Less than or equal to the date.
- `lt` Example: `"?date=lt2021-01-01"`
  - Strictly less than the date.
- `eq` Example: `"?date=eq2021-01-01"`
  - Strictly equal to the date.
- `ne` Example: `"?date=ne2021-01-01"`
  - Not equal to the date.

For more details, see https://hl7.org/fhir/search.html#prefix