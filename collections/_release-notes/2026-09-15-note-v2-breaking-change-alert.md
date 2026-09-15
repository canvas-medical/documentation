---
slug: note-v2-breaking-change-2026-09-15
title: Upcoming Breaking Change - Clinical Note Body Structure
date: 2026-09-15 08:00:00
layout: productupdates
tags: breaking-change
feed_summary: |
  Canvas is changing how a clinical note stores its body, enabled per instance.

  Charting, the Note API, and FHIR are unchanged. Three changes affect plugins that read note content:

  • body cannot be selected with values() or values_list().
  • body cannot be named through a relation.
  • Note.checksum is no longer maintained.
---

Canvas is changing how a clinical note stores its body. Each line of a note becomes an addressable object with its own identity, in place of the single block of content that holds the whole note today.

This is enabled one instance at a time rather than as a single cutover. Every note records which structure it uses, both structures work side by side on the same chart, and Canvas coordinates with your team before enabling it on your instance. Notes written before it is enabled keep working as they are.

## What this changes for clinicians

Nothing in the charting workflow. Commands, signing, locking, printing, and the note's appearance behave as they do today. Alongside that, the new structure brings:

- Two clinicians, or two browser tabs, can work in the same note at the same time. Edits to different lines merge, instead of one person's work being refused because someone else touched the note.
- A command that is originated always lands in the note, or is rolled back completely.
- Changes made elsewhere in Canvas appear in an open note without a reload.
- A note stops refetching itself after every interaction, so a long note stays responsive as it grows.

## What this does not change

- The [Note API](/api/note/) payload, in shape or content. This API does not expose the note body.
- FHIR resources.
- Note content as it prints or renders.

## Breaking changes for plugin and integration developers

Three changes affect code that reads note content through the [Note data model](/sdk/data-note/). Two are already live for every instance. One takes effect on an instance when the new structure is enabled there.

Reading a note body is not one of them. `note.body` returns the same lines in the same order on both structures, and a command line still carries its `command_uuid`, so code that walks a body to resolve its commands keeps working. The one thing not to rely on there is `data["id"]`, the integer identifier of the record a command created: read the [Command](/sdk/data-command/) through `command_uuid` and take `anchor_object` from it instead.

### Live as of the September 8, 2026 release

**`body` cannot be selected with `values()` or `values_list()`.** Canvas assembles `body` from more than one column, so no single column holds a value to return. Naming it raises a `FieldError`. Load the note and read the property instead:

```python?partial=true
# Selecting body as a value raises a FieldError.
Note.objects.filter(dbid__in=note_ids).values_list("dbid", "body")

# Load the columns the body needs, then read it.
for note in Note.objects.only("dbid", "body").filter(dbid__in=note_ids):
    note_dbid, body = note.dbid, note.body
```

**`body` cannot be named through a relation.** A queryset on another model that defers or filters `note__body` raises an error. Query `Note` directly for the notes you need, and defer `body` there:

```python?partial=true
# Naming body through a relation raises an error.
Appointment.objects.defer("note__body")

# Query Note itself.
Note.objects.defer("body").filter(patient__id=patient_id)
```

`filter()`, `exclude()`, `get()`, `only()`, and `defer()` all continue to accept `body` on a `Note` queryset. See [Querying on the body](/sdk/data-note/#querying-on-the-body) for the full list of supported operations.

### When the new structure is enabled on your instance

**`Note.checksum` is no longer maintained.** The new structure controls concurrency per line rather than across the whole note, so it computes no checksum. The `checksum` attribute is still present and still readable, and its value no longer changes when the note changes. To detect that a note has been modified, read its `modified` timestamp.

## Action required

Review your plugins for these patterns:

- `values("body")` and `values_list(..., "body")`
- `body` named through a relation, such as `note__body`
- `Note.checksum`

Code that filters on `body`, or reads a note's commands through `note.commands`, needs no change.

If you would like Canvas to review your plugins for these patterns before the new structure is enabled on your instance, contact your Canvas team.

Keep track of upcoming breaking changes [here.](/product-updates/important-dates/)
