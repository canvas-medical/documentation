---
title: "Observation"
---

## Observation Create
[block:callout]
{
  "type": "info",
  "title": "Currently the Observation Create Endpoint can only be used to generate vital sign panels and vital signs.",
  "body": "Although the observation endpoint houses many different Canvas models, currently, only vital signs and panels can be created through this endpoint."
}
[/block]

[block:callout]
{
  "type": "success",
  "title": "Note In Patient Timeline",
  "body": "Traditionally most our FHIR endpoints will insert commands into a Data Import Note type on the patient's timeline. However with the release of [configurable note types](https://canvas-medical.zendesk.com/hc/en-us/articles/6623684024083-Note-Types-) if you specify a new Note Type with \n           system = Canvas\n           code = VitalsImport \nthen this Observation Create endpoint will always import into that note type."
}
[/block]
### Vital signs and Vital Sign Panels
Vital sign panels and vital signs are both observations. Their relationship with one another is outlined below:
- Vital sign panels are the "parent" that "contain" all of the vital sign observations. These vital signs are linked to the panel using the `hasMembers` attribute. 
- Each vital sign links back to a "parent" vital sign panel. If a parent vital sign panel is not linked (via the `derivedFrom` attribute), a new vital sign panel observation is created and will autofill the derivedFrom attribute field. 

Vital signs and their "parent" panel feed into our [Vitals command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs). 

### Getting the newly-created observation's ID.
Upon successful creation, the Canvas-issued identifier assigned for the new resource can be found in the `Location:` header. You will use this for subsequent requests that reference this observation, such as linking vital sign observations to an observation representing a vital sign panel.

### Observation Attributes:

