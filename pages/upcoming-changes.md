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
      <td>FHIR API: Task note field append/replace behavior phase 1</td>
      <td style="color: red;">Breaking Change</td>
      <td>The FHIR Task update endpoint currently operates in a non-RESTful manner with respect to task notes (i.e. task comments in Canvas nomenclature). A FHIR Task update request will append all notes in the request body to the resource, rather than replacing all notes in the resource with the notes in the request body. To make the endpoint behave in a RESTful manner, we will be changing the behavior of this endpoint in multiple phases to allow for a gradual migration.<br><br>To facilitate this change, the Task update endpoint now recognizes a <code>Prefer</code> header that will accept one of two values: <code>note-append</code> or <code>note-replace</code>. The current default value, if this header is not provided, is <code>Prefer: note-append</code>.<br><br>On the release date, the default behavior will change from <code>Prefer: note-append</code> to <code>Prefer: note-replace</code>. Users are advised to update their client code to send <code>Prefer: note-replace</code> before the release date. Sending <code>Prefer: note-replace</code> will also require updating client code to send all notes for a Task in a update request body, rather than just new notes. Without this update to client code, there is a risk of deletion of Task notes during update requests. If you wish to temporarily retain the old default behavior to allow more time to update client code, you can send <code>Prefer: note-append</code>, but please note that this behavior is deprecated, and support for it will be removed in the near future.</td>
      <td>09/16/25</td>
      <td></td>
    </tr>
    <tr>
      <td>FHIR API: Task note field append/replace behavior phase 2</td>
      <td style="color: red;">Breaking Change</td>
      <td>On the release date, the FHIR Task update endpoint will no longer support the <code>Prefer: note-append</code> header.</td>
      <td>09/30/25</td>
      <td></td>
    </tr>
    <tr>
      <td>UI & FHIR API: Patient Contact Relationship</td>
      <td style="color: red;">Breaking Change</td>
      <td>
        On the release date, the following will be updated: <code>Prefer: note-append</code> header.
        <ul>
          <li>UI: Relationship field is being removed from contacts section of patient profile page</li>
          <li>Data migration: Data in Relationship field will be migrated to / appended to the Comments field</li>
          <li>FHIR Patient
            <ul>
              <li>Support will be discontinued for free text <code>contact[].relationship[].text</code> field; Relationship will now be represented by expanded use of contact categories</li>
              <li>Support will be discontinued for <strong>emergency contact</strong> and <strong>authorized for release of information</strong> extensions</li>
            </ul>
          </li>
        </ul>
      </td>
      <td>09/30/25</td>
      <td></td>
    </tr>
    <tr>
      <td>FHIR API: Coverage member identifier moving from subscriberId attribute to identifier attribute</td>
      <td style="color: red;">Breaking Change</td>
      <td>
        On the release date, several corrections will be made to the FHIR Coverage resource to comply with USCDI v3 requirements.<br><br>
        The meaning of the <code>subscriberId</code> attribute in the resource is changing, resulting in the following updates:<br>
        <ul>
          <li>Insurance member ID will no longer be provided in the <code>subscriberId</code> attribute. The member ID will now be presented in the <code>identifier</code> attribute instead, and the <code>subscriberId</code> attribute will now represent the identifier for the subscriber, not the member. This will apply for create, read, update, and search endpoints.</li>
          <li>The <code>subscriberid</code> will represent a new optional field within Canvas.</li>
          <li>The <code>subscriberid</code> search parameter will no longer search member IDs; it will now instead search subscriber IDs. The new <code>identifier</code> search parameter will now search member IDs.</li>
        </ul>
        Additionally, we will be making several corrections to code systems in Coverage resources that are returned by read/search endpoints, and consumed by create/update endpoints:
        <ul>
          <li><code>http://hl7.org/fhir/ValueSet/coverage-type</code> will be changing to either <code>http://terminology.hl7.org/CodeSystem/coverage-selfpay</code> (for code value <code>pay</code>) or <code>http://terminology.hl7.org/CodeSystem/v3-ActCode</code> (for all other code values).</li>
          <li><code>http://hl7.org/fhir/ValueSet/subscriber-relationship</code> will be changing to <code>http://terminology.hl7.org/CodeSystem/subscriber-relationship</code></li>
          <li><code>http://hl7.org/fhir/ValueSet/coverage-class</code> will be changing to <code>http://terminology.hl7.org/CodeSystem/coverage-class</code></li>
        </ul>
        To facilitate these changes, the following changes have already been made to FHIR Coverage resource and endpoints:
        <ul>
          <li>The insurance member ID is being populated into and consumed from the <code>identifier</code> attribute.</li>
          <li>Member IDs can be searched using the new <code>identifier</code> search parameter.</li>
          <li>The correct codings listed above have been added to responses from read/search endpoints, and are being consumed by create/update endpoints. On the release date, the incorrect codings will be removed.</li>
        </ul>
        Examples and documentation for the <code>identifier</code> field and the new code system values are available in the <a href="/api/coverage/">FHIR Coverage API documentation</a>.<br><br>
        <strong>API client code must be updated by the release date to avoid disruption.</strong>
      </td>
      <td>10/21/25</td>
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
      <td>FHIR API: Setting appointment location using the location integer value</td>
      <td style="color: red;">Breaking Change</td>
      <td>The FHIR Appointment endpoint now uses the reference from the Location Read/Search endpoint for the Location in supportingInformation. We plan to discontinue support of using the location integer.</td>
      <td>TBD</td>
      <td></td>
    </tr>
</tbody>
</table>
