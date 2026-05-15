---
title: "Medication History"
slug: "data-medication-history"
excerpt: "Canvas SDK Medication History"
hidden: false
---

## Introduction

The `MedicationHistoryMedication` model represents historical medication data for a patient, typically imported from external sources such as health information exchanges or pharmacy systems. The `MedicationHistoryResponse` model tracks responses to medication history requests.

## Basic usage

To get a medication history record by identifier, use the `get` method on the `MedicationHistoryMedication` model manager:

```python
from canvas_sdk.v1.data.medication_history import MedicationHistoryMedication

medication_history = MedicationHistoryMedication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")
```

If you have a patient object, the medication history for a patient can be accessed with the `medication_history_medications` attribute on a `Patient` object:

```python
from canvas_sdk.v1.data.patient import Patient

patient = Patient.objects.get(id="1eed3ea2a8d546a1b681a2a45de1d790")
medication_history = patient.medication_history_medications.all()
```

## Codings

The codings for a medication history record can be accessed with the `codings` attribute on a `MedicationHistoryMedication` object:

```python
from canvas_sdk.v1.data.medication_history import MedicationHistoryMedication
from logger import log

medication_history = MedicationHistoryMedication.objects.get(id="b80b1cdc-2e6a-4aca-90cc-ebc02e683f35")

for coding in medication_history.codings.all():
    log.info(f"system:  {coding.system}")
    log.info(f"code:    {coding.code}")
    log.info(f"display: {coding.display}")
```

## Filtering

Medication history records can be filtered by any attribute that exists on the model.

Filtering is done with the `filter` method on the `MedicationHistoryMedication` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data.medication_history import MedicationHistoryMedication

medications = MedicationHistoryMedication.objects.filter(dea_schedule="CII")
```

### By date range

Filter by last fill date or written date:

```python
from canvas_sdk.v1.data.medication_history import MedicationHistoryMedication
from datetime import datetime

medications = MedicationHistoryMedication.objects.filter(
    last_fill_date__gte=datetime(2023, 1, 1)
)
```

## Attributes

### MedicationHistoryMedication

| Field Name                        | Type                                                    |
| --------------------------------- | ------------------------------------------------------- |
| id                                | UUID                                                    |
| dbid                              | Integer                                                 |
| created                           | DateTime                                                |
| modified                          | DateTime                                                |
| patient                           | [Patient](/sdk/data-patient/#patient)                  |
| drug_description                  | String                                                  |
| strength_value                    | String                                                  |
| strength_form                     | String                                                  |
| strength_unit_of_measure          | String                                                  |
| quantity                          | Float                                                   |
| quantity_unit_of_measure          | String                                                  |
| quantity_code_list_qualifier      | String                                                  |
| days_supply                       | Integer                                                 |
| last_fill_date                    | DateTime                                                |
| written_date                      | DateTime                                                |
| other_date                        | DateTime                                                |
| other_date_qualifier              | String                                                  |
| substitutions                     | Boolean                                                 |
| refills_remaining                 | Integer                                                 |
| diagnosis_code                    | String                                                  |
| diagnosis_qualifier               | String                                                  |
| diagnosis_description             | String                                                  |
| secondary_diagnosis_code          | String                                                  |
| secondary_diagnosis_qualifier     | String                                                  |
| secondary_diagnosis_description   | String                                                  |
| dea_schedule                      | String                                                  |
| potency_unit_code                 | String                                                  |
| etc_path_id                       | Array[Integer]                                          |
| etc_path_name                     | Array[String]                                           |
| fill_number                       | Integer                                                 |
| prescriber_order_number           | String                                                  |
| source_description                | String                                                  |
| source_qualifier                  | String                                                  |
| source_payer_id                   | String                                                  |
| source_type                       | String                                                  |
| note                              | String                                                  |
| sig                               | String                                                  |
| prior_authorization_status        | String                                                  |
| prior_authorization               | String                                                  |
| pharmacy_name                     | String                                                  |
| pharmacy_ncpdp_id                 | String                                                  |
| pharmacy_npi                      | String                                                  |
| prescriber_business_name          | String                                                  |
| prescriber_first_name             | String                                                  |
| prescriber_last_name              | String                                                  |
| prescriber_npi                    | String                                                  |
| prescriber_dea_number             | String                                                  |
| codings                           | [MedicationHistoryMedicationCoding](#medicationhistorymedicationcoding)[] |

### MedicationHistoryMedicationCoding

| Field Name    | Type                                                      |
| ------------- | --------------------------------------------------------- |
| dbid          | Integer                                                   |
| system        | String                                                    |
| version       | String                                                    |
| code          | String                                                    |
| display       | String                                                    |
| user_selected | Boolean                                                   |
| medication    | [MedicationHistoryMedication](#medicationhistorymedication) |

### MedicationHistoryResponse

| Field Name             | Type                                                          |
| ---------------------- | ------------------------------------------------------------- |
| id                     | UUID                                                          |
| dbid                   | Integer                                                       |
| created                | DateTime                                                      |
| modified               | DateTime                                                      |
| patient                | [Patient](/sdk/data-patient/#patient)                        |
| staff                  | [Staff](/sdk/data-staff/#staff)                              |
| message_id             | String                                                        |
| related_to_message_id  | String                                                        |
| status                 | [MedicationHistoryResponseStatus](#medicationhistoryresponsestatus) |
| reason                 | String                                                        |
| reason_code            | String                                                        |
| note                   | String                                                        |
| start_date             | Date                                                          |
| end_date               | Date                                                          |

## Enumeration types

### MedicationHistoryResponseStatus

| Value    | Label    |
| -------- | -------- |
| approved | approved |
| denied   | denied   |

<br/>
<br/>
<br/>