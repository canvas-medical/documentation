---
title: "EHI Export"
layout: documentation
---

{% include alert.html type="info" content=" This functionality will be available as of 1/1/2024." %}

Canvas supports the <b>export of electronic health information (EHI)</b> based on FHIR Bulk Data Access.


## Creating a Single Patient Export
To generate a single patient export, navigate to `Fhir bulk data exports` in your admin settings. 

Click on `ADD FHIR BULK DATA EXPORT` to pull up the tool. Select the appropriate Oauth application from the dropdown. These are typically created by your team as a part of implementation. Support can also help to create one if needed. Export type defaults to 'Patient'. Search for the patient and click `Start Export`.

The export will generate links to the output files for each resource. Clicking each will download the files locally. 


{% include alert.html type="warning" content="This functionality is permission based. If you do not have access and need it, please reach out to your internal administrators. They can work with our support team to ensure the permissions are assigned to the necessary groups." %}
<br>


## Format 
EHI is exported as standard FHIR R4 resources in Newline Delimited JSON format, as outlined by the [FHIR Bulk Data Access pattern](https://hl7.org/fhir/uv/bulkdata/STU1.0.1/).
<br>
<br>

## Resources

The resources in scope for the response are:

- The patient resource itself.
- Any resource that is associated with the patient.

The table below lists the Canvas resources included in the patient recordset:

| Resource                       | 
|--------------------------------|
| [AllergyIntolerance](/api/allergyintolerance)             | 
| [Appointment](/api/appointment)                    | 
| [CarePlan](/api/careplan)                       | 
| [CareTeam](/api/careteam)                       |
| [Claim](/api/claim)                          | 
| [Communication](/api/communication)                  | 
| [Condition](/api/condition)                      | 
| [Consent](/api/consent)                        | 
| [Coverage](/api/coverage)                         | 
| [CoverageEligibilityResponse](/api/coverageeligibilityresponse)      | 
| [Device](/api/device)                 | 
| [DiagnosticReport](/api/diagnosticreport)                 | 
| [DocumentReference](/api/documentreference)                | 
| [Encounter](/api/encounter)                        | 
| [Goal](/api/goal)                             |  
| [Immunization](/api/immunization)                     | 
| [Media](/api/media)                 | 
| [MedicationRequest](/api/medicationrequest)                 | 
| [MedicationStatement](/api/medicationstatement)               | 
| [Observation](/api/observation)                       | 
| [Patient](/api/patient)                           | 
| [Procedure](/api/procedure)                           | 
| [Provenance](/api/provenance)                           | 
| [QuestionnaireResponse](/api/questionnaireresponse)             | 
| [Task](/api/task)                              | 
