---
title: 2023 Real World Testing Results
date: 2024-01-31
layout: betas
permalink: /product-updates/rwt-2023-results/
---

This page contains a list of the steps taken to conduct the annual Real World Testing requirements for ONC certification for the 2023 reporting year. The Results within this were reviewed as Screenshots and spreadsheets for their compliance with the criteria defined in the test plan. These artifacts will be maintained by the health IT developer for audit purposes or further requests.

## General Information

**Developer Name:** Canvas Medical, Inc <br>
**Product Name(s):** Canvas <br>
**Version Number(s):** 1 <br>
**Certified Health IT:** 2015 Cures Update <br>
**CHPL Product Number:** 15.04.04.3112.Canv.01.00.1.220523 <br>
**Developer Real World Testing URL:** https://www.canvasmedical.com/compliance/onc/mandatory-disclosures

## Changes to Original Plan

| Summary of Change | Reason | Impact |
| --- | --- | --- |
| 70.315 (g)(7): Application Access - Patient Selection:  We intended to report on the number of patient-restricted tokens with a reduced set of scope. We instead tested the functionality through quarterly interactive live testing using the Inferno Tests.  | Our quarterly reports showed no to little use of this functionality. When reviewing the results, the numbers were questioned due to specific knowledge of a customer’s recent adoption. It was discovered that the reports would only reflect 10 hours of tokens, as they were being deleted after 10 hours due to our security protocols.  | The functionality was tested live and was also confirmed to be working based on customer feedback. Our team is implementing logging to have better reporting of this feature in the future.  |
| 170.315 (e)(1): View, Download, and Transmit to 3rd Party (Cures Update): We combined the metric to group viewed and downloaded. We also conducted live testing to confirm both options were available to patients.  | Our reporting could not differentiate between the two actions taken by patients.  | Our real world metrics do not necessarily confirm that both interactions are working as intended so we added live interactive testing to confirm.   |

## Withdrawn Products

We have not withdrawn any products within the past year that we previously included in the Real World Testing plan.

## Summary and Key Findings

Canvas Medical v1 is a certified electronic health record (ehr) that is sold to ambulatory primary care clinics and tech-enabled multispecialty provider organizations operating in hybrid settings (telehealth and in-person).

Functionality within Canvas is shared across all supported care settings and so our Real World Testing plan was designed to incorporate data from our entire customer base.

Our test plan focused on capturing and documenting the number of instances that each certified capability (listed below) is successfully utilized in the real world. In instances where no evidence exists due to zero adoption of a certified capability or the inability to capture evidence of successful use for other reasons, we will demonstrate the required certified capability using interactive testing methods in a semi-controlled setting as close to a “real world” implementation as possible.

Adoption of certified functionality has been low within our customer base. Many of our customers are either direct-to-consumer or focus on employer or commercial contracts.

We did run across some issues during live testing with the functionality that is not widely used by customers. We make fast and frequent changes to our platform, and in doing so, unintentionally altered some of the lesser used and therefore understood features. Post testing - all non-conformities were reported within 30 days and quickly corrected. 

We also discovered some deficits in our reporting capabilities. We set out to capture each measure at the most granular level. Additional logging is needed to do that in some areas. That work has been started in order to better support the 2024 reporting year. 

## Standards Updates (SVAP and USCDI)

For CY 2023, Canvas did not make any version updates on approved standards through the SVAP process. This applies to all test scenarios described within.

## Care Settings

Canvas markets to provider organizations that operate in hybrid settings. Most customers deliver care to patients using a combination of of the following:

- In-person, office-based visits
- Synchronous telehealth visits
- Asynchronous digital consultations
- In-Facility or in-home visits
- Field-based visits

## Metrics and Outcomes

### **170.315 (b)(1):** Transitions of Care (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Create a Valid CCDA<br/><br/><strong>INTERACTIVE</strong>:<br/>1) A CCDA of each type (Referral Note and CCD) will be created in Canvas and uploaded to another EHR. A user in the receiving EHR will demonstrate a triumphant display of all required elements.<br/><br/></td>
            <td><strong>Expected Outcome</strong>: Success is when a different EHR receives and recognizes each type of CCDA as conformant.</td>
            <td>Q1: <strong>Pass</strong><br/>Q2: <strong>Fail</strong><br/>Q3: <strong>Pass</strong><br/>Q4: <strong>Pass</strong></td>
            <td>The CCD created in Q2 failed to load into athenanet. The ETT identified several non-conformities that had been introduced and were reported within 30 days. We entered a CAP to make the necessary corrections</td>
        </tr>
        <tr>
            <td>Create and send a CCDA<br/>1) Number of CCDAs sent via edge protocols<br/></td>
            <td><strong>Expected Outcome</strong>: Success will be measured through volume. As our customers implement this tool, usage will demonstrate that the capability is available and effective.</td>
            <td><strong>Pass</strong><br/><br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 0<br/></td>
            <td>none</td>
        </tr>
        <tr>
            <td>Receive and display a CCDA<br/>1) Number of CCDAs received via edge protocols<br/></td>
            <td><strong>Expected Outcome</strong>: Success will be measured through volume. As our customers implement this tool, usage will demonstrate that the capability is available and effective.</td>
            <td><strong>Pass</strong> <br/><br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 11<br/></td>
            <td>none</td>
        </tr>
    </tbody>
