---
title: 'send_all_prescriptions'
slug: 'example-send_all_prescriptions'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/send_all_prescriptions' target='_blank'>View the source</a> for this plugin on GitHub." %}

# Canvas Send Prescriptions Plugin

A Canvas Medical SDK plugin that adds a convenient "Send Prescriptions" button to note footers, allowing healthcare providers to send all committed prescriptions in a note with a single click.

## Overview

This plugin adds an action button in the note footer that enables providers to quickly send all committed prescriptions within a note. Instead of sending prescriptions individually, providers can now send all prescriptions at once, streamlining the prescribing workflow.

## Features

- **Single-Click Prescription Sending**: Send all committed prescriptions in a note with one button click
- **Note Footer Integration**: Conveniently placed button in the note footer for easy access
- **Batch Processing**: Automatically identifies and processes all committed `PrescribeCommand` instances in the current note
- **Simple Workflow**: No configuration required - works immediately after installation

## Prerequisites

- Canvas CLI installed (`pip install canvas`)
- OAuth credentials configured for your Canvas instance

## Installation

1. Clone or download this plugin to your local development environment

2. Install the Canvas CLI if you haven't already:
   ```bash
   pip install canvas
   ```

3. Configure your Canvas CLI with OAuth credentials:
   - Register an OAuth application in your Canvas instance
   - Choose "confidential" for Client type
   - Choose "client-credentials" for Authorization grant type

4. Install the plugin to your Canvas instance:
   ```bash
   canvas install /path/to/send_all_prescriptions
   ```

## How It Works

1. **Button Display**: The plugin adds a "Send Prescriptions" button to the footer of all notes
2. **Command Detection**: When clicked, the button identifies all committed `PrescribeCommand` instances in the current note
3. **Batch Sending**: Iterates through each committed prescription and sends it to the pharmacy
4. **User Feedback**: Provides immediate feedback on the sending process

## Usage

### For Healthcare Providers

1. **Create Prescriptions**: Add prescribe commands to your note as usual
2. **Commit Prescribe Commands**
3. **Send All**: Click the "Send Prescriptions" button in the note footer

### Button Location

The "Send Prescriptions" button appears in the note footer and is only functional when there are committed prescription commands in the note.

## Development

### Project Structure

```
send_all_prescriptions/
├── CANVAS_MANIFEST.json           # Plugin configuration
├── README.md                     # This file
├── protocols/
│   └── my_protocol.py            # Main button handler
```

### Key Components

- **SendPrescriptionButtonHandler**: ActionButton subclass that handles the button click event
- **Button Configuration**: Defines button title, key, and location
- **Command Processing**: Queries and processes committed prescribe commands

### Code Structure

```python
class SendPrescriptionButtonHandler(ActionButton):
    BUTTON_TITLE = "Send Prescriptions"
    BUTTON_KEY = "SEND_ALL_PRESCRIPTIONS"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_FOOTER

    def handle(self) -> list[Effect]:
        # Get note ID from context
        # Query committed prescribe commands
        # Send each prescribe
        # Return effects list
```

## Testing

To test the plugin during development:

1. **Install the plugin** in your Canvas development instance

2. **Create a test note** with prescribe commands

3. **Commit the prescribe command** to make them eligible for sending

4. **Look for the button** in the note footer

5. **Click the button** and verify prescriptions are sent


## Troubleshooting

### Common Issues

1. **Button not appearing**
   - Verify the plugin is installed and enabled
   - Check that you're viewing a note (button only appears in notes)
   - Ensure the ActionButton class is properly imported

2. **Button not working when clicked**
   - Verify there are committed/signed prescribe commands in the note

3. **Some prescriptions not being sent**
   - Only committed/signed and not sent prescriptions are processed


## API Reference

### ActionButton Methods

- `handle()`: Main method called when button is clicked, returns list of Effects
- `BUTTON_TITLE`: Display text for the button
- `BUTTON_KEY`: Unique identifier for the button
- `BUTTON_LOCATION`: Where the button appears (NOTE_FOOTER)

### Canvas SDK Components Used

- `ActionButton`: Base class for creating clickable buttons
- `Command`: ORM model for querying prescription commands
- `PrescribeCommand`: SDK command class for prescribe command
- `Effect`: Return type for Canvas SDK

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

## Changelog

### Version 1.0.0
- Initial release
- Basic "Send Prescriptions" button functionality
- Note footer integration
- Batch prescription sending

## Support

For support with this plugin, please:

1. Check this README and troubleshooting section
2. Review Canvas Medical SDK ActionButton documentation
3. Contact your Canvas Medical administrator
4. Submit issues through the appropriate channels

---

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

### __init__.py

This file is empty.
### handler.py

**Overview**

This file defines a custom button handler for the Canvas Medical platform, which uses the Canvas SDK. It provides functionality to send all prescription commands associated with a specific note when the button is activated.

**Class Definition**

- The main class, `SendPrescriptionButtonHandler`, inherits from `ActionButton` and represents a custom action button shown in the UI (specifically, at the note footer).
- The button is labeled "Send Prescriptions" and assigned a unique key "SEND_ALL_PRESCRIPTIONS".

**Button Handling Logic**

- The `handle` method is the core logic, executed when the user clicks the button.
- It obtains the `note_id` from the plugin execution context (self.context).
- It queries the database for all commands of type `"prescribe"` that are committed (i.e., have an associated committer) and belong to the given note.
- For each qualifying command, it creates a `PrescribeCommand`, sets its UUID to match the command, and calls `send()`, which returns an `Effect`.
- All created effects are collected into a list and returned; these effects trigger the actual process of sending prescriptions.

**Purpose**

- The overall purpose of this handler is to provide a single-click method for a user to send all pending/committed prescriptions related to a specific note in the Canvas Medical system. This automates the transmission of prescriptions for a patient's encounter or documentation.

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

<br/>
<br/>
<br/>
