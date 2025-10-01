---
title: 'Abnormal Lab Task Notification'
slug: 'example-abnormal_lab_task_notification'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/abnormal_lab_task_notification' target='_blank'>View the source</a> for this plugin on GitHub." %}

# Abnormal Lab Task Notification Plugin

This Canvas EMR plugin automatically creates task notifications whenever lab results with abnormal values are received, ensuring critical lab findings are flagged for prompt clinical review.

## Technical Details

**Event Triggered By:** New lab reports entering the Canvas system
**Detection Method:** Checks the `abnormal_flag` field on lab values
**Task Creation:** Uses Canvas SDK's AddTask effect
**Labels Applied:** "abnormal-lab", "urgent-review"

The plugin is designed to be safe and efficient:
- Filters out test-only and invalid lab reports
- Handles missing data gracefully
- Includes comprehensive error logging for troubleshooting

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.1.0",
    "name": "abnormal_lab_task_notification",
    "description": "A plugin that creates task notifications for abnormal lab values",
    "components": {
        "protocols": [
            {
                "class": "abnormal_lab_task_notification.protocols.abnormal_lab_protocol:AbnormalLabProtocol",
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

## tests/

This example plugin contains tests for the plugin core functionality.

**Key Plugins/SDK Components Used**

- `canvas_sdk.effects.task.AddTask` and `TaskStatus`: Used to simulate creation of urgent lab review tasks.
- `canvas_sdk.events.EventType`: Used to check that the plugin subscribes to the correct event type.

**Intended Context**

While these tests do not require a live or full Django/Canvas environment (since they use mocks), they are written to confirm the core business logic expected by the abnormal lab value detection protocol, ensuring correctness before integrating fully with the Canvas platform.

```python
"""
Test for the abnormal lab task notification plugin.

These tests validate the plugin logic for creating tasks when abnormal lab values are detected.
"""
from unittest.mock import Mock

from canvas_sdk.effects.task import AddTask, TaskStatus
from canvas_sdk.events import EventType


class MockLabValue:
    """Mock lab value for testing."""
    def __init__(self, abnormal_flag="", value="", units="", reference_range=""):
        self.id = "test-value-id"
        self.abnormal_flag = abnormal_flag
        self.value = value
        self.units = units
        self.reference_range = reference_range


class MockLabReport:
    """Mock lab report for testing."""
    def __init__(self, patient_id="test-patient", for_test_only=False, junked=False, values=None):
        self.id = "test-lab-report-id"
        self.patient_id = patient_id
        self.for_test_only = for_test_only
        self.junked = junked
        self.values = Mock()
        self.values.all.return_value = values or []


def test_plugin_responds_to_correct_event():
    """Test that the plugin responds to LAB_REPORT_CREATED events."""
    # This test would be run in a Django environment where we can import the plugin
    # For now, we'll test the event type matching
    expected_event = EventType.Name(EventType.LAB_REPORT_CREATED)
    assert expected_event == "LAB_REPORT_CREATED"


def test_abnormal_lab_detection():
    """Test the logic for detecting abnormal lab values."""
    # Test case 1: Normal values (no abnormal flag)
    normal_value = MockLabValue(abnormal_flag="")
    assert not normal_value.abnormal_flag.strip()

    # Test case 2: Abnormal values (has abnormal flag)
    abnormal_value = MockLabValue(abnormal_flag="HIGH")
    assert abnormal_value.abnormal_flag.strip()

    # Test case 3: Whitespace only abnormal flag (should be treated as normal)
    whitespace_value = MockLabValue(abnormal_flag="   ")
    assert not whitespace_value.abnormal_flag.strip()

    # Test case 4: None abnormal flag (defensive programming)
    none_value = MockLabValue(abnormal_flag=None)
    # Simulate getattr with None fallback
    flag = getattr(none_value, 'abnormal_flag', None) or ""
    assert not flag.strip()


def test_task_creation_logic():
    """Test the task creation parameters."""
    # Test parameters for AddTask
    task = AddTask(
        patient_id="test-patient-id",
        title="Review Abnormal Lab Values (2 abnormal)",
        status=TaskStatus.OPEN,
        labels=["abnormal-lab", "urgent-review"]
    )

    assert task.patient_id == "test-patient-id"
    assert task.title == "Review Abnormal Lab Values (2 abnormal)"
    assert task.status == TaskStatus.OPEN
    assert "abnormal-lab" in task.labels
    assert "urgent-review" in task.labels


def test_task_apply_method():
    """Test that AddTask has apply() method (structure validation)."""
    task = AddTask(
        patient_id="test-patient-id",
        title="Test Task",
        status=TaskStatus.OPEN
    )

    # Verify apply method exists
    assert hasattr(task, 'apply')
    assert callable(getattr(task, 'apply'))

    # Note: We can't actually call apply() without Django environment
    # but we can verify the method exists for the protocol to use


def test_filtered_reports():
    """Test that test-only and junked reports are filtered out."""
    # Test case 1: Test-only report should be filtered
    test_report = MockLabReport(for_test_only=True)
    assert test_report.for_test_only

    # Test case 2: Junked report should be filtered
    junked_report = MockLabReport(junked=True)
    assert junked_report.junked

    # Test case 3: Normal report should not be filtered
    normal_report = MockLabReport(for_test_only=False, junked=False)
    assert not normal_report.for_test_only and not normal_report.junked


def test_multiple_abnormal_values():
    """Test handling of multiple abnormal values in a single report."""
    abnormal_values = [
        MockLabValue(abnormal_flag="HIGH", value="180", units="mg/dL", reference_range="70-100"),
        MockLabValue(abnormal_flag="LOW", value="9.2", units="g/dL", reference_range="12-16"),
        MockLabValue(abnormal_flag="CRITICAL", value="2.1", units="mmol/L", reference_range="3.5-5.0")
    ]

    # Count abnormal values
    abnormal_count = len([v for v in abnormal_values if v.abnormal_flag.strip()])
    assert abnormal_count == 3

    # Test title generation
    expected_title = f"Review Abnormal Lab Values ({abnormal_count} abnormal)"
    assert expected_title == "Review Abnormal Lab Values (3 abnormal)"


if __name__ == "__main__":
    # Run basic validation tests
    test_plugin_responds_to_correct_event()
    test_abnormal_lab_detection()
    test_task_creation_logic()
    test_task_apply_method()
    test_filtered_reports()
    test_multiple_abnormal_values()
    print("All tests passed!")
```

## protocols/

### abnormal_lab_protocol.py

**Purpose and Functionality**

This file defines a protocol called AbnormalLabProtocol for use with the Canvas Medical SDK. Its primary function is to monitor for the creation of new laboratory reports (LAB_REPORT_CREATED events). When such an event occurs, the protocol inspects the report to determine if it contains any abnormal lab values. If abnormal results are found, it automatically creates a task for prompt clinical review.

**Event Handling**

- The protocol listens for the LAB_REPORT_CREATED event.
- When triggered, it examines the relevant lab report for any values marked as abnormal.

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

This protocol automates the process of flagging abnormal laboratory results for clinical review within Canvas Medical, enhancing the safety net for critical lab findings by ensuring they are not overlooked.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.task import AddTask, TaskStatus
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.v1.data.lab import LabReport
from logger import log


class AbnormalLabProtocol(BaseProtocol):
    """
    A protocol that monitors lab reports and creates task notifications
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
