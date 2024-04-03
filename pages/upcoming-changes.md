---
permalink: /product-updates/important-dates/
title: Important Dates
layout: productupdates	
date: 2023-12-01
hidden: true
---
Stay up to date on the latest important dates for the Canvas platform.

<table border="1">
  <thead>
    <tr>
      <th>Feature</th>
      <th>What You Need To Know</th>
      <th>Release Date</th>
      <th>End of Life</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>FHIR API Version 1</td>
      <td>We have released V2 of our FHIR API and will be transitioning away from V1. During the transiton period, you can control which API you use on a request-by-request basis by simply changing the subdomain. Your authentication tokens work on both versions. All updates and fixes will only occur in V2 going forward. Please reference our <a href="/guides/fhir-v2-migration-guide/">FHIR V2 migration guide.</a></td>
      <td></td>
      <td>06/28/2024</td>
    </tr>
    <tr>
      <td>FHIR API: Setting appointment location using the location integer value</td>
      <td>The FHIR Appointment endpoint now uses the reference from the Location Read/Search endpoint for the Location in supportingInformation. We plan to discontinue support of using the location integer. </td>
      <td></td>
      <td>TBD</td>
    </tr>
  </tbody>
</table>
