---
permalink: /product-updates/important-dates/
title: Important Dates
layout: roadmap
date: 2024-05-17
hidden: true
---
Stay up to date on the latest important dates for the Canvas platform.

<table border="1" style="table-layout: fixed; width: 100%">
  <colgroup>
    <col width="18%">
    <col width="12%">
    <col width="48%">
    <col width="11%">
    <col width="11%">
  </colgroup>
  <thead>
    <tr>
      <th>Description</th>
      <th>Type</th>
      <th>What You Need To Know</th>
      <th>Release Date</th>
      <th>End of Life</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Workflow SDK</td>
      <td style="color: green;">New Version</td>
      <td>The Workflow SDK has been deprecated, and will only receive fixes for defects or security issues. We are replacing its functionality with the Canvas SDK and its plugins, and will not set a date for the removal of the Workflow SDK until the Canvas SDK reaches feature parity. At that time we will present a migration plan to convert Workflow SDK Protocols into Canvas Plugins.</td>
      <td></td>
      <td>TBD<br/>(Not Soon)</td>
    </tr>
    <tr>
      <td>FHIR API: Setting appointment location using the location integer value</td>
      <td style="color: red;">Breaking Change</td>
      <td>The FHIR Appointment endpoint now uses the reference from the Location Read/Search endpoint for the Location in supportingInformation. We plan to discontinue support of using the location integer.</td>
      <td>TBD</td>
      <td></td>
    </tr>
</tbody>
</table>
