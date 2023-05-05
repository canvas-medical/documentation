---
title: "DocumentReference Search"
slug: "documentreference-search"
excerpt: "Endpoint for returning specific PDF document references. PDFs are generated for any invoicing associated with a patient. See this Zendesk article.   that are uploaded to Canvas along with lab reports and imaging reports."
hidden: false
createdAt: "2021-09-10T23:26:46.098Z"
updatedAt: "2022-05-31T20:44:53.071Z"
---
This endpoint implements the US Core DocumentReference Profile for Report and Note Exchange. The following USCDI data elements are retrievable from this endpoint:

Clinical Notes: 

* Consultation Note
* Discharge Summary Note
* History & Physical
* Progress Note
* Imaging Narrative
* Laboratory Report Narrative
* Pathology Report Narrative
* Procedure Note

## Categories
The following categories are supported in Canvas: 
- `labreport` see [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918713-Lab-Reports) on how to link an uploaded lab report to a patient.
- `imagingreport` see [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918193-Imaging-Reports) on how to link an uploaded imaging report to a patient.
- `educationalmaterial` see [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4999882305939-Educational-Material-Command-) on how to educate a specific patient with an external PDF file.
- `invoicefull` see [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4406239284499-Statements-and-Invoicing) on how statement and invoicing works for a specific patient.


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