</table>




### **170.315 (b)(2):** Clinical Information Reconciliation and Incorporation (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Receive and reconcile a CCDA<br/><br/>1) Percentage of CCDAs imported successfully<br/><br/>2) Number of CCDA Import Notes Created<br/><br/>3) Number of CCDA Import Notes Reconciled and Locked<br/></td>
            <td><strong>Expected Outcome:</strong> Success will be measured through volume. Our expectation is there will be low utilization by providers with a high success rate (with expected errors).</td>
            <td>1)<br/>Q1: 75% (3/4)<br/>Q2: 0% (0/2)<br/>Q3: 0% 0/9 <br/>Q4: 40% 2/5 <br/><br/>2)<br/>Q1: 3<br/>Q2: 0<br/>Q3: 0<br/>Q4 2<br/><br/>3)<br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 0<br/></td>
            <td>The small sample size is mainly reflective of some testing by customers. The high error rates were evaluated and the errors were expected and due to file non-conformance or the inability to match patients. </td>
        </tr>
    </tbody>
</table>




### **170.315 (b)(3):** Electronic Prescribing (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Enable a user to perform the following (...) prescription-related electronic transactions<br/><br/>1) Number of and success rates for:<br> NewRx<br> RxChange<br>CancelRx<br>RxRenewal<br>RxFill<br>Medication History<br/></td>
            <td><strong>Justification: </strong>Evaluating a statistically significant sample size of electronic prescriptions spanning multiple organizations using Canvas will demonstrate the real-world utility of the feature.<br/><br/><br/><strong>Expected Outcome</strong>: Transactions are successfully delivered with standard errors (e.g., pharmacy does not support electronic transactions). Data validation errors are prevented, or the end-user is notified of the errors when applicable.</td>
            <td><strong>Pass</strong><br><br><strong>NewRx</strong><br/>Q1: 32423 99.12%<br/>Q2: 26949 99.25%<br/>Q3: 33140 98.77%<br/>Q4: 34211 98.34%<br/><br/><strong>RxChange<br/></strong>n/a<br/><br/><strong>CancelRx<br/></strong>n/a<br/><br/><strong>RxRenewal<br/></strong>Q1: 24635 98.72%<br/>Q2: 26991 98.23%<br/>Q3: 28213 98.38%<br/>Q4: 30484 98.61%<br/><br/><strong>RxFill<br/></strong>Q1: 14535 100%<br/>Q2: 23472 100%<br/>Q3: 227696 100%<br/>Q4: 510027 100%<br/><br/><strong>Medication History<br/></strong>Q1: n/a<br/>Q2: n/a<br/>Q3: n/a<br/>Q4: 191676 100%<br/></td>
            <td>Our customers did not opt in or adopt some of the workflows to facilitate certain transaction types<br/><br/>Users received common validation warnings/errors from the application as expected for missing data requirements/etc.<br/></td>
        </tr>
    </tbody>
</table>


### **170.315 (c)(1):** Clinical Quality Measures - Record and Export

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Record & Export<br/>1) Number of measures recorded during the period<br/><br/><br/>2) Number of QRDA Category 1 files exported<br/></td>
            <td><strong>Expected Outcome: </strong>Success will be measured through volume. We expect moderate utilization of our eCQMs with high success rates but limited utilization of the export functionality.</td>
            <td><strong>Pass</strong><br/><br/>1)<br/>Q1: 0 <br/>Q2: 0 <br/>Q3: 0 <br/>Q4: 0 <br/><br/><br/>2)<br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 0<br/></td>
            <td>No adoption</td>
        </tr>
    </tbody>
</table>




### **170.315 (c)(2):** Clinical Quality Measures - Import and Calculate

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Import & Calculate every CQM (clinical quality measure)<br/><br/>1) Number of QRDA Category 1 files imported (if applicable)<br/></td>
            <td><strong>Expected Outcome: </strong>Success will be measured through volume. We expect limited utilization of the import functionality.</td>
            <td><strong>Pass</strong><br/><br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 0<br/></td>
            <td>No adoption</td>
        </tr>
    </tbody>
</table>


