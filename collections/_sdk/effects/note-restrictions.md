---
title: "Note Restrictions Effect"
slug: "effect-note-restrictions"
excerpt: "Control access to notes in real time using plugin-driven restriction effects."
hidden: false
---

The `NoteRestrictionsEffect` and `NoteRestrictionsUpdatedEffect` allow plugins to restrict access to notes and push real-time permission updates to connected clients.

- **`NoteRestrictionsEffect`** — returned by a plugin in response to a `GET_NOTE_RESTRICTIONS` event. It tells the Canvas frontend whether the requesting user should see a banner, have the note content blurred, and have editing disabled.
- **`NoteRestrictionsUpdatedEffect`** — emitted by a plugin at any time to signal that restrictions for a specific note have changed, causing all connected clients viewing that note to immediately refetch their restrictions.

---

## NoteRestrictionsEffect

### How it works

Every time a note is opened (or its restrictions are refetched), Canvas fires a `GET_NOTE_RESTRICTIONS` event targeting that note's external ID. Plugins that subscribe to this event can return a `NoteRestrictionsEffect` to control what the user sees.

If no plugin returns a `NoteRestrictionsEffect`, the note is unrestricted by default.

### Event payload

| Property          | Value        | Description                                                                                                                                        |
|-------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `event.target.id` | `str` (UUID) | The `externally_exposable_id` of the note being accessed. Use this to look up the note or its metadata.                                            |
| `event.actor.id`  | `str` (int)  | The database ID of the authenticated user requesting the note. Use `Staff.objects.filter(user__dbid=event.actor.id)` to resolve to a staff record. |
| `event.context`   | `{}`         | Empty — no additional context is provided.                                                                                                         |

### Fields

| Field             | Type            | Default | Description                                                                                            |
|-------------------|-----------------|---------|--------------------------------------------------------------------------------------------------------|
| `restrict_access` | `bool`          | `False` | Whether the requesting user is restricted from editing this note.                                      |
| `blur_content`    | `bool`          | `False` | Whether the note body should be blurred for the requesting user.                                       |
| `banner_message`  | `str` \| `None` | `None`  | Message shown in the warning banner at the top of the note. Falls back to a default message if `None`. |

### Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.restrictions import NoteRestrictionsEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class NoteAccessHandler(BaseHandler):
    """Restrict access to notes based on custom business logic."""

    RESPONDS_TO = EventType.Name(EventType.GET_NOTE_RESTRICTIONS)

    def compute(self) -> list[Effect]:
        note_id = self.event.target.id
        actor_id = self.event.actor.id

        if not self.user_can_access(note_id, actor_id):
            return [
                NoteRestrictionsEffect(
                    restrict_access=True,
                    blur_content=True,
                    banner_message="You do not have permission to view this note.",
                ).apply()
            ]

        return []

    def user_can_access(self, note_id: str, actor_id: str) -> bool:
        # Custom access logic here
        ...
```

---

## NoteRestrictionsUpdatedEffect

### How it works

When a plugin performs an action that changes whether a note is restricted (e.g. writing an edit lock to `NoteMetadata`, updating an access rule), it can emit a `NoteRestrictionsUpdatedEffect`. Canvas will broadcast a WebSocket notification to all clients currently viewing that note, causing them to refetch their restrictions immediately — no page reload required.

### Fields

| Field     | Type  | Description                                         |
|-----------|-------|-----------------------------------------------------|
| `note_id` | `str` | The id of the note whose restrictions have changed. |

### Example

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.note.restrictions import NoteRestrictionsUpdatedEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import NoteMetadata


class NoteAccessChangedHandler(BaseHandler):
    """Broadcast a real-time restriction update after note metadata changes."""

    RESPONDS_TO = EventType.Name(EventType.NOTE_METADATA_UPDATED)

    def compute(self) -> list[Effect]:
        note_id = (
            NoteMetadata.objects
            .filter(id=self.event.target.id)
            .values_list("note__id", flat=True)
            .first()
        )
        if not note_id:
            return []

        return [NoteRestrictionsUpdatedEffect(note_id=str(note_id)).apply()]
```

---

## Common use cases

- **Concurrent edit protection** — prevent multiple providers from editing the same note simultaneously; the second user sees a banner and disabled inputs until the first provider's session expires.
- **Role-based note type access** — restrict certain note types (e.g. sensitive clinical notes) to a specific set of staff members.
- **Sensitive note hiding** — blur the content of notes containing sensitive information for users who should not see the full details.

For full working implementations of these patterns, see the [**note-timeline-restrictions**](https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/note-timeline-restrictions) example plugin, which covers concurrent edit locking, role-based access via a dashboard, automatic lock expiry via a cron job, and real-time updates.

<br/>
<br/>
<br/>