Canvas accepts a FHIR standard request body, you may refer to [FHIR Observation Documentation](https://build.fhir.org/observation.html) to help out in building your observation request. Below is our documentation on how Canvas specifically will use each attribute.

### category [REQUIRED]

The `category` attribute's code should be set to "vital-signs" or the request will error. `system` and `display` are not validated or required. Only the first item in the coding list will be used. All other codings will be ignored. 
```
{
  "codes": [
    {
      "code": "\t\t\"category\": [\n        {\n            \"coding\": [\n                {\n                    \"system\": \"http://terminology.hl7.org/CodeSystem/observation-category\",\n                    \"code\": \"vital-signs\",\n                    \"display\": \"Vital Signs\"\n                }\n            ]\n        }\n    ]",
      "language": "text"
    }
  ]
}
```
### code [REQUIRED]

The code attribute contains the coding for the type of information the observation endpoint is accessing. The codings either code for a specific vital sign or a vital sign panel.
- `system` and `display` are not required nor are they validated. 
- `coding` is required and validated. It must be a coding of the vital sign panel or a vital sign that is supported by Canvas. If it is not supported, you will see a 422 error with the following message: "Requested Sign does not exist". The supported vital signs, their codings, and supported units are listed below:
[block:parameters]
{
  "data": {
    "h-0": "vital sign",
    "h-1": "LOINC code",
    "h-2": "default unit",
    "h-3": "additional accepted units",
    "0-0": "vital sign panel",
    "2-0": "weight",
    "4-0": "pulse rate",
    "5-0": "body temperature",
    "6-0": "oxygen saturation (arterial)*",
    "7-0": "oxygen saturation*",
    "8-0": "respiration rate",
    "9-0": "waist circumference",
    "10-0": "note",
    "11-0": "pulse rhythm",
    "0-1": "85353-1",
    "2-1": "29463-7",
    "4-1": "8867-4",
    "3-0": "height",
    "3-1": "8302-2",
    "5-1": "8310-5",
    "6-1": "2708-6",
    "7-1": "59408-5",
    "8-1": "9279-1",
    "9-1": "56086-2",
    "10-1": "80339-5",
    "11-1": "8884-9",
    "1-1": "85354-9",
    "1-0": "blood pressure",
    "0-2": "",
    "1-2": "mmHg",
    "2-2": "oz",
    "3-2": "in",
    "4-2": "bpm",
    "5-2": "°F",
    "6-2": "%",
    "7-2": "%",
    "8-2": "bpm",
    "9-2": "cm",
    "10-2": "",
    "11-2": "",
    "2-3": "lbs, kg",
    "3-3": "cm",
    "9-3": "in"
  },
  "cols": 4,
  "rows": 12
}
[/block]
*If an oxygen saturation vital sign is created, an oxygen saturation (arterial) vital sign code is also automatically generated.*
```
{
  "codes": [
    {
      "code": "\t\t\"code\": {\n        \"coding\": [\n            {\n            \t\t\"system\": \"http://loinc.org\",\n            \t\t\"code\": \"29463-7\",\n            \t\t\"display\": \"Weight\"\n            }\n        ]\n    }",
      "language": "text"
    }
  ]
}
```
###  subject [REQUIRED]

Subject ingests the ID of the patient from whom the vital signs were taken. It must be a patient that exists in your instance.
```
{
  "codes": [
    {
      "code": "\"subject\": {\n        \"reference\": \"Patient/ee8672f3497e4a83937b9e71d0a704a5\"\n},",
      "language": "text"
    }
  ]
}
```
###  effectiveDateTime [REQUIRED]

`effectiveDateTime` ingests the date and time that the vitals or vitals panel was recorded. This is a DateTime. This time will display as the time of import for the note that contains the vitals panel. For an individual vital sign, if the effectiveDateTime differs from the panel time, it will be reflected in a read/search; however, you will not see the individual date in the UI, only the panel's datetime. 
```
{
  "codes": [
    {
      "code": "\"effectiveDateTime\": \"2022-07-29T08:50:24.883809+00:00\"",
      "language": "text"
    }
  ]
}
```
### valueQuantity

This attribute ingests the data associated with the vital sign that was indicated by the coding. If the observation is a vital sign panel, the valueQuantity will be ignored. 

A valid unit (which is specific to the vital sign being entered) must be entered for `unit`. Inputting an incorrect unit will result in a 422 error with the following message: "Invalid sign unit detected for weight". If unit is omitted, the it will default to the unit documented in the table above. 

If `value` is omitted, it will default to an empty field. If this field's input type cannot be converted to the given vital sign's expected type (e.g. a string "fifty" is given for weight), it will display on the Canvas UI's patient chart on the left-hand column under vitals, but it will not display in the Vitals command that is generated on an imported note. It will be saved in the database and returned in a read/search. 

Note: Blood pressure vital sign observations support components for diastolic and systolic blood pressure. However, if only the components are included, and this `valueQuantity` isn't included (e.g. "100/80"), it will not display on the Canvas UI. 

Note: When creating a vital sign for pulse rhythm, the accepted values are:
- Regular
- Irregularly Irregular
- Regulary Irregular
```
{
  "codes": [
    {
      "code": " \"valueQuantity\": {\n        \"value\": 50,\n        \"unit\": \"kg\"\n },",
      "language": "text"
    }
  ]
}
```
### derivedFrom 
This attribute is used to link a vital sign to its "parent" vital sign panel. It ingests a reference to the vital sign panel's observation. This observation ID can be found using the [Observation Search](ref:observation-search). It is important to note that each vital sign panel can only contain a single vital sign of each type. Adding a duplicate of a vital sign will result in a 422 error: "Vital sign reading already exists for the given reading". 
```
{
  "codes": [
    {
      "code": "\"derivedFrom\": [\n    {\n       \"reference\": \"Observation/6173fbe8-110e-4a4a-9647-e949f7b1c35e\"\n    }\n]",
      "language": "text"
    }
  ]
}
```
### hasMembers
This attribute is used to link the vital signs that are members of all the same vital sign panel. It is a list of references to vital sign observations. 

If a new vital sign panel is created and links pre-existing vital signs via the hasMember attribute, those linked observations will update their derivedFrom attribute to be set to the newly created vital sign panel. 
```
{
  "codes": [
    {
      "code": "\"hasMember\": [\n    {\n       \"reference\": \"Observation/6173fbe8-110e-4a4a-9647-e949f7b1c35e\"\n    },\n    {\n       \"reference\": \"Observation/2533fbe9-333f-4a4a-9647-e949f7b1c35f\"\n    }\n]",
      "language": "text"
    }
  ]
}
```
### component

This attribute is only used for blood pressure, as it has two components (systolic and diastolic). These components are added to a vital sign observation by including their code and valueQuantity. The components are what will be stored in the database; however, they will not display on the UI. The valueQuantity for the blood pressure vital sign (e.g. "100/80") will be the one used to generate a display on the UI. The `valueQuantity` for the systolic component should match the first number in the blood pressure vital sign `valueQuantity`, where the `valueQuantity` of the diastole component should match the second number. 
```
{
  "codes": [
    {
      "code": "    \"component\": [ \n        {\n            \"code\": {\n                \"coding\": [\n                                    {\n                            \"system\": \"http://loinc.org\",\n                            \"code\": \"8480-6\",\n                            \"display\": \"BP - Systolic\"\n                        }\n                ]\n            },\n            \"valueQuantity\": {\n                \"value\": \"100\"\n            }\n        },\n                {\n            \"code\": {\n                \"coding\": [\n                                    {\n                            \"system\": \"http://loinc.org\",\n                            \"code\": \"8462-4\",\n                            \"display\": \"BP - Diastole\"\n                        }\n                ]\n            },\n            \"valueQuantity\": {\n                \"value\": \"80\"\n            }\n        }\n    ],",
      "language": "text"
    }
  ]
}
```
### Additional examples

### Creating a vital panel

https://canvasmedical.postman.co/workspace/Canvas-Medical-Interoperability~5af171b4-61c3-4090-89e6-bc10d1970ebb/request/16792990-463cfe84-d9ff-42c9-a110-4fedfe2baa9b

### Creating a vital sign with components (currently should only be used for blood pressure)

https://canvasmedical.postman.co/workspace/Canvas-Medical-Interoperability~5af171b4-61c3-4090-89e6-bc10d1970ebb/request/16792990-4866da6b-f0ec-44d1-8a61-85441dc60ad7

### Creating a vital sign without components

https://canvasmedical.postman.co/workspace/Canvas-Medical-Interoperability~5af171b4-61c3-4090-89e6-bc10d1970ebb/request/16792990-3f5dbfe9-073f-45a6-ba49-38dc80e3c7ce

## Observation Read
This endpoint implements the US Core Laboratory Results Observation Profile. The following USCDI data elements are retrievable from this endpoint:

Laboratory:
- Tests
- Values/Results

Smoking Status:
- Smoking Status

See [Observation Search](ref:observation-search) on more info about specific observation records

## Observation Search
This endpoint implements the US Core Laboratory Results Observation Profile. The following USCDI data elements are retrievable from this endpoint:

Laboratory:
- Tests
- Values/Results

Smoking Status:
- Smoking Status

### Creating an Observation in Canvas

Observations fall into the following categories: 
- social history
- vital signs
- imaging
- laboratory
- procedure
- survey, exam
  - therapy
- activity. 

Below are some links to guide you through creating some observations on the Canvas UI.

To create a vital signs observation, use the [vitals command](https://canvas-medical.zendesk.com/hc/en-us/articles/360056077654-Logging-Vital-Signs). 

To create an imaging observation, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918193-Imaging-Reports).

To create a laboratory observation, see this [Zendesk article](https://canvas-medical.zendesk.com/hc/en-us/articles/360057918713-Lab-Reports).

To create a procedure, use the [perform command](https://canvas-medical.zendesk.com/hc/en-us/articles/360055626874-Perform-Command-for-In-Office-Procedures).

### Specific Notes on Vital Sign Observations

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