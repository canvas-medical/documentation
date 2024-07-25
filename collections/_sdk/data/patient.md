---
title: "Patient"
slug: "data-patient"
excerpt: "Canvas SDK Patient"
hidden: false
---

### Fields

| Name         | Type      | Required    | Description                         |
|:-------------|:----------|:------------|:------------------------------------|
| `id`         | _string_  | if updating | The id of the `Patient`.            |
| `first_name` | _string_  | `false`     | The first name of the `Patient`.    |
| `last_name`  | _string_  | `false`     | The last name of the `Patient`.     |
| `birth_date` | _date_    | `false`     | The date of birth of the `Patient`. |

### Methods

#### get

Given a `Patient` id, returns a `Patient` with the data attributes populated. Example:

```python
from canvas_sdk.data.patient import Patient
from canvas_sdk.protocols import BaseProtocol
from logger import log

class Protocol(BaseProtocol):

    RESPONDS_TO = EventType.Name(EventType.PATIENT_CREATED)
  
    def compute(self):
        patient_id = self.target

        patient = Patient.get(patient_id)

        log.info(f"First name: %s", patient.first_name)
        log.info(f"Last name: %s", patient.last_name)
        log.info(f"Birth date: %s", patient.birth_date.isoformat())
```
