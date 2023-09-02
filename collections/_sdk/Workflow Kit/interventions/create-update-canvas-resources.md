---
title: "Create or Update Resources from a Protocol"
---
The Workflow Kit allows the ability to create or update specific resources in Canvas. Instead of posting a network request to your Canvas instance's API endpoint, there's a shortcut where you can ask your protocol to do it for you when it computes! 

Within the `compute_results` function you can call the method `self.set_updates([payload])` which accepts a single parameter -  a list of dictionaries that conform to a specific schema, where each dictionary is a resource creation or update. Every time the protocol is computed, these updates will be saved directly to your instance's database. 

These JSON messages can be processed by the Canvas message bus, but the message itself needs to be constructed by calling a helper function.  Currently, these are limited but let us know what data you'd like to create/update via protocols and we can see about adding them!

## Patient Group

To add or remove a patient from a Group in Canvas, we have made two helper functions that you can pass to the `set_updates` function. Both groups require the patient's key and the group's UUID. The group UUID can be found using a [Group Search](ref:group-search-intern). 

**ensure_patient_in_group(patient_key: str, group_externally_exposable_id: str)**
    - Creates a message to add a patient to a patient group if they are not already in that group.
**ensure_patient_not_in_group(patient_key: str, group_externally_exposable_id: str)**
    - Creates a message that removes a patient from a patient group if they are currently in the group.

Here is an oversimplified example of how to use these in a protocol:
```python
from canvas_workflow_kit.internal.integration_messages import (
    ensure_patient_in_group,
    ensure_patient_not_in_group
)
from canvas_workflow_kit.protocol import ClinicalQualityMeasure    

class XYZPatientGroupUpdate(ClinicalQualityMeasure):
  
  patient_key = self.patient.patient['key']
  # replace with the uuid for your patient group
  patient_group_uuid = '00000000-0000-0000-0000-000000000000'
  
  self.set_updates([ensure_patient_in_group(patient_key, patient_group_uuid)])
```
## Task Create 

To create a Task associated with a patient in a Canvas protocol, we made a helper function called **create_task_payload** and it will take the following arguments:

- `patient_key` is a required argument that represents the patient's unique identifier. You can get this in the sdk with `self.patient.patient['key']`
- `created_by_key` is a required argument that represents the practitioner's unique identifier. 
- `status` is an optional argument for what the status of the task will be when created. The status can be "COMPLETED", "CLOSED", or  "OPEN"  If this isn't supplied it will default to "OPEN". 
- `title` is an optional string for the title/summary of the task
- `assignee_identifier` is an optional staff unique identifier if the task is to be assigned to a specific practitioner
- `team_identifier` is an optional team unique identifier if the task is to be assigned to a team. You can get this identifier by using the FHIR [Group Search](ref:group-search) endpoint. 
- `due` is on optional datetime string that much match the iso date format (YYYY-MM-DDThh:mm:ss)
- `created` is on optional datetime string that much match the iso date format (YYYY-MM-DDThh:mm:ss)
- `labels` is an optional list of strings that represent any Task Labels in your instance you want to associate with the Task. If you supply a label that does not currently exist, the label will be created. 

To see this function used here is an [example](https://github.com/canvas-medical/open-source-sdk/blob/main/canvas_workflow_helpers/protocols/appointment_task_creator.py) of creating a task when an appointment is created