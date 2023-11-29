---
title: "EHI Export"
layout: documentation
---

<b>This functionality will be available as of 1/1/2024</b>

Canvas supports the <b>export of electronic health information (EHI)</b> based on FHIR Bulk Data Access.

## Format 
EHI is exported as standard FHIR R4 resources in Newline Delimited JSON format, as outlined by the [FHIR Bulk Data Access pattern](https://hl7.org/fhir/uv/bulkdata/STU1.0.1/).

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
