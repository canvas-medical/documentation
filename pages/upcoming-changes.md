---
permalink: /product-updates/important-dates/
title: Important Dates
layout: productupdates	
date: 2024-05-17
hidden: true
---
Stay up to date on the latest important dates for the Canvas platform.

<table border="1" style="table-layout: fixed; width: 100%">
  <colgroup>
    <col width="18%">
    <col width="12">
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
      <td>FHIR API Version 1</td>
      <td style="color: green;">New Version</td>
      <td>We have released V2 of our FHIR API and will be transitioning away from V1. During the transition period, you can control which API you use on a request-by-request basis by simply changing the subdomain. Your authentication tokens work on both versions. All updates and fixes will only occur in V2 going forward. Please reference our <a href="/guides/fhir-v2-migration-guide/">FHIR V2 migration guide.</a></td>
      <td></td>
      <td>06/28/2024</td>
    </tr>
    <tr>
      <td>FHIR API: Create and Updates Return Null</td>
      <td style="color: red;">Breaking Change</td>
      <td>We currently return the string <code>null</code> in the response body for successful create and update interactions. This behavior does not adhere to the FHIR spec. We will be updating all create and update endpoints to return empty response bodies on successful interactions.</td>
      <td>07/02/2024</td>
      <td></td>
    </tr>
    <tr>
      <td>Workflow SDK</td>
      <td style="color: green;">New Version</td>
      <td>The Workflow SDK has been deprecated, and will only receive fixes for defects or security issues. We are replacing its functionality with the Canvas SDK and its plugins, and will not set a date for the removal of the Workflow SDK until the Canvas SDK reaches feature parity. At that time we will present a migration plan to convert Workflow SDK Protocols into Canvas Plugins.</td>
      <td></td>
      <td>TBD<br/>(Not Soon)</td>
    </tr>
    <tr>
      <td>FHIR API: DiagnosticReport Status <code>entered_in_error</code></td>
      <td style="color: red;">Breaking Change</td>
      <td>We currently return <code>entered_in_error</code> for status. Per the FHIR spec, it should be <code>entered-in-error</code>, so we will be updating the read and search endpoints to return the correct value.</td>
      <td>07/02/2024</td>
      <td></td>
    </tr>
    <tr>
      <td>FHIR API: Location Header</td>
      <td style="color: red;">Breaking Change</td>
      <td>Canvas does not support versioned resources; however, we currently include a resource version number in the location header returned for create interactions:<br>
      <code>Location: [base]/[type]/[id]/_history/[vid]</code><br><br>
      We will be removing it to adhere to the FHIR spec. If you are parsing the location header, you may need to adjust how you do so. The new format will be:<br>
      <code>Location: [base]/[type]/[id]</code></td>
      <td>07/02/2024</td>
      <td></td>
    </tr>
    <tr>
      <td>FHIR API: Resource Attachment File URLs</td>
      <td style="color: red;">Breaking Change</td>
      <td>The FHIR spec does not allow expiring pre-signed URLs for resource attachments. Going forward, HTTP clients that request resource attachment files will need to provide a bearer token in the request. The affected resources are Consent, DocumentReference, DiagnosticReport, Media, Patient, and Practitioner. Unless otherwise specified, the responses for these requests will be a temporary redirect to the pre-signed URLs. We have added a temporary extension to the Attachment attribute in each resource that includes the pre-signed URLs to support the transition.</td>
      <td><small>12/03/2024 <br> (updates to the existing Attachment attribute)</small></td>
      <td><small>TBD <br> (removing the temporary extension)</small></td>
    </tr>
    <tr>
      <td>FHIR API: Setting appointment location using the location integer value</td>
      <td style="color: red;">Breaking Change</td>
      <td>The FHIR Appointment endpoint now uses the reference from the Location Read/Search endpoint for the Location in supportingInformation. We plan to discontinue support of using the location integer.</td>
      <td>TBD</td>
      <td></td>
    </tr>
    <tr>
      <td>FHIR API: Task note field append/replace behavior phase 1</td>
      <td style="color: red;">Breaking Change</td>
      <td>The FHIR Task update endpoint currently operates in a non-RESTful manner with respect to task notes (i.e. task comments in Canvas nomenclature). A FHIR Task update request will append all notes in the request body to the resource, rather than replacing all notes in the resource with the notes in the request body. To make the endpoint behave in a RESTful manner, we will be changing the behavior of this endpoint in multiple phases to allow for a gradual migration.<br><br>To facilitate this change, the Task update endpoint now recognizes a <code>Prefer</code> header that will accept one of two values: <code>note-append</code> or <code>note-replace</code>. The current default value, if this header is not provided, is <code>Prefer: note-append</code>.<br><br>On the release date, the default behavior will change from <code>Prefer: note-append</code> to <code>Prefer: note-replace</code>. Users are advised to update their client code to send <code>Prefer: note-replace</code> before the release date. Sending <code>Prefer: note-replace</code> will also require updating client code to send all notes for a Task in a update request body, rather than just new notes. Without this update to client code, there is a risk of deletion of Task notes during update requests. If you wish to temporarily retain the old default behavior to allow more time to update client code, you can send <code>Prefer: note-append</code>, but please note that this behavior is deprecated, and support for it will be removed in the near future.</td>
      <td>TBD</td>
      <td></td>
    </tr>
    <tr>
      <td>FHIR API: Task note field append/replace behavior phase 2</td>
      <td style="color: red;">Breaking Change</td>
      <td>On the release date, the FHIR Task update endpoint will no longer support the <code>Prefer: note-append</code> header.</td>
      <td>TBD</td>
      <td></td>
    </tr>
</tbody>
</table>
