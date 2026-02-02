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
      <td>FHIR API: QuestionnaireResponse questionnaire attribute changing from reference string to absolute URL</td>
      <td style="color: red;">Breaking Change</td>
      <td>
        On the release date, Canvas will change the way the QuestionnaireResponse
        <code>questionnaire</code> attribute is presented. We are making this change to meet USCDI
        v3 requirements.<br><br>
        The <code>questionnaire</code> attribute is currently presented as a reference string, e.g.
        <code>Questionnaire/b357ddc9-c6fc-4a99-a79b-1d0b933afd7a</code>. USCDI v3 requires that this
        attribute be presented as a full URL, e.g. <code>https://fumage-CUSTOMER-ID.canvasmedical.com/Questionnaire/b357ddc9-c6fc-4a99-a79b-1d0b933afd7a</code><br><br>
        This will affect all QuestionnaireResponse endpoints.<br><br>
        <strong>What you need to do to avoid disruption:</strong><br><br>
        The create and update endpoints currently accept either a reference string or an absolute
        URL for the <code>questionnaire</code> attribute. Client code needs to be adjusted to start
        sending the absolute URL of the Questionnaire for this attribute in request bodies. Use the
        example above as a reference, and be sure to replace the customer ID in the example so that
        the base URL matches what you normally use for FHIR requests.<br><br>        
        Read and search endpoints will start returning the absolute URL for this attribute on the
        release date. Client code needs to be adjusted so that it can accept and handle either a
        reference string or an absolute URL for this attribute in response bodies.<br><br>
        <strong>Making these two changes before the release date will ensure that your use of the
        QuestionnaireResponse endpoints will be unaffected by this change.</strong> 
      </td>
      <td>02/02/26</td>
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