### **170.315 (c)(3):** Clinical Quality Measures - Report (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Enable a user to create a data file for transmission electronically<br/><br/>1) Number of QRDA Category 3 aggregate report(s) created over the period<br/></td>
            <td><strong>Expected Outcome: </strong>Success will be measured through volume. We expect limited utilization of the reporting functionality.</td>
            <td><strong>Pass</strong><br/><br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 0<br/></td>
            <td>No adoption</td>
        </tr>
    </tbody>
</table>

### **170.315 (e)(1):** View, Download, and Transmit to 3rd Party (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Preview CCD or Download CCD<br/><br/>1) System logs will be evaluated to identify patients with a successful CCD document preview or download in the patient app.</td>
            <td><strong>Justification:</strong> Many of our customers have developed their own patient-facing applications. For those using the Canvas patient web app, usage will demonstrate the ability of a patient to download a CCD document template in the live production environment of their patient app.<br/><br/><strong>Expected Outcome:</strong> Success is defined by the number of patients with successful CCD document previews or downloads. We expect usage to be limited.</td>
            <td><strong>Pass</strong><br/><br/>Q1: 14<br/>Q2: 14<br/>Q3: 5<br/>Q4: 14</td>
            <td>Our current reporting does not differentiate between a patient viewing and downloading their data. We are adding additional logging to track.</td>
        </tr>
        <tr>
            <td>Transmit CCD<br/><br/>1) System logs will be evaluated to identify patients with a successful CCD document transmission in the patient app.</td>
            <td><strong>Justification:</strong> This measure will demonstrate the ability of a patient to transmit a CCD document template in the live production environment of their patient app. The ability to send via Direct is tied to the implementation of DataMotion as a relied upon software.<br/><br/><strong>Expected Outcome:</strong> CCD documents were successfully sent via email and Direct with the expected errors (e.g., invalid direct address, lack of response, etc.). We expect usage to be limited as many of our customers have developed their own patient-facing applications.</td>
            <td><strong>Pass</strong><br/><br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 0</td>
            <td>Adoption of DataMotion was limited due to customers not leveraging our patient experience.</td>
        </tr>
    </tbody>
</table>

### **170.315 (f)(1):** Transmission to Immunization Registries

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Record immunizations and generate the HL7 v2.5.1 Z22 VXU immunization information messages<br/><br/>1) Percentage of immunization records submitted to immunization registries</td>
            <td><strong>Justification:</strong> We intend to record the frequency that immunization data is submitted to registries to demonstrate the certified capability is available and effective, regardless of the frequency it is used.<br/><br/><strong>Expected Outcome:</strong> We expect limited volume with a high rate of success.</td>
            <td><strong>Pass</strong><br/><br/>Q1: 0<br/>Q2: 0<br/>Q3: 0<br/>Q4: 0</td>
            <td>No adoption</td>
        </tr>
    </tbody>
</table>

### **170.315 (f)(5):** Transmission to Public Health Agencies - Electronic Case Reporting (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Consume and Maintain Table of Reportable Condition Trigger CodesCreate a case report for the patient encounter(s) based on a matched trigger<br/><br/><br/><strong>INTERACTIVE<br/><br/></strong>1) Provider will document a condition from the trigger code table in a test encounter</td>
            <td><strong>Justification:</strong> While Canvas provides the capability for electronic case reporting, there has been zero adoption to date. Therefore, we plan to demonstrate real-world performance through interactive testing.<br/><br/><br/><strong>Expected Outcome:</strong> Success is when a case report is generated for the patient encounter(s) based on a matched trigger.</td>
            <td>Q1: <strong>Fail</strong><br/>Q2: <strong>Pass</strong><br/>Q3: <strong>Pass</strong><br/>Q4: <strong>Pass</strong></td>
            <td>A nonconformity was discovered during Q1 testing and reported within 30 days. It was resolved under a CAP.</td>
        </tr>
    </tbody>
</table>



### **170.315 (g)(7):** Application Access - Patient Selection

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Receive a request with sufficient information to uniquely identify a patient and return an ID or other token that can be used by an application to subsequently execute requests for that patient's data.<br/><br/><br/><strong>INTERACTIVE<br/><br/></strong>1) Run the inferno tests on the production API service with test patient data.</td>
            <td><strong>Justification:</strong> The evaluation of a statistically significant sample size of API requests spanning a broad spectrum of API Information Sources will demonstrate the real-world utility of the API<br/><br/><br/><strong>Expected Outcome: </strong>Success is defined by passing the Inferno test using the production API and verifying that the documentation is complete</td>
            <td>Q1: <strong>Pass</strong><br/>Q2: <strong>Pass</strong><br/>Q3: <strong>Pass</strong><br/>Q4: <strong>Pass</strong></td>
            <td>We ran into reporting limitations and therefore leveraged our inferno test results to demonstrate the capability</td>
        </tr>
    </tbody>
