---
title: 'Abnormal Lab Task Notification'
slug: 'example-abnormal_lab_task_notification'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/abnormal_lab_task_notification' target='_blank'>View the source</a> for this plugin on GitHub." %}

This Canvas EMR plugin automatically creates task notifications whenever lab results with abnormal values are received, ensuring critical lab findings are flagged for prompt clinical review.

## SDK Features

* Responds to `LAB_REPORT_CREATED` [event](/sdk/events/#labs)
* Loads and parses the [Lab Report data model](/sdk/data-labs/#labreport) to identify [lab values](/sdk/data-labs/#labvalue) flagged as abnormal
* Returns a [task effect](/sdk/effect-tasks/#adding-a-task)

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.1.0",
    "name": "abnormal_lab_task_notification",
    "description": "A plugin that creates task notifications for abnormal lab values",
    "components": {
        "handlers": [
            {
                "class": "abnormal_lab_task_notification.handlers.abnormal_lab_handler:AbnormalLabHandler",
                "description": "Monitors lab reports and creates tasks for abnormal values",
                "data_access": {
                    "event": "LAB_REPORT_CREATED",
                    "read": [
                        "lab_reports",
                        "lab_values"
                    ],
                    "write": [
                        "tasks"
                    ]
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "tags": ["lab", "notifications", "tasks"],
    "secrets": [],
    "license": "NONE",
    "readme": "This plugin monitors incoming lab reports and creates task notifications for any abnormal lab values, ensuring they are flagged for prompt review."
}
```

## handlers/

### abnormal_lab_handler.py

**Purpose and Functionality**

This file defines a handler called AbnormalLabHandler for use with the Canvas Medical SDK. Its primary function is to monitor for the creation of new laboratory reports (`LAB_REPORT_CREATED` events). When such an event occurs, the handler inspects the report to determine if it contains any abnormal lab values. If abnormal results are found, it automatically creates a task for prompt clinical review.

**Event Handling**

- The handler listens for the LAB_REPORT_CREATED event.
- When triggered, it examines the relevant [lab report(/sdk/data-labs/#labreport)] for any values marked as abnormal.

**Core Logic**

- It fetches the full LabReport instance specified by the event.
- It filters out any reports that are for test purposes, junked, or do not belong to a patient.
- It iterates through all values within the lab report.
- For each value, it checks if there is a non-empty abnormal_flag.
- If one or more abnormal values are found, it creates a task for the associated patient.

**Effects Produced**

- Adds a new open task titled "Review Abnormal Lab Values ({count} abnormal)", labeled as "abnormal-lab" and "urgent-review" to the patient's workflow.
- Logs the creation of the task and any errors encountered in the process.

**Error Handling**

- If anything goes wrong (e.g., the report is missing, or there’s a processing error), it logs the error and does not produce any task.

**Summary**

This handler automates the process of flagging abnormal laboratory results for clinical review within Canvas Medical, enhancing the safety net for critical lab findings by ensuring they are not overlooked.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.task import AddTask, TaskStatus
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data.lab import LabReport
from logger import log


class AbnormalLabHandler(BaseHandler):
    """
    A handler that monitors lab reports and creates task notifications
    for abnormal lab values to ensure prompt review.

    Triggers on: LAB_REPORT_CREATED events
    Effects: Creates tasks for abnormal lab values
    """

    RESPONDS_TO = EventType.Name(EventType.LAB_REPORT_CREATED)

    def compute(self) -> list[Effect]:
        """
        This method gets called when a LAB_REPORT_CREATED event is fired.
        It checks for abnormal lab values and creates tasks for them.
        """
        # Get the lab report ID from the event target
        lab_report_id = self.event.target.id

        try:
            # Get the lab report instance with filters applied
            lab_report = LabReport.objects.filter(
                id=lab_report_id,
                for_test_only=False,
                junked=False,
                patient__isnull=False
            ).first()

            if not lab_report:
                return []

            patient_id = lab_report.patient.id

            # Check all lab values for abnormal flags
            abnormal_values = []
            for lab_value in lab_report.values.all():
                # Check if the lab value has an abnormal flag (handle None case)
                abnormal_flag = getattr(lab_value, 'abnormal_flag', None) or ""
                if abnormal_flag.strip():
                    abnormal_values.append(lab_value)

            if not abnormal_values:
                return []

            # Create a task for the abnormal lab values
            abnormal_count = len(abnormal_values)
            task_title = f"Review Abnormal Lab Values ({abnormal_count} abnormal)"

            # Create the task
            task = AddTask(
                patient_id=patient_id,
                title=task_title,
                status=TaskStatus.OPEN,
                labels=["abnormal-lab", "urgent-review"]
            )

            applied_task = task.apply()
            log.info(f"Created task for {abnormal_count} abnormal lab value(s) in report {lab_report_id}")
            return [applied_task]

        except Exception as e:
            log.error(f"Error processing lab report {lab_report_id}: {str(e)}")
            return []
```

<br/>
<br/>
<br/>
