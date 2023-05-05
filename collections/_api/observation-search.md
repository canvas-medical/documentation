---
title: "Observation Search"
slug: "observation-search"
excerpt: "List observations"
hidden: false
createdAt: "2022-05-24T13:58:01.704Z"
updatedAt: "2022-08-04T00:24:28.719Z"
---
This endpoint implements the US Core Laboratory Results Observation Profile. The following USCDI data elements are retrievable from this endpoint:

Laboratory:
* Tests
* Values/Results

Smoking Status:
* Smoking Status

## Creating an Observation in Canvas

Observations fall into the following categories: 
- social history
- vital signs
- imaging
- laboratory
- procedure
- survey, exam
-therapy
- activity. 

Below are some links to guide you through creating some observations on the Canvas UI.

To create a vital signs observation, use the [vitals command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs). 

To create an imaging observation, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918193-Imaging-Reports).

To create a laboratory observation, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918713-Lab-Reports).

To create a procedure, use the [perform command](https://canvas-medical.zendesk.com/hc/en-us/articles/360055626874-Perform-Command-for-In-Office-Procedures).

## Specific Notes on Vital Sign Observations

Vital signs can be retrieved from this endpoint. Instead of a `valueCodableConcept`, a vital sign read will contain `valueQuantity`. Values will be converted and displayed in the default unit for that specific sign, similar to how it is displayed in the Vitals command on the UI.

Additionally, individual vital signs have a `derivedFrom` attribute that links them to their parent vital sign panel. 

`issued` is not a field you can create via [Observation Create Intern](ref:observation-create-intern), it is the timestamp in Canvas that the vital's record was ingested. 

Finally, if a vital sign panel is being shown, it may have a `hasMembers` attribute that references the vital signs that are members of the vital sign panel. 

### Example of a result from reading a vital sign without components:
[block:code]
{
  "codes": [
    {
      "code": "{\n    \"resourceType\": \"Observation\",\n    \"id\": \"b235cc5c-e9f7-4d26-8b04-62c792a4b3ec\",\n    \"meta\": {\n        \"versionId\": \"1\",\n        \"lastUpdated\": \"2022-07-27T15:50:26.097+00:00\"\n    },\n    \"status\": \"final\",\n    \"category\": [\n        {\n            \"coding\": [\n                {\n                    \"system\": \"http://terminology.hl7.org/CodeSystem/observation-category\",\n                    \"code\": \"vital-signs\",\n                    \"display\": \"Vital Signs\"\n                }\n            ]\n        }\n    ],\n    \"code\": {\n        \"coding\": [\n            {\n                \"system\": \"http://loinc.org\",\n                \"code\": \"29463-7\",\n                \"display\": \"Weight\"\n            }\n        ]\n    },\n    \"subject\": {\n        \"id\": \"ee8672f3497e4a83937b9e71d0a704a5\",\n        \"reference\": \"Patient/ee8672f3497e4a83937b9e71d0a704a5\"\n    },\n    \"effectiveDateTime\": \"2022-09-29T08:50:24.883809+00:00\",\n    \"issued\": \"2022-07-27T15:50:00.000861+00:00\",\n    \"valueQuantity\": {\n        \"value\": 110.23125,\n        \"unit\": \"lb\",\n        \"system\": \"http://unitsofmeasure.org\",\n        \"code\": \"[lb_av]\"\n    },\n    \"interpretation\": [\n        {\n            \"extension\": [\n                {\n                    \"url\": \"http://hl7.org/fhir/StructureDefinition/data-absent-reason\",\n                    \"valueCode\": \"unknown\"\n                }\n            ],\n            \"text\": \"Unknown\"\n        }\n    ],\n    \"derivedFrom\": [\n        {\n            \"reference\": \"Observation/53950e1b-06d9-4648-a54e-f158e88ea82b\"\n        }\n    ]\n}",
      "language": "text"
    }
  ]
}
[/block]
### Example of a result from reading a blood pressure vital sign with components:
[block:code]
{
  "codes": [
    {
      "code": "{\n    \"resourceType\": \"Observation\",\n    \"id\": \"b80d82ec-1901-4c42-8e4c-42a09b9d3657\",\n    \"meta\": {\n        \"versionId\": \"1\",\n        \"lastUpdated\": \"2022-07-27T16:50:30.438+00:00\"\n    },\n    \"status\": \"final\",\n    \"category\": [\n        {\n            \"coding\": [\n                {\n                    \"system\": \"http://terminology.hl7.org/CodeSystem/observation-category\",\n                    \"code\": \"vital-signs\",\n                    \"display\": \"Vital Signs\"\n                }\n            ]\n        }\n    ],\n    \"code\": {\n        \"coding\": [\n            {\n                \"system\": \"http://loinc.org\",\n                \"code\": \"85354-9\",\n                \"display\": \"Blood Pressure\"\n            }\n        ]\n    },\n    \"subject\": {\n        \"id\": \"ee8672f3497e4a83937b9e71d0a704a5\",\n        \"reference\": \"Patient/ee8672f3497e4a83937b9e71d0a704a5\"\n    },\n    \"effectiveDateTime\": \"2022-09-29T08:50:24.883809+00:00\",\n    \"issued\": \"2022-07-27T16:49:13.228267+00:00\",\n    \"interpretation\": [\n        {\n            \"extension\": [\n                {\n                    \"url\": \"http://hl7.org/fhir/StructureDefinition/data-absent-reason\",\n                    \"valueCode\": \"unknown\"\n                }\n            ],\n            \"text\": \"Unknown\"\n        }\n    ],\n    \"derivedFrom\": [\n        {\n            \"reference\": \"Observation/53950e1b-06d9-4648-a54e-f158e88ea82b\"\n        }\n    ],\n    \"component\": [\n        {\n            \"code\": {\n                \"coding\": [\n                    {\n                        \"system\": \"http://loinc.org\",\n                        \"code\": \"8480-6\"\n                    }\n                ]\n            },\n            \"valueQuantity\": {\n                \"value\": 100,\n                \"unit\": \"mmHg\",\n                \"system\": \"http://unitsofmeasure.org\",\n                \"code\": \"mm[Hg]\"\n            }\n        },\n        {\n            \"code\": {\n                \"coding\": [\n                    {\n                        \"system\": \"http://loinc.org\",\n                        \"code\": \"8462-4\"\n                    }\n                ]\n            },\n            \"valueQuantity\": {\n                \"value\": 80,\n                \"unit\": \"mmHg\",\n                \"system\": \"http://unitsofmeasure.org\",\n                \"code\": \"mm[Hg]\"\n            }\n        }\n    ]\n}",
      "language": "text"
    }
  ]
}
[/block]
### Example of a result from reading a blood pressure vital sign panel:
[block:code]
{
  "codes": [
    {
      "code": "{\n    \"resourceType\": \"Observation\",\n    \"id\": \"53950e1b-06d9-4648-a54e-f158e88ea82b\",\n    \"meta\": {\n        \"versionId\": \"1\",\n        \"lastUpdated\": \"2022-07-27T16:51:14.462+00:00\"\n    },\n    \"status\": \"final\",\n    \"category\": [\n        {\n            \"coding\": [\n                {\n                    \"system\": \"http://terminology.hl7.org/CodeSystem/observation-category\",\n                    \"code\": \"vital-signs\",\n                    \"display\": \"Vital Signs\"\n                }\n            ]\n        }\n    ],\n    \"code\": {\n        \"coding\": [\n            {\n                \"system\": \"http://loinc.org\",\n                \"code\": \"85353-1\",\n                \"display\": \"Vital Signs Panel\"\n            },\n            {\n                \"system\": \"http://loinc.org\",\n                \"code\": \"85354-9\",\n                \"display\": \"Blood Pressure\"\n            },\n            {\n                \"system\": \"http://loinc.org\",\n                \"code\": \"29463-7\",\n                \"display\": \"Weight\"\n            }\n        ]\n    },\n    \"subject\": {\n        \"id\": \"ee8672f3497e4a83937b9e71d0a704a5\",\n        \"reference\": \"Patient/ee8672f3497e4a83937b9e71d0a704a5\"\n    },\n    \"effectiveDateTime\": \"2022-09-29T08:50:24.883809+00:00\",\n    \"issued\": \"2022-07-27T15:49:59.926164+00:00\",\n    \"dataAbsentReason\": {\n        \"coding\": [\n            {\n                \"system\": \"http://terminology.hl7.org/CodeSystem/data-absent-reason\",\n                \"code\": \"not-performed\",\n                \"display\": \"Not Performed\"\n            }\n        ]\n    },\n    \"interpretation\": [\n        {\n            \"extension\": [\n                {\n                    \"url\": \"http://hl7.org/fhir/StructureDefinition/data-absent-reason\",\n                    \"valueCode\": \"unknown\"\n                }\n            ],\n            \"text\": \"Unknown\"\n        }\n    ],\n    \"hasMember\": [\n        {\n            \"reference\": \"Observation/b80d82ec-1901-4c42-8e4c-42a09b9d3657\"\n        },\n        {\n            \"reference\": \"Observation/b235cc5c-e9f7-4d26-8b04-62c792a4b3ec\"\n        }\n    ]\n}",
      "language": "text"
    }
  ]
}
[/block]