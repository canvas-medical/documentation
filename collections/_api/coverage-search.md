---
title: "Coverage Search"
slug: "coverage-search"
excerpt: "Search for coverages for a particular patient"
hidden: false
createdAt: "2021-09-10T02:22:54.647Z"
updatedAt: "2022-09-21T20:36:41.504Z"
---
## Adding a Coverage in Canvas

See this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/4408206355603-Patient-Coverages-2-0) to learn how to create or update coverage for a patient.

## Pagination

To paginate coverage search results, use the query param `_count`.
Example:
`GET /Coverage?_count=10` will return the first 10 coverages, along with relative links to see the subsequent pages.
The pages are specified by a combination of `_count` and `_offset`.