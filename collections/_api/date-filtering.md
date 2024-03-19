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
    Example: `"?date=ne2021-01-01"`