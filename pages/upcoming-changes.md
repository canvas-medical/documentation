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
      <td>The Workflow SDK is deprecated and receives only fixes for defects or security issues. Build new logic as Canvas SDK plugins. Uploading new protocol code returns an error. If you still use the Workflow SDK, reach out to Canvas support and we can help you migrate to plugins.</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Read-only replica: Clinical note body structure</td>
      <td style="color: red;">Breaking Change</td>
      <td>Canvas is changing how a clinical note stores its body, with every existing note migrated onto the new structure. Instances without a read-only replica are turned on first, on 09/21/2026, and instances with one a week later, on 09/28/2026. Nothing looks different in the chart, and the Note API, FHIR, and the plugin SDK need no change. An integration reading note bodies from the read-only replica needs a query change: on a migrated note the <code>body</code> column is empty and the lines move to <code>body_content</code> and <code>body_order</code>, with <code>checksum</code> no longer maintained. <a href="/release-notes/note-v2-2026-09-15/">Read more.</a></td>
      <td><small>09/21/2026 <br> (09/28/2026 with a read-only replica)</small></td>
      <td></td>
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
