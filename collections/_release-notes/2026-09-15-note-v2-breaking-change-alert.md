---
slug: note-v2-2026-09-15
title: Upcoming Change - Clinical Note Body Structure
date: 2026-09-15 08:00:00
layout: productupdates
tags: breaking-change
feed_summary: |
  Canvas is changing how a clinical note stores its body, enabled per instance.

  Charting, the Note API and FHIR are unchanged, and the plugin SDK changes shipped earlier. The breaking change is for integrations reading a note body from the read-only replica: on a refactored note the body column is empty and the lines move to body_content and body_order.
---

Canvas is changing how a clinical note stores its body. Each line of a note becomes an addressable object with its own identity, in place of the single block of content that holds the whole note today.

## What it changes in the chart

- Two clinicians, or two browser tabs, can work in the same note at the same time. Edits to different lines merge, instead of one person's work being refused because someone else touched the note.
- A command that is originated always lands in the note, or is rolled back completely.
- Changes made elsewhere in Canvas appear in an open note without a reload.
- A note stops refetching itself after every interaction, so a long note stays responsive as it grows.

Commands, signing, locking, printing, and the note's appearance are unchanged.

## How it rolls out

Every note records which structure it uses, so this arrives note by note rather than as a single cutover. The two structures work side by side on the same chart, and Canvas coordinates with your team before enabling the new one on your instance. Notes written beforehand keep working as they are until they are converted.

That means a chart can hold notes of both structures at once, so anything reading note bodies needs to handle both for the duration of the rollout.

## Breaking change: reading a note body from the read-only replica

An integration that reads note bodies from the [read-only replica](/guides/audit-logging-and-telemetry/#read-only-replica-database) needs a query change. This is the one place the structure is visible, because SQL reads the stored columns directly rather than going through the SDK.

On a note using the new structure:

- **`body` is empty.** It is not an error and not a partial read, so a query selecting `body` returns an empty array rather than failing.
- **The lines live in two columns.** `body_content` is an object keyed by line identifier, and `body_order` is an array of those identifiers holding the order.
- **A command line's identifier is its key in `body_content`**, not a field inside the line. This is how you resolve a line to a row in the command table.
- **A line identifier in `body_order` with no `body_content` entry is a blank line.** These are common, because Canvas puts a blank line around each command. Treat a missing entry as empty text rather than dropping the line or reading it as null.
- **`checksum` is empty and stays empty.** The new structure controls concurrency per line rather than across the whole note, so it computes no checksum. To find notes that changed since your last run, use the `modified` timestamp.

This query reads either structure, so it keeps working through the rollout and after it:

```sql
SELECT n.id AS note_id,
       ord.idx AS line_number,
       COALESCE(n.body_content -> ord.line_uuid::text ->> 'type', 'text') AS line_type,
       COALESCE(n.body_content -> ord.line_uuid::text ->> 'value', '')    AS line_value,
       CASE WHEN n.body_content -> ord.line_uuid::text ->> 'type' = 'command'
            THEN ord.line_uuid::text END                                 AS command_uuid
FROM canvas_sdk_data_api_note_001 n
CROSS JOIN LATERAL unnest(n.body_order) WITH ORDINALITY AS ord(line_uuid, idx)
WHERE n.version = 2

UNION ALL

SELECT n.id,
       line.idx,
       line.value ->> 'type',
       COALESCE(line.value ->> 'value', ''),
       line.value -> 'data' ->> 'command_uuid'
FROM canvas_sdk_data_api_note_001 n
CROSS JOIN LATERAL jsonb_array_elements(n.body) WITH ORDINALITY AS line(value, idx)
WHERE n.version IS DISTINCT FROM 2
```

Identifying a command gets more reliable under the new structure, not less. On a legacy note, a command line carries its identifier only if a particular write path happened to record one, so roughly half of them have no identifier in the body at all and can only be matched by position and type. Under the new structure the identifier is the line's key, so every command line has one.

## Plugins and the SDK

Plugin code needs no further change. The queryset changes to the [Note data model](/sdk/data-note/) shipped in the September 8, 2026 release: `body` cannot be selected with `values()` or `values_list()`, and cannot be named through a relation such as `note__body`. Everything else about reading a body through the SDK is unchanged, including a command line's `command_uuid`, so code that walks `note.body` to resolve its commands keeps working on both structures.

One attribute to move off: `Note.checksum` is not maintained under the new structure, for the reason given above. Read the `modified` timestamp instead.

## What is not changing

- The [Note API](/api/note/) payload, in shape or content. This API does not expose the note body.
- FHIR resources.
- Note content as it prints or renders.

Keep track of upcoming changes [here.](/product-updates/important-dates/)