</table>


### **170.315 (g)(9):** Application Access - All Data Request (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Respond to requests for patient data for all of the data categories specified in the Common Clinical Data Set.<br/><br/>1) Number of requests for a patient’s Summary Record made by an application via an all data category request using a valid patient ID or token</td>
            <td><strong>Justification:</strong> The evaluation of a statistically significant sample size of API requests spanning a broad spectrum of API Information Sources will demonstrate the real-world utility of the API<br/><br/><br/><strong>Expected Outcome: </strong>Our expectation is there will be low utilization by external applications with a high success rate (including expected errors that could include failure in authorization/authentication, incorrectly formatted request, etc.)</td>
            <td><strong>Pass</strong><br/><br/>Q1: 0 <br/>Q2: 0 <br/>Q3: 0<br/>Q4: 961<br/></td>
            <td>None</td>
        </tr>
        <tr>
            <td>Respond to requests for patient data associated with a specific date as well as requests for patient data within a specified date range.<br/><br/>1) Number of requests for a patient’s Summary Record made by an application via an all data category request using a valid patient ID or token for a specific date range</td>
            <td><strong>Justification:</strong> The evaluation of a statistically significant sample size of API requests spanning a broad spectrum of API Information Sources will demonstrate the real-world utility of the API<br/><br/><br/><strong>Expected Outcome: </strong>Our expectation is there will be low utilization by external applications with a high success rate (including expected errors that could include failure in authorization/authentication, incorrectly formatted request, etc.)</td>
            <td><strong>Pass</strong><br/><br/>Q1: 0 <br/>Q2: 0 <br/>Q3: 0<br/>Q4: 0</td>
            <td>None</td>
        </tr>
    </tbody>
</table>


### **170.315 (g)(10):** Standardized API for Patient and Population Services (Cures Update)

<table>
    <thead>
        <tr>
            <th style="width:25%"><strong>Requirement(s)</strong></th>
            <th style="width:25%"><strong>Justification & Expected Outcome</strong></th>
            <th style="width:25%"><strong>Results</strong></th>
            <th style="width:25%"><strong>Challenges Encountered</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Standardized API for Patient and Population Services<br/><br/><br/><strong>INTERACTIVE<br/><br/></strong>1) Run the inferno tests on the production API service with test patient data.2) Review of the documentation for required elements</td>
            <td><strong>Justification: </strong>The standardized testing tool reflects a wider variety of features that our customers employ and is therefore the most thorough method of showing real-world capabilities. <br/><br/><br/><strong>Expected Outcome: </strong>Success is defined by passing all sections of the Inferno test using the production API and verifying that the documentation is complete</td>
            <td>Q1: <strong>Fail</strong><br/>Q2: <strong>Pass</strong><br/>Q3: <strong>Pass</strong><br/>Q4: <strong>Pass</strong><br/></td>
            <td>An issue was discovered during Q1 testing and reported within 30 days. No non-conformity was found.</td>
        </tr>
    </tbody>
</table>



## Key Milestones

<table id="146a53a9-ffd1-4585-b433-5d25b81d0ea2">
    <tbody>
        <tr id="19d78398-b704-4ef3-8a6e-621cb4789c0a">
            <td style="width:50%"><strong>Requirement(s)</strong></td>
            <td style="width:50%"><strong>Justification & Expected Outcome</strong></td>
        </tr>
        <tr id="19d78398-b704-4ef3-8a6e-621cb4789c0a">
            <td style="width:50%">Finalization of the Real World Testing plan</td>
            <td style="width:50%">December 2022</td>
        </tr>
        <tr id="830481ed-8c50-4436-aba5-e44639d2e089">
            <td style="width:50%">Development of candidate list of providers to assist with interactive Real World Testing</td>
            <td style="width:50%">December 2022</td>
        </tr>
        <tr id="7b12e91d-09c2-4c55-b2c2-d0e7c17af380">
            <td style="width:50%">Data collection and interactive testing</td>
            <td style="width:50%">2023 - Quarterly</td>
        </tr>
        <tr id="561dedce-9869-40e1-95a1-adf2f8cf3447">
            <td style="width:50%">Validation of expected outcomes</td>
            <td style="width:50%">2023 - Quarterly</td>
        </tr>
        <tr id="31c41109-9f96-45cf-8dc6-4643b876b19a">
            <td style="width:50%">Analysis and report creation</td>
            <td style="width:50%">January 2023</td>
        </tr>
        <tr id="f952f9e1-6764-46d8-a3f1-434fac614fe3">
            <td style="width:50%">Submit Real World Testing Report to ACB</td>
            <td style="width:50%">February 2024</td>
        </tr>
    </tbody>
</table>

