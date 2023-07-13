---
title: "Condition"
---

# FHIR Specification

http://hl7.org/fhir/us/core/STU3.1.1/StructureDefinition-us-core-condition.html

# Fields Supported by Canvas

```json
{
    "resourceType": "Condition",
    "id": "00a6a9f1-ffdb-4cf8-8e11-f2d6459dec3f",
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note": [
        {
            "text": "Condition note"
        }
    ]
}
```

# Read

## Example

```shell
curl --location 'https://fumage-customer.canvasmedical.com/Condition/00a6a9f1-ffdb-4cf8-8e11-f2d6459dec3f' \
     --header 'Content-Type: application/fhir+json' \
     --header 'Authorization: Bearer <token>'
```

## Error Codes

- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

# Search

## Example

```shell
curl --location 'https://fumage-customer.canvasmedical.com/Condition?patient=Patient%2Fb8dfa97bdcdf4754bcd8197ca78ef0f0' \
     --header 'Content-Type: application/fhir+json' \
     --header 'Authorization: Bearer <token>'
```

## Search Parameters Supported by Canvas

* `_id`
* `patient`

## Error Codes

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

# Create

## Usage Notes

If `clinicalStatus` is **active**, the Condition will be added as a `Diagnose` command. If it is not
**active**, the Condition will be added as a `Past Medical History` command.

If `encounter` is provided, the Condition will be added to existing encounter (note). If it is not
provided, a new data import note will be created.

### Fields

- `clinicalStatus`: supported codes are: **active**, **resolved**
- `verificationStatus`: supported codes are: **confirmed**, **entered-in-error**
- `category`: supported codes are: **encounter-diagnosis**
- `code`: supported codes are from: http://hl7.org/fhir/sid/icd-10-cm
- `onsetDateTime`: must be a YYYY-MM-DD date
- `abatementDateTime`: must be a YYYY-MM-DD date
- `recordedDate`: must be a full ISO 8601 datetime

## Example

```shell
curl --location 'https://fumage-customer.canvasmedical.com/Condition' \
     --header 'Content-Type: application/fhir+json' \
     --header 'Authorization: Bearer <token>' \
     --data '
{
    "resourceType": "Condition",
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ],
        "text": "Confirmed"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note": [
        {
            "text": "Condition note"
        }
    ]
}'
```

## Error Codes

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 405 Method Not Allowed
- 422 Unprocessable Entity

# Update

## Usage Notes

The only type of Condition update interaction that is supported by Canvas is to mark an existing
Condition as **entered-in-error**. No changes to other fields will be processed.

## Example

```shell
curl --location --request PUT 'https://fumage-customer.canvasmedical.com/Condition/00a6a9f1-ffdb-4cf8-8e11-f2d6459dec3f' \
     --header 'Content-Type: application/fhir+json' \
     --header 'Authorization: Bearer <token>' \
     --data '
{
    "resourceType": "Condition",
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "resolved",
                "display": "Resolved"
            }
        ],
        "text": "Resolved"
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "entered-in-error",
                "display": "Entered in Error"
            }
        ],
        "text": "Entered in Error"
    },
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                    "code": "encounter-diagnosis",
                    "display": "Encounter Diagnosis"
                }
            ],
            "text": "Encounter Diagnosis"
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://hl7.org/fhir/sid/icd-10-cm",
                "code": "V97.21XS",
                "display": "Parachutist entangled in object, sequela"
            }
        ],
        "text": "Parachutist entangled in object, sequela"
    },
    "subject": {
        "reference": "Patient/b8dfa97bdcdf4754bcd8197ca78ef0f0"
    },
    "encounter": {
        "reference": "Encounter/eae3c8a5-a129-4960-9715-fc26da30eccc"
    },
    "onsetDateTime": "2023-06-15",
    "abatementDateTime": "2023-06-17",
    "recordedDate": "2023-06-18T15:00:00-04:00",
    "recorder": {
        "reference": "Practitioner/76428138e7644ce6b7eb426fdbbf2f39"
    },
    "note": [
        {
            "text": "Condition note"
        }
    ]
}'
```

## Error Codes
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 Method Not Allowed
- 412 Precondition Failed
- 422 Unprocessable Entity
