---
title: "Data Integration"
slug: "effect-data-integration"
excerpt: "Manage documents in the Data Integration queue."
hidden: false
---

The Canvas SDK allows you to manage documents in the Data Integration queue.

## Assigning a Document Reviewer

To assign a staff member or team as a reviewer to a document in the Data Integration queue, import the `AssignDocumentReviewer` class and create an instance of it.

| Attribute       |          | Type                        | Description                                                                                                        |
|-----------------|----------|-----------------------------|--------------------------------------------------------------------------------------------------------------------|
| document_id     | required | string                      | The ID of the IntegrationTask document to assign a reviewer to.                                                    |
| reviewer_id     | optional | string                      | The Staff key of the reviewer to assign.                                                                           |
| team_id         | optional | string                      | The Team UUID to assign.                                                                                           |
| priority        | optional | [Priority](#priority)       | Priority level for the review. Defaults to `NORMAL`.                                                               |
| review_mode     | optional | [ReviewMode](#reviewmode)   | Review mode for the document. Defaults to `REVIEW_REQUIRED`.                                                       |
| annotations     | optional | list                        | List of annotations for display in the UI. See [Annotations](#annotations).                                        |
| source_protocol | optional | string                      | Identifier for the protocol/plugin that generated this effect. Used for tracking and debugging.                    |

### Priority

| Value  | Description                                    |
|--------|------------------------------------------------|
| NORMAL | Standard priority (default).                   |
| HIGH   | Elevated priority for time-sensitive documents.|

### ReviewMode

| Value               | Description                                          |
|---------------------|------------------------------------------------------|
| REVIEW_REQUIRED     | Document requires active review and action (default).|
| ALREADY_REVIEWED    | Document was already reviewed offline.               |
| REVIEW_NOT_REQUIRED | Document does not require review.                    |

### Annotations

The `annotations` parameter accepts a list of dictionaries with the following keys:

| Key   | Type   | Description                                           |
|-------|--------|-------------------------------------------------------|
| text  | string | The annotation text to display (e.g., "AI 95%").      |
| color | string | Hex color code (e.g., "#4CAF50" for green).         |

An example of assigning a staff reviewer:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import AssignDocumentReviewer, Priority, ReviewMode
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.v1.data.staff import Staff


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        document_id = self.event.context.get("document", {}).get("id")
        reviewer = Staff.objects.get(last_name="Smith")

        assign_reviewer = AssignDocumentReviewer(
            document_id=document_id,
            reviewer_id=reviewer.id,
            priority=Priority.NORMAL,
            review_mode=ReviewMode.REVIEW_REQUIRED,
        )

        return [assign_reviewer.apply()]
```

An example of assigning a team reviewer:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.data_integration import AssignDocumentReviewer, Priority
from canvas_sdk.events import EventType
from canvas_sdk.protocols import BaseProtocol

from canvas_sdk.v1.data.team import Team


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.DOCUMENT_RECEIVED)

    def compute(self) -> list[Effect]:
        document_id = self.event.context.get("document", {}).get("id")
        team = Team.objects.get(name="Document Review")

        assign_reviewer = AssignDocumentReviewer(
            document_id=document_id,
            team_id=team.id,
            priority=Priority.HIGH,
        )

        return [assign_reviewer.apply()]
```

You can assign both a staff member and a team to the same document, and include annotations:

```python
from canvas_sdk.effects.data_integration import (
    AssignDocumentReviewer,
    Priority,
    ReviewMode,
)

assign_reviewer = AssignDocumentReviewer(
    document_id="d2194110-5c9a-4842-8733-ef09ea5ead11",
    reviewer_id="staff-key-here",
    team_id="team-uuid-here",
    priority=Priority.HIGH,
    review_mode=ReviewMode.REVIEW_REQUIRED,
    annotations=[
        {"text": "Team lead", "color": "#4CAF50"},
        {"text": "Auto-assigned", "color": "#FF9800"},
    ],
    source_protocol="my_plugin",
)
```

<br/>
<br/>
<br/>
