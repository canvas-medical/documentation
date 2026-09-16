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

Canvas is changing how a clinical note stores its body, from a single block of content to a set of individually addressable lines.

Nothing looks or behaves differently. Charting, commands, signing, locking, printing, and the note's appearance are exactly as they are today. This is a change to the storage underneath, and what matters about it is what it made possible: two clinicians can work in the same note at once with their edits merging, a command that is originated always lands in the note or is rolled back completely, changes made elsewhere appear without a reload, and a long note stays responsive as it grows. None of that was reachable while the body was a single block, because nothing could refer to one line of it.

## What happens on your instance

Once this is on, new notes use the new structure and your existing notes are migrated onto it, in batches outside business hours. A note looks the same before and after it migrates, and the end state is that every note on your instance uses the new structure.

## Breaking change: reading a note body from the read-only replica

An integration that reads note bodies from the [read-only replica](/guides/audit-logging-and-telemetry/#read-only-replica-database) needs a query change before its instance is migrated. This is the one place the structure is visible, because SQL reads the stored columns directly rather than going through the SDK.

A note's `version` is `NULL` before it is migrated and `2` after. On a migrated note the legacy body column is empty, returning an empty array rather than an error, and the lines move to `body_content`, an object keyed by line identifier, and `body_order`, an array of those identifiers in order:

```json
{
  "body_order": [
    "0d5f2c81-4a19-4e77-b3c2-7e1a9f480b6d",
    "5f3b1a90-7c42-4e18-9a6d-2b81cc4f0e77",
    "86da9457-c9d3-429c-9dfb-5b33a12934da",
    "c71e4d38-9b05-42af-8e13-6f9a0d2b5c84"
  ],
  "body_content": {
    "0d5f2c81-4a19-4e77-b3c2-7e1a9f480b6d": { "type": "text", "value": "Patient reports feeling better" },
    "86da9457-c9d3-429c-9dfb-5b33a12934da": { "type": "command", "value": "diagnose" }
  }
}
```

That is four lines: the text, a blank, the Diagnose command, and another blank. An identifier with no `body_content` entry is a blank line, and most lines are blank because Canvas puts one on each side of a command. A command line's identifier is its key, which is how you resolve it to a row in the command table.

This query reads a body in the new structure, one row per line, in order:

```sql
SELECT n.id AS note_id,
       ord.idx AS line_number,
       COALESCE(n.body_content -> ord.line_uuid::text ->> 'type', 'text') AS line_type,
       COALESCE(n.body_content -> ord.line_uuid::text ->> 'value', '')    AS line_value,
       CASE WHEN n.body_content -> ord.line_uuid::text ->> 'type' = 'command'
            THEN ord.line_uuid::text END                                 AS command_uuid
FROM canvas_sdk_data_api_note_001 n
CROSS JOIN LATERAL unnest(n.body_order) WITH ORDINALITY AS ord(line_uuid, idx)
```

The same query runs against `api_note` by changing the table name, since `body_content` and `body_order` are named the same there. On that table the legacy body column is `_body` rather than `body`, and the note identifier is an integer rather than a UUID.

`checksum` is also empty on a migrated note and stays empty, because the new structure controls concurrency per line rather than across the whole note. Use the `modified` timestamp to find notes that changed since your last run.

## Plugins

Plugin code needs no change. The queryset changes to the [Note data model](/sdk/data-note/) shipped in the September 8, 2026 release, and reading a body through the SDK is otherwise unchanged, including each command line's `command_uuid`. The one attribute to move off is `Note.checksum`, for the reason above.

Keep track of upcoming changes [here.](/product-updates/important-dates/)
