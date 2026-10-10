---
title: "Visual Exam Finding"
slug: "commands-visual-exam-finding"
excerpt: "Capture a clinical finding image (title, narrative, photo) inside a note."
hidden: false
---

## Introduction

`VisualExamFindingCommand` originates a Visual Exam Finding command in a note — a photo plus a short title and narrative. It is the **first SDK command that accepts an attached file**: the image is referenced by an S3 key under your plugin's uploads prefix, not uploaded inline.

Useful for ophthalmology, dermatology, wound documentation, and any workflow where a clinician captures an image alongside a note.

## Parameters

| Name                | Type     | Required | Description                                                                                |
|:--------------------|:---------|:---------|:-------------------------------------------------------------------------------------------|
| `note_uuid`         | _string_ | `true`   | The externally exposable id of the note in which to insert the command.                    |
| `command_uuid`      | _string_ | `true` (edit / delete / commit / enter_in_error) | The externally exposable id of an existing command.       |
| `title`             | _string_ | `false`  | Short label for the finding (e.g. "Mole on left arm").                                     |
| `narrative`         | _string_ | `false`  | Free-text description (size, color, location, etc.).                                       |
| `image_upload_key`  | _string_ | `false`  | S3 key under your plugin's uploads prefix (`plugin-uploads/<your-plugin>/...`) — see below. |

## File attachment

`image_upload_key` must live under your plugin's uploads prefix; keys outside that prefix are rejected. The platform performs a server-side S3 copy into the visual-exam-finding storage location when the originate or edit effect is applied — no file bytes pass through your plugin. See the [SimpleAPI HTTP documentation](/sdk/handlers-simple-api-http/) for the `upload_files=True` flag that produces these keys.

## Effect Types

| Method | Effect Type |
|---|---|
| `.originate()` | `ORIGINATE_VISUAL_EXAM_FINDING_COMMAND` |
| `.edit()` | `EDIT_VISUAL_EXAM_FINDING_COMMAND` |
| `.delete()` | `DELETE_VISUAL_EXAM_FINDING_COMMAND` |
| `.commit()` | `COMMIT_VISUAL_EXAM_FINDING_COMMAND` |
| `.enter_in_error()` | `ENTER_IN_ERROR_VISUAL_EXAM_FINDING_COMMAND` |

## Example Usage

### Originate with an image

```python
from canvas_sdk.commands.commands.visual_exam_finding import VisualExamFindingCommand
from canvas_sdk.handlers.base import BaseHandler


class MyHandler(BaseHandler):
    def compute(self):
        command = VisualExamFindingCommand(
            note_uuid="note-uuid-here",
            title="Mole on left arm",
            narrative="3mm diameter, asymmetric border, irregular pigmentation.",
            image_upload_key="plugin-uploads/derm_plugin/abc-photo.jpg",
        )
        return [command.originate()]
```

### Edit to replace the image

```python?partial=True
VisualExamFindingCommand(
    command_uuid="cmd-uuid-here",
    image_upload_key="plugin-uploads/derm_plugin/follow-up-photo.jpg",
).edit()
```

The new image replaces the existing one. `title` / `narrative` are only updated when explicitly set.
