---
title: "Pagination"
slug: "pagination"
layout: apipage
---
Most endpoints that perform search operations support pagination.  For these endpoints, search results are paginated by default, with a `links` section as defined [by FHIR](http://hl7.org/fhir/R4/http.html#paging).  The links include urls for `self`, `first`, `next`, and `last` as needed for the searchset. Clients that want all results will need to make use of these links to page through the data. Pagination links will not be provided for an empty result set. A tip when traversing through the pages, if a `next` relation is not in the links list, you are on the last page!

There is a maximum page size (`_count`) that is enforced by the server. This value is at 100 at the time of writing, but can change without warning. Clients must use the links in a search bundle to paginate after an initial search request is sent. When no count is specified in a search, it will default to 10. 

In this example, `entry` contains 10 Observation resources - following the relative link marked as `next` returns the remaining 9.
```json
{
    "resourceType": "Bundle",
    "type": "searchset",
    "total": 19,
    "link": [
        {
            "relation": "self",
            "url": "/Observation?_count=10&_offset=0"
        },
        {
            "relation": "first",
            "url": "/Observation?_count=10&_offset=0"
        },
        {
            "relation": "next",
            "url": "/Observation?_count=10&_offset=10"
        },
        {
            "relation": "last",
            "url": "/Observation?_count=10&_offset=10"
        }
    ],
    "entry": [
        {
            "resource": {
                "resourceType": "Observation",
```