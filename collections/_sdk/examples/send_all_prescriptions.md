---
title: 'Send All Prescriptions'
slug: 'example-send_all_prescriptions'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/send_all_prescriptions' target='_blank'>View the source</a> for this plugin on GitHub." %}

A Canvas plugin that adds a "Send Prescriptions" button to note footers, allowing healthcare providers to send all committed prescriptions in a note with a single click.

## SDK Features
* Creates an [ActionButton](/sdk/handlers-action-buttons/) that uses the [Note](/sdk/data-note/) context to get all committed prescribe [Commands](/sdk/data-command/) in a Note
* Returns a list of [PrescribeCommand](sdk/commands/#prescribe) effects with [`send`](/sdk/commands/#send) action request

## Structure

```
send_all_prescriptions/
├── CANVAS_MANIFEST.json          # Plugin configuration
├── README.md                     # Documentation
├── handlers/
│   └── handler.py                # Defines SendPrescriptionButtonHandler class
```

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "1.0.0",
    "name": "send_all_prescriptions",
    "description": "Adds a 'Send Prescriptions' button to note footers that allows providers to send all committed prescriptions in a note with a single click, streamlining the prescription workflow.",
    "components": {
        "protocols": [
            {
                "class": "send_all_prescriptions.handlers.handler:SendPrescriptionButtonHandler",
                "description": "Action button that sends all committed prescriptions in the current note.",
                "data_access": {
                    "event": "",
                    "read": [],
                    "write": []
                }
            }
        ],
        "commands": [],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [],
    "tags": {},
    "references": ["https://docs.canvasmedical.com/sdk/handlers-action-buttons/", "https://docs.canvasmedical.com/sdk/commands/#prescribe"],
    "license": "",
    "diagram": false,
    "readme": "./README.md"
}
```

## handlers/

### handler.py

This file defines a custom button handler. It provides functionality to send all prescription commands associated with a specific note when the button is activated.

- The main class, `SendPrescriptionButtonHandler`, inherits from `ActionButton` and represents a custom action button shown in the UI (specifically, at the note footer).
- The button is labeled "Send Prescriptions" and assigned a unique key "SEND_ALL_PRESCRIPTIONS".

**Button Handling Logic**

- The `handle` method is the core logic, executed when the user clicks the button.
- It obtains the `note_id` from the plugin execution context (self.context).
- It queries the database for all commands of type `"prescribe"` that are committed (i.e., have an associated committer) and belong to the given note.
- For each qualifying command, it creates a `PrescribeCommand`, sets its UUID to match the command, and calls `send()`, which returns an `Effect`.
- All created effects are collected into a list and returned; these effects trigger the actual process of sending prescriptions.

```python
from canvas_sdk.commands import PrescribeCommand
from canvas_sdk.effects import Effect
from canvas_sdk.handlers.action_button import ActionButton
from canvas_sdk.v1.data import Command


class SendPrescriptionButtonHandler(ActionButton):
    BUTTON_TITLE = "Send Prescriptions"
    BUTTON_KEY = "SEND_ALL_PRESCRIPTIONS"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_FOOTER


    def handle(self) -> list[Effect]:
        note_id = self.context.get("note_id")

        effects = []
        # get all committed prescribe commands
        prescribe_commands = Command.objects.filter(note_id=note_id, schema_key="prescribe", committer__isnull=False)

        for command in prescribe_commands:
            prescribe = PrescribeCommand()
            prescribe.command_uuid = str(command.id)
            effects.append(prescribe.send())

        return effects
```
## Customization

### Button Appearance

You can customize the button by modifying the class attributes:

```python
BUTTON_TITLE = "Your Custom Title"    # Change button text
BUTTON_KEY = "YOUR_UNIQUE_KEY"        # Change button identifier
```

### Button Location

Change where the button appears by modifying:

```python
BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_FOOTER  # or other locations
```
<br/>
<br/>
<br/>
