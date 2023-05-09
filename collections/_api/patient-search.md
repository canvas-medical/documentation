---
title: "Patient Search"
slug: "patient-search"
excerpt: "Search for patients"
hidden: false
createdAt: "2021-05-14T02:27:25.069Z"
updatedAt: "2022-06-06T14:40:03.013Z"
---
## Creating a New Patient in Canvas

To create a new patient chart in Canvas, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360059207113-Creating-a-New-Patient-Chart). 
[block:api-header]
{
  "title": "Searching by identifier."
}
[/block]

We support the following for searching by patient identifier in the identifier query param:

- `/Patient?identifier=abc123` will return patients with an identifier of “abc123” issued by any system, including Canvas-issued MRNs
- `/Patient?identifier=foo|abc123` will return patients with an identifier of “abc123" issued by the system named “foo”
- `/Patient?identifier=http://canvasmedical.com|012345` will return the patient with the Canvas-issued MRN of “012345"
- `/Patient?identifier=foo|` will return all patients with an identifier issued by the system named “foo”
- `/Patient?identifier=|abc123` will return patients with an identifier of “abc123" issued by the system named “” (empty string)
[block:api-header]
{
  "title": "Pagination"
}
[/block]
To paginate patient search results, use the query param `_count`.
Example:
`GET /Patient?_count=10` will return the first 10 patients, along with relative links to see the subsequent pages.
The pages are specified by a combination of `_count` and `_offset`.