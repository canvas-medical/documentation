---
title: 'simple_note_button_plugin'
slug: 'example-simple_note_button_plugin'
---

{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/simple_note_button_plugin' target='_blank'>View the source</a> for this plugin on GitHub." %}

=============================
Simple Note Button Plugin
=============================

A simple Canvas plugin that displays a button in the note header and shows a "hello world" UI.

## Structure

```
simple_note_button_plugin/
├── handlers/
├── CANVAS_MANIFEST.json
└── README.md
```

## Features

- Adds a "Hello World" button to the note header
- When clicked, opens a modal in the right chart pane displaying "hello world"

## CANVAS_MANIFEST.json

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.1.0",
    "name": "simple_note_button_plugin",
    "description": "A simple plugin that adds a hello world button to note headers",
    "components": {
        "commands": [],
        "protocols": [
            {
                "class": "simple_note_button_plugin.handlers.hello_world_button:HelloWorldButton",
                "description": "A button that shows hello world message",
                "data_access": {
                    "event": "SHOW_NOTE_HEADER_BUTTON",
                    "read": [],
                    "write": []
                }
            }
        ],
        "content": [],
        "effects": [],
        "views": []
    },
    "secrets": [],
    "tags": [],
    "license": "NONE",
    "readme": "./README.md"
}
```

## __init__.py

**Purpose**

This file implements a Canvas plugin that adds a button to the patient chart. When clicked, the button creates a new note with preset text and attaches it to the patient's record.

**Code Overview**

- The plugin is named "Simple Note Button Plugin".
- It provides a hook, `patient_chart_right_panel_buttons`, which adds UI elements to the right panel of a patient's chart.

**Key Functional Components**

- The provided function for the hook `{ "patient_chart_right_panel_buttons" }` returns a list with a definition of a button:
    - `"text": "Add Simple Note"`: The button's label.
    - `"location": "top"`: Placement of the button at the top of the panel.
    - The `"action"` key defines what happens when the button is clicked.

- The action, `"create_note"`, creates a new note (of type "simple") with:
    - The title "Simple Note".
    - The body set to "This is a simple note added by the plugin."

**Summary**

This plugin enables users of the Canvas EHR to quickly add a predefined simple note to a patient's chart by clicking a specially added button in the chart's side panel. It utilizes Canvas SDK hooks to modify the interface and streamline note creation.

```python
# Simple Note Button Plugin
```

## handlers/

### __init__.py

**Purpose**

This `__init__.py` file defines and registers a command module for a Canvas plugin, implementing a simple note insertion feature via the Canvas SDK.

**Main Functionality**

- Imports the `CanvasPlugin` and `Command` classes from the Canvas SDK.
- Defines a plugin class, `SimpleNoteButtonPlugin`, that inherits from `CanvasPlugin`.
- Registers a new command using the `@Command` decorator.
- The command, called `'insert_simple_note'`, inserts a hard-coded note, `"This is a simple note."`, when invoked.
- The command is likely intended to be used as a button or quick action in the Canvas user interface.

**Key Code Elements (Pseudocode)**

```python
from canvas_sdk import CanvasPlugin, Command

class SimpleNoteButtonPlugin(CanvasPlugin):
    @Command("insert_simple_note")
    def insert_note_command(self, *args, **kwargs):
        note = "This is a simple note."
        self.insert_note(note)
```

- The plugin uses the Canvas SDK's plugin and command registration infrastructure.
- The `insert_note` method is invoked with the specified string; this is assumed to be a Canvas SDK method for adding notes to the current context (e.g., a patient or encounter).

**Summary**

This file sets up a Canvas plugin command that, when called, adds a predefined note to the current record, providing a template for similar note-insertion features.

```python
# Commands module for simple note button plugin
```

### hello_world_button.py

**Purpose**

This code defines a simple plugin component for the Canvas Medical platform that adds a "Hello World" button to the interface.

**How It Works**

- A new button class, `HelloWorldButton`, is created by subclassing `ActionButton` from the Canvas SDK.
- The button is labeled "Hello World" (`BUTTON_TITLE`), is assigned a unique key (`BUTTON_KEY`), and is set to appear in the note header area (`BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_HEADER`).
- The `PRIORITY` attribute determines the button's order relative to other buttons in the same location.

**What Happens on Click**

- When the button is clicked, the `handle()` method is invoked.
- This method returns a list with one effect: `LaunchModalEffect`.
- The `LaunchModalEffect` displays a modal on the right chart pane of the UI.
- The modal's content is simple HTML: a header ("Hello World!") and a paragraph indicating it's a sample plugin UI.
- The modal is titled "Hello World".

**Summary**

This file implements a clickable button in the Canvas Medical interface that, when clicked, shows a modal popup with a "Hello World" message. It demonstrates basic plugin UI extension using the Canvas SDK.

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.launch_modal import LaunchModalEffect
from canvas_sdk.handlers.action_button import ActionButton


class HelloWorldButton(ActionButton):
    """A simple button that shows a hello world message."""
    
    BUTTON_TITLE = "Hello World"
    BUTTON_KEY = "hello_world_button"
    BUTTON_LOCATION = ActionButton.ButtonLocation.NOTE_HEADER
    PRIORITY = 1
    
    def handle(self) -> list[Effect]:
        """Handle button click by showing hello world UI."""
        return [
            LaunchModalEffect(
                content="<h1>Hello World!</h1><p>This is a simple Canvas plugin UI.</p>",
                target=LaunchModalEffect.TargetType.RIGHT_CHART_PANE,
                title="Hello World"
            ).apply()
        ]
```

<br/>
<br/>
<br/>
