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
      <td>FHIR API: Condition category handling</td>
      <td style="color: red;">Breaking Change</td>
      <td>
        On the release date, Canvas will handle the <code>category</code> attribute on the FHIR
        Condition resource differently in order to meet USCDI v3 requirements.<br><br>
        Currently, the <code>category</code> attribute for all Conditions is required to be
        <code>encounter-diagnosis</code>. On the release date, the following changes will take
        effect:<br>
        <ul>
          <li>
            The Condition create and update endpoints will accept <code>encounter-diagnosis</code>,
            <code>problem-list-item</code>, or <code>health-concern</code> for the <code>code</code>
            attribute of the category coding.
          </li>
          <li>
            The Condition read and search-type endpoints will return
            <code>encounter-diagnosis</code>, <code>problem-list-item</code>, or
            <code>health-concern</code> for the <code>code</code> attribute of the category coding,
            based on what is stored in the database for the Condition.
          </li>
          <li>
            Conditions created by the Diagnose command will have <code>category</code> set to
            <code>problem-list-item</code>. The Diagnose command will be enhanced in the future to
            enable use of the other value options for <code>category</code>.
          </li>
          <li>
            The <code>category</code> for all existing Conditions in the database will be set to
            <code>problem-list-item</code>.
          </li>
        </ul>
        <strong>What you need to do:</strong><br>
        <ul>
          <li>
            All client code that makes use of the Condition create or update endpoints must be
            updated before the release date so that <code>problem-list-item</code> is sent instead
            of <code>encounter-diagnosis</code>. Please note that until we make the breaking change,
            even if you send <code>problem-list-item</code>, we will continue returning you
            <code>encounter-diagnosis</code> from read and search endpoints until we make the
            breaking change.
          </li>
          <li>
            All client code that makes use of the read or search endpoints must be updated if they
            reference the <code>category</code> attribute to flexibly handle either
            <code>encounter-diagnosis</code> or <code>problem-list-item</code>.
          </li>
        </ul><br>
        <strong>Making these two changes before the release date will ensure that your use of the endpoint
        will be unaffected by this change.</strong> 
      </td>
      <td>12/08/25</td>
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
