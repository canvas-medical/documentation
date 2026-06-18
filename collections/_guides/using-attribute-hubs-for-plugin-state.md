---
title: "Using AttributeHubs for Plugin State"
guide_for:
- /sdk/custom-data-attribute-hubs/
- /sdk/handlers-cron-task/
- /sdk/custom-data/
---

Plugins that run on a schedule often need to remember where they left off. A
lab sync needs a cursor so it doesn't re-fetch results. A reminder system needs
to track which patients have already been contacted. A data pipeline needs a
lock so overlapping runs don't collide.

[AttributeHubs](/sdk/custom-data-attribute-hubs/) are a natural fit for this
kind of state. A single hub can hold a mix of strings, numbers, booleans,
timestamps, and JSON structures — no schema definition required. In this guide
you'll build a plugin that periodically syncs lab results from an external
vendor and uses one AttributeHub to manage its sync cursor, run lock,
configuration, and operational statistics.

{% include alert.html type="info" content="This guide assumes you have the
Canvas CLI installed and configured, and that you're familiar with plugin
basics. If you're starting from scratch, work through
<a href='/guides/your-first-plugin/'>Your First Plugin</a> first." %}

## What we're building

The plugin has two components:

1. **A cron handler** that runs every 10 minutes and processes a batch of lab
   results. This guide uses generated demo data so you can deploy it
   immediately and see it work. In production, you'd swap in a real API call to
   your lab vendor — only the `fetch_results` method changes.
2. **A single AttributeHub** that stores all of the sync state: cursor position,
   run lock, processing stats, and a mapping of the vendor's test codes to
   LOINC codes.

The hub demonstrates several AttributeHub value types working together:

| Attribute | Type | Purpose |
|-----------|------|---------|
| `last_sync_cursor` | datetime | Timestamp of the most recent result fetched |
| `is_running` | boolean | Lock flag to prevent overlapping runs |
| `last_run_at` | datetime | When the sync last completed |
| `results_synced` | integer | Running total of results processed |
| `batch_size` | integer | How many results to pull per run |
| `code_mapping` | JSON (dict) | Vendor test codes → LOINC codes |
| `failed_accessions` | JSON (list) | Accession numbers that failed processing |

## Initialize the plugin

```sh
$ canvas init
  [1/1] project_name (My Cool Plugin): Lab Sync
Project created in /Users/you/lab-sync
```

```sh
cd lab-sync
```

Remove the placeholder handler since we'll create our own:

```sh
rm lab_sync/handlers/event_handlers.py
```

## Configure the manifest

Replace the contents of `lab_sync/CANVAS_MANIFEST.json`:

```json
{
    "sdk_version": "0.1.4",
    "plugin_version": "0.0.1",
    "name": "lab_sync",
    "description": "Syncs lab results from an external vendor on a schedule",
    "components": {
        "handlers": [
            {
                "class": "lab_sync.handlers.sync_labs:SyncLabs",
                "description": "Cron job that pulls lab results from an external vendor"
            }
        ]
    },
    "secrets": [],
    "custom_data": {
        "namespace": "my_org__lab_sync",
        "access": "read_write"
    },
    "tags": {},
    "license": "",
    "readme": "./README.md"
}
```

Replace `my_org` in the namespace with your organization's name.

## Build the sync handler

Create `lab_sync/handlers/sync_labs.py`. This version uses generated demo data
so you can install it and see every code path exercised immediately. The
`fetch_results` method is the only part you'd replace with a real API call in
production — everything else stays the same.

```python
from datetime import datetime, timezone, timedelta
from canvas_sdk.effects import Effect
from canvas_sdk.handlers.cron_task import CronTask
from canvas_sdk.v1.data import AttributeHub
from logger import log


# Default vendor test code → LOINC mapping. In practice this might come from
# the vendor's API or a configuration endpoint.
DEFAULT_CODE_MAPPING = {
    "CBC": "58410-2",
    "BMP": "51990-0",
    "HBA1C": "4548-4",
    "TSH": "3016-3",
    "LIPID": "57698-3",
}

# Demo data: test codes to cycle through. Includes "UNKNOWN_PANEL" to exercise
# the failure/unmapped-code path.
DEMO_TEST_CODES = ["CBC", "HBA1C", "UNKNOWN_PANEL", "TSH", "BMP", "LIPID"]


def get_sync_state():
    """Load or create the sync state hub with sensible defaults."""
    hub, created = AttributeHub.objects.get_or_create(
        type="lab_sync_state",
        id="singleton",
    )

    if created:
        hub.set_attributes({
            "is_running": False,
            "results_synced": 0,
            "batch_size": 50,
            "code_mapping": DEFAULT_CODE_MAPPING,
            "failed_accessions": [],
        })
        log.info("Initialized lab sync state hub with defaults")

    return hub


class SyncLabs(CronTask):
    SCHEDULE = "*/10 * * * *"  # Every 10 minutes

    def execute(self) -> list[Effect]:
        hub = get_sync_state()

        # Check the run lock to prevent overlapping syncs
        if hub.get_attribute("is_running"):
            log.info("Lab sync already in progress, skipping")
            return []

        # Acquire the lock
        hub.set_attribute("is_running", True)

        try:
            results = self.fetch_results(hub)
            self.process_results(hub, results)
        finally:
            # Always release the lock, even if something fails
            hub.set_attributes({
                "is_running": False,
                "last_run_at": datetime.fromisoformat(self.target),
            })

        return []

    def fetch_results(self, hub):
        """Generate demo lab results.

        In a real plugin, this method would call the vendor's API using
        canvas_sdk.utils.Http. The demo generates 3 results per run with
        timestamps after the current cursor so the sync always has work to do.
        """
        cursor = hub.get_attribute("last_sync_cursor") or ""
        synced_count = hub.get_attribute("results_synced") or 0

        # Use the synced count to cycle through demo test codes so each run
        # produces different results.
        now = datetime.now(timezone.utc)
        results = []
        for i in range(3):
            code_index = (synced_count + i) % len(DEMO_TEST_CODES)
            collected_at = (now + timedelta(seconds=i)).replace(microsecond=0)
            results.append({
                "accession_number": f"DEMO-{synced_count + i + 1:04d}",
                "test_code": DEMO_TEST_CODES[code_index],
                "collected_at": collected_at,
            })

        return results

    def process_results(self, hub, results):
        """Process fetched results and update sync state."""
        if not results:
            log.info("No new lab results to process")
            return

        code_mapping = hub.get_attribute("code_mapping") or {}
        failed = hub.get_attribute("failed_accessions") or []
        synced_count = hub.get_attribute("results_synced") or 0
        latest_cursor = hub.get_attribute("last_sync_cursor")

        for result in results:
            accession = result.get("accession_number", "")
            vendor_code = result.get("test_code", "")
            loinc_code = code_mapping.get(vendor_code)

            if not loinc_code:
                log.info(
                    f"No LOINC mapping for vendor code '{vendor_code}' "
                    f"(accession {accession}), skipping"
                )
                failed.append(accession)
                continue

            # In a real plugin, you would create an Observation here using
            # canvas_sdk.effects.observation.Observation with the mapped LOINC code.
            log.info(
                f"Processed result {accession}: {vendor_code} → {loinc_code}"
            )

            synced_count += 1
            result_timestamp = result.get("collected_at")
            if latest_cursor is None or result_timestamp > latest_cursor:
                latest_cursor = result_timestamp

        hub.set_attributes({
            "last_sync_cursor": latest_cursor,
            "results_synced": synced_count,
            "failed_accessions": failed,
        })

        log.info(
            f"Lab sync complete: {len(results)} fetched, "
            f"{synced_count} total synced, {len(failed)} failed"
        )
```

## Anatomy of the plugin

### State initialization

The `get_sync_state` function uses `get_or_create` to ensure the state hub
exists. On first run, it seeds the hub with default values:

```python?partial=true
hub, created = AttributeHub.objects.get_or_create(
    type="lab_sync_state",
    id="singleton",
)

if created:
    hub.set_attributes({
        "is_running": False,
        "results_synced": 0,
        "batch_size": 50,
        "code_mapping": DEFAULT_CODE_MAPPING,
        "failed_accessions": [],
    })
```

Because this plugin only needs one state hub, we use the fixed id `"singleton"`.
The `type` and `id` together form a unique key, so every invocation loads the
same hub.

Notice the variety of types in one hub: a boolean lock, integer counters and
configuration, a dict for code mappings, and a list for tracking failures.
Timestamp attributes like `last_sync_cursor` and `last_run_at` start as `None`
(unset) and are populated with `datetime` objects once the first run completes.
`set_attributes` maps each Python type to the appropriate database column
automatically.

### Run lock

The `is_running` boolean prevents overlapping syncs. Since the cron runs every
10 minutes, a slow API response could cause the next invocation to start before
the previous one finishes. The lock pattern is straightforward:

```python?partial=true
if hub.get_attribute("is_running"):
    log.info("Lab sync already in progress, skipping")
    return []

hub.set_attribute("is_running", True)

try:
    # ... do work ...
finally:
    hub.set_attributes({
        "is_running": False,
        "last_run_at": datetime.fromisoformat(self.target),
    })
```

The `finally` block ensures the lock is released even if processing raises an
exception. Without it, a crash would leave `is_running` as `True` permanently,
and the sync would never run again. Note that `self.target` is an ISO 8601
string, so we parse it into a `datetime` before storing it — this way
AttributeHub stores it in the `timestamp_value` column rather than as text.

### Cursor-based pagination

Each run picks up where the last one left off by reading `last_sync_cursor`.
In a production plugin, this cursor would be sent to the vendor API so it only
returns newer results. After processing a batch, the cursor advances to the
timestamp of the most recent result:

```python?partial=true
cursor = hub.get_attribute("last_sync_cursor") or ""
# ... fetch and process results ...
hub.set_attribute("last_sync_cursor", latest_cursor)
```

On the very first run, the cursor is an empty string. Each subsequent run
advances the cursor to the most recent result's timestamp, so a real vendor API
call would only return results newer than the cursor.

### Code mapping as JSON

The `code_mapping` attribute is a Python dict stored as JSON in the database.
It maps the vendor's proprietary test codes to standard LOINC codes:

```python?partial=true
code_mapping = hub.get_attribute("code_mapping") or {}
# ...
loinc_code = code_mapping.get(vendor_code)
```

This mapping doesn't belong in a CustomModel column because its keys vary by
vendor. A different lab system would have entirely different test codes. Storing
it as a JSON attribute means the mapping can be updated at runtime — for example,
through a separate admin API endpoint — without any schema changes.

### Failure tracking

Failed accession numbers accumulate in the `failed_accessions` list attribute.
This gives operators visibility into which results couldn't be processed,
without building a separate error-tracking table:

```python?partial=true
failed = hub.get_attribute("failed_accessions") or []
# ...
failed.append(accession)
# ...
hub.set_attribute("failed_accessions", failed)
```

In a production plugin you might periodically clear this list after the
failures have been investigated, or cap its length to prevent unbounded growth.

## Install and test

Install the plugin:

```sh
canvas install lab-sync --host YOUR_INSTANCE
```

Stream the logs to watch the sync run:

```sh
canvas logs --host YOUR_INSTANCE
```

Within 10 minutes you should see the first run initialize the state hub and
process the demo batch:

```text
INFO Initialized lab sync state hub with defaults
INFO Processed result DEMO-0001: CBC → 58410-2
INFO Processed result DEMO-0002: HBA1C → 4548-4
INFO No LOINC mapping for vendor code 'UNKNOWN_PANEL' (accession DEMO-0003), skipping
INFO Lab sync complete: 3 fetched, 2 total synced, 1 failed
```

The first two results mapped successfully. The third — `UNKNOWN_PANEL` — had no
entry in `code_mapping`, so it was added to the `failed_accessions` list. On
the next run, the demo cycles to different test codes and the accession numbers
continue incrementing, so you can watch the cursor, counters, and failure list
evolve over successive runs.

## Inspecting and updating state

Because all sync state lives in a single AttributeHub, you can inspect or
adjust it through a SimpleAPI endpoint or a plugin-based application.
For example, to reset the cursor and re-sync from scratch:

```python?partial=true
hub = AttributeHub.objects.get(type="lab_sync_state", id="singleton")
hub.set_attributes({
    "last_sync_cursor": "",
    "results_synced": 0,
    "failed_accessions": [],
})
```

To add a new code mapping without redeploying:

```python?partial=true
hub = AttributeHub.objects.get(type="lab_sync_state", id="singleton")
mapping = hub.get_attribute("code_mapping")
mapping["VITAMIN_D"] = "1989-3"
hub.set_attribute("code_mapping", mapping)
```

This is one of the practical benefits of storing configuration as AttributeHub
attributes — it's data you can change at runtime, not code you have to redeploy.

## Connecting to a real vendor

To swap the demo data for a real lab vendor API, replace `fetch_results` with
an HTTP call using `canvas_sdk.utils.Http`. The rest of the plugin stays
exactly the same.

```python?partial=true
from canvas_sdk.utils import Http

def fetch_results(self, hub):
    """Pull a batch of results from the vendor API."""
    base_url = self.secrets["LAB_VENDOR_BASE_URL"]
    api_key = self.secrets["LAB_VENDOR_API_KEY"]
    cursor = hub.get_attribute("last_sync_cursor") or ""
    batch_size = hub.get_attribute("batch_size")

    http = Http()
    response = http.get(
        f"{base_url}/results",
        headers={
            "Authorization": f"Bearer {api_key}",
            "X-Since": cursor,
            "X-Limit": str(batch_size),
        },
    )

    if not response.ok:
        log.info(
            f"Lab vendor API returned {response.status_code}, "
            f"skipping this run"
        )
        return []

    return response.json().get("results", [])
```

You'll also need to add the secrets to your manifest and configure them at
install time:

```json?partial=true
"secrets": ["LAB_VENDOR_API_KEY", "LAB_VENDOR_BASE_URL"],
```

```sh
canvas install lab-sync \
    --host YOUR_INSTANCE \
    --secret LAB_VENDOR_API_KEY=your-api-key \
    --secret LAB_VENDOR_BASE_URL=https://api.labvendor.example.com/v1
```

The vendor's response must include a `results` array of objects with at minimum
`accession_number`, `test_code`, and `collected_at` fields to match what
`process_results` expects.

## When to use a CustomModel instead

A single state hub works well when your plugin manages a handful of values
that are read and written as a group. Consider switching to
[CustomModels](/sdk/custom-data-custom-models/) when:

- You need to **store one record per entity** (e.g., sync status per patient).
  A separate hub per patient works up to a point, but a CustomModel with a
  foreign key to Patient gives you proper relationships and efficient queries.
- You need to **query by attribute value** across many records. Finding all hubs
  where `results_synced > 100` requires a JOIN to the attribute table per
  condition. A CustomModel with an indexed integer column handles this natively.
- Your **state has grown into a stable schema**. If you find yourself always
  reading and writing the same set of attributes, that's a sign the data has
  matured into a schema worth formalizing.

For a deeper comparison, see
[Design Considerations](/sdk/custom-data-design-considerations/).

<br/>
<br/>
<br/>
