---
slug: note-v2-2026-09-15
title: Upcoming Change - Clinical Note Body Structure
date: 2026-09-15 08:00:00
layout: productupdates
tags: breaking-change
feed_summary: |
  Canvas is changing how a clinical note stores its body. Nothing looks different in the chart. The change is what it made possible, including two people editing one note at the same time.

  The breaking change is for integrations reading a note body from the read-only replica: on a refactored note the body column is empty and the lines move to body_content and body_order.
---

Canvas is changing how a clinical note stores its body. Each line of a note becomes an addressable object with its own identity, in place of the single block of content that holds the whole note today.

Nothing about the note looks or behaves differently. Charting, commands, signing, locking, printing, and the note's appearance are all exactly as they are today. This is a change to the storage underneath, and what matters about it is what it made possible:

- Two clinicians, or two browser tabs, can work in the same note at the same time. Edits to different lines merge, instead of one person's work being refused because someone else touched the note.
- A command that is originated always lands in the note, or is rolled back completely.
- Changes made elsewhere in Canvas appear in an open note without a reload.
- A note stops refetching itself after every interaction, so a long note stays responsive as it grows.

None of those were reachable while the body was a single block, because nothing could refer to one line of it.

## What happens on your instance

Once this is on, new notes use the new structure and your existing notes are migrated onto it, in batches outside business hours so no one is interrupted mid-note. A note looks and behaves the same before and after it migrates.

The end state is that every note on your instance uses the new structure. While the migration runs a chart can hold notes of both, so anything that reads a note body needs to handle both during that window, and the new structure from then on.

## Breaking change: reading a note body from the read-only replica

An integration that reads note bodies from the [read-only replica](/guides/audit-logging-and-telemetry/#read-only-replica-database) needs a query change before its instance is migrated. This is the one place the structure is visible, because SQL reads the stored columns directly rather than going through the SDK.

Both surfaces on the replica carry the change, and they differ by a single column name. If you read `api_note` directly, the legacy body is `_body` there rather than `body`:

| Holds | `api_note` | `canvas_sdk_data_api_note_001` |
|-------|------------|--------------------------------|
| The legacy body | `_body` | `body` |
| The line content | `body_content` | `body_content` |
| The line order | `body_order` | `body_order` |
| Which structure the note uses | `version` | `version` |

`version` is `NULL` on a legacy note and `2` on a migrated one. Select legacy notes with `version IS NULL`: both `version = 1` and `version <> 2` return nothing for them.

On a note using the new structure:

- **`body` is empty.** It is not an error and not a partial read, so a query selecting `body` returns an empty array rather than failing. Once the migration finishes that is every note on the instance, so a query left unchanged returns nothing rather than reporting a problem.
- **The lines live in two columns.** `body_content` is an object keyed by line identifier, and `body_order` is an array of those identifiers holding the order.
- **A command line's identifier is its key in `body_content`**, not a field inside the line. This is how you resolve a line to a row in the command table.
- **A line identifier in `body_order` with no `body_content` entry is a blank line.** These are common, because Canvas puts a blank line around each command. Treat a missing entry as empty text rather than dropping the line or reading it as null.
- **`checksum` is empty and stays empty.** The new structure controls concurrency per line rather than across the whole note, so it computes no checksum. To find notes that changed since your last run, use the `modified` timestamp.

### What the two columns hold

For a note with four lines, `body_order` holds the line identifiers in the order they appear:

```json
[
  "0d5f2c81-4a19-4e77-b3c2-7e1a9f480b6d",
  "5f3b1a90-7c42-4e18-9a6d-2b81cc4f0e77",
  "86da9457-c9d3-429c-9dfb-5b33a12934da",
  "c71e4d38-9b05-42af-8e13-6f9a0d2b5c84"
]
```

`body_content` holds only the lines that have content, keyed by those same identifiers:

```json
{
  "0d5f2c81-4a19-4e77-b3c2-7e1a9f480b6d": {
    "type": "text",
    "value": "Patient reports feeling better"
  },
  "86da9457-c9d3-429c-9dfb-5b33a12934da": {
    "type": "command",
    "value": "diagnose"
  }
}
```

Read together, that is four lines: the text line, a blank line, the Diagnose command, and a second blank line. The two identifiers with no entry in `body_content` are the blank lines, and the Diagnose command's identifier is `86da9457-c9d3-429c-9dfb-5b33a12934da`, the key it is stored under.

Blank lines make up most of a typical note, since Canvas puts one on each side of a command, so expect the majority of `body_order` entries to have no `body_content` of their own.

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

It reads the `canvas_sdk_data_api_note_001` view. To run it against `api_note` instead, change `n.body` to `n._body` in the second half and the table name in both. Everything else is the same on either surface.

Identifying a command gets more consistent under the new structure, not less. On a legacy note a command line carries its identifier only if a particular write path recorded one, so a small number of lines have none and can be matched only by position and type. Under the new structure the identifier is the line's key, so every command line has one.

## Plugins and the SDK

Plugin code needs no further change. The queryset changes to the [Note data model](/sdk/data-note/) shipped in the September 8, 2026 release: `body` cannot be selected with `values()` or `values_list()`, and cannot be named through a relation such as `note__body`. Everything else about reading a body through the SDK is unchanged, including a command line's `command_uuid`, so code that walks `note.body` to resolve its commands keeps working on both structures.

One attribute to move off: `Note.checksum` is not maintained under the new structure, for the reason given above. Read the `modified` timestamp instead.

## What is not changing

- The [Note API](/api/note/) payload, in shape or content. This API does not expose the note body.
- FHIR resources.
- Note content as it prints or renders.

Keep track of upcoming changes [here.](/product-updates/important-dates/)
