---
permalink: /product-updates/note-revamp/
title: "Beta | Revamped Note"
layout: betas
---

{% include alert.html type="warning" content="<b>Beta Participation:</b> The revamped note is in beta and is turned on per instance. Reach out to Canvas support if you would like to participate." %}

## Overview

The revamped note is a redesigned note body that organizes commands into clinical sections and lets providers arrange the Assessment & Plan the way they think about it, with each order, prescription and plan sitting under the condition it treats. Notes keep all of their existing commands and data; the beta changes how the note is laid out, organized and printed.

## Expected Benefits

**Clinical sections:** The note body is grouped into History, Exam, Assessment & Plan and Internal sections, ordered to match the note's SOAP or APSO format. Each section has its own prompt for adding commands, and a **Sections / All** toggle in the note header switches between the sectioned view and the whole note.

**Commands nested under their Assessment:** Plan and Procedure commands, along with Prescribe, Refill, Adjust Prescription, Change Medication, Lab Order, Imaging Order, Refer and Educational Material, appear nested under the Assess Condition command they are linked to.
- Drag a command onto an Assessment to link it, or drag it out to unlink it.
- Linking a prescription or order adds the assessed condition to its Indications.
- Changes show up live for everyone who has the note open.

**Grouped Assessment & Plan when printed:** A printed note in the revamped format shows one Assessment & Plan section in place of separate Assessment, Procedures and Plan headings. The commands keep the order the provider gave them in the note, and each Assess Condition command prints with its linked commands indented beneath it. Faxed notes, the copy saved when a note is locked, and the patient's entire-record print use the same layout.

**Collapsible commands:** Commands that haven't been committed yet can be collapsed to keep a long note readable, and they stay collapsed when you come back to the note.

**Easier drag and drop:** Commands are picked up by a grip in the left gutter, so clicks inside a command's fields always go to the fields.

## For developers

Plugins can link commands to an Assessment in the same note with `assessment_id`, and read the link back from each data model's `assessment` field. See [Commands linked to an assessment](/sdk/data-assessment/#commands-linked-to-an-assessment) and the [commands module](/sdk/commands/). Links are recorded on every instance; the nested display and grouped print are what the beta adds.

Plugins can also add their own content to the revamped note. Respond to the [`NOTE__GET_CUSTOM_CONTENT`](/sdk/events/#note-custom-content) event with one or more `NoteCustomContent` effects (`canvas_sdk.effects.note_custom_content`), each giving either `content` (HTML) or a `url`, not both. See the [Note Custom Content effect](/sdk/effect-note-custom-content/) for every attribute, URL block permissions, keeping content current, and more examples.
- `section` places the content at the top of a section: `NoteCustomContent.Section.HISTORY`, `EXAM`, `ASSESSMENT_PLAN` or `INTERNAL`, and shows only in the **Sections** view. Leave it unset to place the content above the note body, where it shows in both the **Sections** and **All** views.
- Content returned for the same section stacks in the order the handlers ran.
- Each entry renders in its own frame, which starts 120 pixels tall. To fit the frame to the content, send a `RESIZE` message with the content's height over the frame's message channel, as shown in [Frame height](/sdk/effect-note-custom-content/#frame-height).
- Outside the beta, Canvas doesn't send the event, so the content doesn't appear.

```python
from canvas_sdk.effects.note_custom_content import NoteCustomContent
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class NoteBanner(BaseHandler):
    RESPONDS_TO = [EventType.Name(EventType.NOTE__GET_CUSTOM_CONTENT)]

    def compute(self):
        return [
            NoteCustomContent(
                section=NoteCustomContent.Section.ASSESSMENT_PLAN,
                content="<p>Remember to link each order to its assessment.</p>",
            ).apply()
        ]
```
