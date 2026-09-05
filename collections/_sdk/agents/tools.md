---
title: "Tools"
slug: "agents-tools"
excerpt: "How agents discover and call functions on the EHR — and how you authorize them."
---

A tool is a named function paired with a JSON-Schema describing its
inputs. The agent advertises tools to the LLM; the LLM picks one,
chooses arguments, and asks the agent to invoke it; the agent
dispatches to the matching executor and feeds the result back into
the model on the next turn.

The SDK gives you a `ToolRegistry` to hold the catalog, a built-in
`standard_tools` set of clinical reads, and a manifest-driven
permission filter so the EHR administrator (not the agent itself)
controls which tools any given agent can use.

## The two kinds of tools

**Read tools** answer questions about the chart. They don't change
state; the agent uses them to inform its decisions. The SDK ships a
broad clinical-reads catalog in `standard_tools` — medications,
conditions, labs, allergies, immunizations, vitals, tasks,
appointments, encounters, goals, imaging reports, referrals, care
team, prescriptions, banner alerts, and more — see the full list
in the [catalog section](#the-sdk-standard_tools-catalog) below.

**Effect tools** stage Canvas Effects (draft commands, tasks, banner
alerts, etc.) into a shared accumulator that the agent returns from
`run()`. The platform dispatches each emitted effect through
`handle_effect` exactly once *after* the run completes — the model
decides *what* to emit; the platform decides *when*. Effect tools
typically never commit anything outright; they originate drafts the
clinician then reviews.

## Defining a registry

Plugin authors register tools at module-import time. Mix the SDK's
standard tools with your own.

The SDK ships three opinionated helpers — `filter_search_tool`,
`originate_command_tool`, and `add_effect_tool` — that take a
declarative spec and synthesize the JSON Schema, executor wiring,
and registration for you. Use them when your tool fits one of the
three common shapes; fall back to the raw `tool()` decorator for
anything bespoke.

```python
from datetime import date, timedelta
from uuid import uuid4

from canvas_sdk.agents import EffectField, FilterSpec, ToolRegistry, standard_tools
from canvas_sdk.commands import PrescribeCommand
from canvas_sdk.effects.task.task import AddTask
from canvas_sdk.v1.data import Condition

tools = ToolRegistry()
tools.extend(standard_tools)  # adopt the SDK catalog


# READ — filter-spec tool. The decorated function is the per-row
# serializer; the helper handles JSON Schema synthesis, patient-scope
# enforcement via queryset_factory, filter application, ordering, and
# limit clamping.
@tools.filter_search_tool(
    name="find_chronic_conditions",
    description=(
        "Search the patient's chronic conditions — active conditions "
        "with onset more than six months ago."
    ),
    queryset_factory=lambda args, pid: Condition.objects.active().filter(
        patient__id=pid,
        onset_date__lte=date.today() - timedelta(days=180),
    ),
    filters={
        "name_contains": FilterSpec(
            type="string",
            description="Substring match on the coding display.",
            apply=lambda qs, v: qs.filter(codings__display__icontains=v),
        ),
    },
    prefetch_related=("codings",),
    model=Condition,
    returns_description="Each row: id, code, display, onset_date.",
    categories=("clinical_reads",),
)
def _serialize_chronic_condition(condition):
    coding = condition.codings.first()
    return {
        "id": str(condition.id),
        "code": coding.code if coding else None,
        "display": coding.display if coding else "(unknown)",
        "onset_date": (
            condition.onset_date.isoformat() if condition.onset_date else None
        ),
    }


# WRITE — note-bound originate-command tool. The helper resolves the
# target note from ctx, instantiates the Command, calls .originate(),
# and appends the resulting Effect. NEVER commits — the clinician
# reviews the draft in the chart UI.
tools.originate_command_tool(
    name="originate_prescribe_medication",
    description=(
        "Stage a draft Prescribe command on the patient's current open "
        "note for the clinician to review, edit, and commit."
    ),
    command_class=PrescribeCommand,
    fields={
        "sig": EffectField(
            type="string",
            description="Patient instructions (e.g., 'Take 1 tablet daily').",
            required=True,
        ),
        "fdb_code": EffectField(
            type="string",
            description="FDB code identifying the medication.",
        ),
    },
    categories=("clinical_writes",),
)


# WRITE — non-note-bound Effect tool. The helper auto-injects
# patient_id from ctx and lets you generate UUIDs or transform field
# values in pre_build. response_builder shapes the dict returned to
# the model on success.
tools.add_effect_tool(
    name="create_followup_task",
    description=(
        "Create a follow-up task tagged with the 'follow-up' label so "
        "the triage workflow can route it."
    ),
    effect_class=AddTask,
    fields={
        "title": EffectField(type="string", description="Task title.", required=True),
    },
    pre_build=lambda args, ctx: {
        "id": str(uuid4()),
        "title": args["title"].strip()[:200],
        "labels": ["follow-up"],
    },
    response_builder=lambda effect: {"ok": True, "task_id": str(effect.id)},
    categories=("task_writes",),
)
```

### When to use which helper

- **`filter_search_tool`** — patient-scoped reads with optional
  filters. The decorated function serializes one row. The model gets
  one tool that combines filter arguments, rather than many narrow
  tools. Used by almost every `find_*` in the SDK catalog.
- **`originate_command_tool`** — staging a draft chart Command on the
  patient's current note. Resolves the note from `ctx["note_id"]` by
  default (override `note_resolver` if your agent finds the note
  differently). Patient scope flows through the Command.
- **`add_effect_tool`** — patient-scoped Effects that aren't pinned
  to a specific note (tasks, banner alerts, protocol cards). Auto-
  injects `patient_id` from ctx onto the Effect; `inject_ctx={}` to
  opt out (e.g., for `update_task` which is identified by `task_id`,
  not derived from the current patient).

### Escape hatch: `@tools.tool`

For tools that don't fit any of the three helper shapes — scalar
reads that return a fixed-shape object, custom workflows that span
multiple Effects, integrations with non-Canvas APIs — drop down to
the raw decorator and hand-build the executor:

```python
@tools.tool(
    name="get_visit_pattern",
    description="Return a summary of the patient's visit frequency.",
    input_schema={"type": "object", "properties": {}},
    returns_description="Object with `visits_last_year` and `avg_days_between_visits`.",
    categories=("clinical_reads",),
)
def _get_visit_pattern(arguments, *, ctx):
    patient_id = ctx["patient_id"]
    # ...compute summary from Appointment queryset...
    return {"visits_last_year": 4, "avg_days_between_visits": 92}
```

The SDK's `get_patient_demographics` is registered this way for
exactly this reason — it returns one dict, not a list, so it doesn't
fit `filter_search_tool`.

## Executor signature

The helpers generate executors with this signature behind the scenes;
you only write one directly when using the raw `@tools.tool`
decorator. Either way, every executor takes the same two arguments:

```python
def my_tool(arguments: dict, *, ctx: dict) -> Any: ...
```

- `arguments` — the model's `tool_use.input` dict. The model chose
  these values from the input schema. Validate as needed before use.
- `ctx` — the platform's per-run context. The model never sees this.
  Common keys:
  - `patient_id` — string UUID of the patient this run is scoped to.
  - `note_id` — for triggered agents that target a specific note.
  - `effects` — the list to append staged Effects to (used by effect tools).

Use `ctx` for anything the model shouldn't choose — patient scoping,
note targeting, the effects accumulator. Never trust `arguments` for
scope (a malicious or hallucinating model could try to switch
patients via an argument). The SDK's `standard_tools` enforce scope
this way: `find_medications` reads `ctx["patient_id"]` and filters
the query on it regardless of what the model passes.

## Attaching tools to an agent

Declare the registry as a class attribute on your `AgentPlugin`
subclass:

```python
from my_plugin.agents.chart_summary_tools import tools as _registered_tools

class ChartSummary(AgentPlugin):
    tools = _registered_tools

    def run(self, state, gateway, trigger_payload):
        # self.tools is the manifest-scoped view — already filtered.
        # Use it, not the imported _registered_tools.
        client.messages.create(tools=self.tools.definitions(), ...)
        result = self.tools.execute(name, args, ctx=tool_ctx)
```

Inside `run()`, always use `self.tools` — that's the platform-scoped
view (see [Permissions](#manifest-driven-permissions)). The
underscore on `_registered_tools` is a convention to signal "don't
reach for me directly."

## Definitions for the model

`self.tools.definitions()` returns a list of dicts shaped for the
Anthropic tool-use API:

```python
[
    {"name": "find_medications", "description": "...", "input_schema": {...}},
    {"name": "originate_plan", "description": "...", "input_schema": {...}},
]
```

Hand this list to `client.messages.create(tools=...)`.

## Dispatching a tool call

When the model returns a `ToolUseBlock`, dispatch it through the
registry:

```python
try:
    result = self.tools.execute(block.name, dict(block.input), ctx=tool_ctx)
    tool_results.append({
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": json.dumps(result, default=str),
    })
except Exception as exc:
    tool_results.append({
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": f"Tool failed: {exc!s}",
        "is_error": True,
    })
```

Errors should go back to the model as `is_error=True` `tool_result`
blocks rather than crashing the run — the model will self-correct on
the next turn (typically by trying different arguments or a
different tool).

## Manifest-driven permissions

The agent's `tools.allowed` declaration in `CANVAS_MANIFEST.json` is
the contract:

```jsonc
{
  "components": {
    "agents": [
      {
        "class": "my_plugin.agents.chart_chat:ChartChatAgent",
        "description": "Chat agent over the patient chart",
        "tools": {
          "allowed": [
            "find_medications",
            "find_conditions",
            "create_task",
            "originate_prescribe_medication"
          ]
        }
      }
    ]
  }
}
```

At run time the platform:

1. Reads `tools.allowed` from the manifest entry for this agent.
2. Sets `self.tools_allowed = frozenset(tools.allowed)`.
3. Replaces `self.tools` with a *scoped* registry containing only
   those tools — disallowed entries aren't in the registry at all.

After step 3, `self.tools.definitions()` returns only the allowlisted
subset (the model never sees the others) and
`self.tools.execute("disallowed_name", ...)` raises `ValueError`
because the executor isn't reachable. There's no per-call `allowed=`
parameter to remember — the registry itself is pre-filtered.

**Why this matters**: the manifest is the single source of truth.
The EHR administrator reviewing your plugin can read the manifest
and know exactly which tools each agent can use. The agent code
can't widen that surface — even accidentally — because `self.tools`
is the only handle the platform hands it.

A determined plugin author could `from my_plugin.agents.chart_chat_tools
import tools` directly and reach the unfiltered registry. That gap
will close in a future release via sandbox-level isolation; for now,
treat the unfiltered registry as platform-internal. The underscore-
prefixed import convention is meant to remind future-you.

## Tool surface design tips

- **Be specific in `description`.** The model picks tools based on
  the description alone. Mention what the tool returns and when to
  use it. Compare:
  - Bad: "Returns medications."
  - Good: "Returns the patient's medications with optional filters
    (`name_contains`, `active_only`, `started_on_or_after`). Use
    this when the conversation needs current or historical
    prescription info."
- **Prefer filter-spec tools over many narrow tools.** One tool with
  filter parameters (`find_medications(name_contains?, active_only?,
  ...)`) is easier for the model than five overlapping tools
  (`find_active_medications`, `find_recent_medications`, ...). The
  SDK's `standard_tools` use this pattern.
- **Enforce scope in `ctx`, never in `arguments`.** `patient_id`
  comes from the platform's `ctx`; the model can't switch patients
  via tool arguments.
- **Return JSON-serializable values.** The agent's loop typically
  does `json.dumps(result, default=str)` to feed it back to the
  model.
- **For effect tools, return a small confirmation dict, not the
  whole effect.** The model only needs to know the call succeeded;
  details of the staged effect are platform-side concerns.
- **Originate, don't commit.** Effect tools that stage chart
  commands should call `.originate()` (draft), not `.commit()`. The
  clinician reviews the draft in the chart UI.

## The SDK `standard_tools` catalog

The SDK ships an opinionated catalog of clinical reads and writes
behind `canvas_sdk.agents.standard_tools`. Patient scope is enforced
by each tool — you can't widen it via filter arguments. The catalog
is grouped into manifest-friendly `@category` tags so plugin authors
can grant access by tool family rather than enumerating every name.

The sections below are auto-generated from the registry — they
reflect the SDK version pinned in your plugin's environment. Hand
edits inside the `<!-- AUTOGEN -->` markers will be overwritten on
the next regeneration.

### By category

Grant a category in your manifest with the `@` prefix (e.g.,
`"allowed": ["@clinical_reads", "@task_writes"]`). Add a `denied`
list to opt out of specific tools within a granted category:

```jsonc
{
  "tools": {
    "allowed": ["@clinical_reads", "@clinical_writes"],
    "denied": ["originate_diagnose_condition"]
  }
}
```

<!-- AUTOGEN:categories START -->
- **`@clinical_alerts`** (3 tools): `add_banner_alert`, `remove_banner_alert`, `add_or_update_protocol_card`
- **`@clinical_reads`** (24 tools): `find_medications`, `find_conditions`, `find_lab_results`, `find_assessments`, `find_allergies`, `find_immunizations`, `find_vitals`, `find_appointments`, `find_encounters`, `find_notes`, `get_open_note`, `get_note_content`, `find_goals`, `find_imaging_reports`, `find_referrals`, `find_care_team_members`, `find_medication_statements`, `find_external_events`, `find_prescriptions`, `find_questionnaire_responses`, `find_stop_medication_events`, `find_banner_alerts`, `find_protocol_cards`, `get_patient_demographics`
- **`@clinical_writes`** (9 tools): `originate_review_note`, `originate_plan`, `originate_prescribe_medication`, `originate_lab_order`, `originate_diagnose_condition`, `originate_goal`, `originate_assessment`, `originate_follow_up`, `originate_stop_medication`
- **`@config_reads`** (4 tools): `find_note_types`, `find_practice_locations`, `find_lab_partners`, `find_lab_partner_tests`
- **`@message_reads`** (1 tool): `find_messages`
- **`@message_writes`** (1 tool): `originate_message`
- **`@task_reads`** (1 tool): `find_tasks`
- **`@task_writes`** (3 tools): `create_task`, `update_task`, `add_task_comment`
<!-- AUTOGEN:categories END -->

### Reads

The clinical reads. Patient scope is enforced internally; row `id`
fields chain into write tools that need them (e.g., the `id` from
`find_conditions` feeds `originate_assessment` in a plugin-side
originate-command tool).

<!-- AUTOGEN:reads START -->
#### `find_medications`

**Category:** `@clinical_reads`

Search the patient's medications with optional filters. Returns each matching medication as an object with `name` (display from the first coding, typically RxNorm), `status` ("active" or "inactive"), `start_date` (ISO 8601 or null), and `end_date` (ISO 8601 or null). Patient scope is enforced — the tool only returns records for the current agent's patient. If no filters are supplied, returns the most recent records by start_date.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match against the medication's first-coding display. E.g. 'metformin' matches 'Metformin 500 mg tablet'. |
| `active_only` | boolean | no | When true, restrict to active (status='active', committed) medications. When false or omitted, include inactive too. |
| `started_on_or_after` | string (date) | no | ISO 8601 date (YYYY-MM-DD). When supplied, only return medications with start_date >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, `status` (active|inactive), `start_date` (ISO 8601 or null), `end_date` (ISO 8601 or null).

**Backing data model:** `Medication`.

#### `find_conditions`

**Category:** `@clinical_reads`

Search the patient's conditions with optional filters. Returns each matching condition with `code` (the first coding's identifier — typically ICD-10), `display`, `clinical_status` (active, resolved, remission, relapse, investigative), `onset_date` (ISO 8601 or null), and `resolution_date` (ISO 8601 or null). Defaults to active conditions only, ordered most-recently-onset first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the coding display (e.g. 'diabetes'). |
| `code_contains` | string | no | Case-insensitive substring match on the coding code (e.g. 'E11' for type-2 diabetes ICD-10 family). |
| `active_only` | boolean | no | When true (default), restrict to currently-active conditions. When false, include resolved/remission/etc. |
| `onset_on_or_after` | string (date) | no | ISO 8601 date. Only return conditions with onset_date >= this. |
| `limit` | integer | no | Max results. Defaults to 25. |

**Returns:** Array of objects with `id`, `code`, `display`, `clinical_status` (active|resolved|remission|relapse|investigative), `onset_date`, `resolution_date`.

**Backing data model:** `Condition`.

#### `find_lab_results`

**Category:** `@clinical_reads`

Search the patient's committed lab results. Returns each matching value with `test` (lab name), `value`, `units`, `abnormal_flag` (e.g. 'H', 'L', or null when normal), and `date` (the report's original_date, ISO 8601). Defaults to the 10 most-recent results.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the lab's coding name (e.g. 'a1c', 'hemoglobin'). |
| `observed_on_or_after` | string (date) | no | ISO 8601 date. Only return results with date >= this. |
| `abnormal_only` | boolean | no | When true, restrict to values with a non-empty abnormal_flag. Useful for spotting out-of-range results quickly. |
| `limit` | integer | no | Max results. Defaults to 10. |

**Returns:** Array of objects with `id`, `test`, `value`, `units`, `abnormal_flag` (e.g. 'H', 'L', or null), `date`.

**Backing data model:** `LabValue`.

#### `find_assessments`

**Category:** `@clinical_reads`

Return the patient's recent clinical assessments (the structured Assess command's status + narrative on a note). Each result has `status` ('improved', 'stable', 'deteriorated'), `narrative`, `background`, `condition_display` (the associated condition's name, if any), and `date` (the source note's datetime_of_service, ISO 8601). Ordered most-recent first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Max results. Defaults to 10. |

**Returns:** Array of objects with `id`, `status`, `narrative`, `background`, `condition_display`, `date`.

**Backing data model:** `Assessment`.

#### `find_allergies`

**Category:** `@clinical_reads`

Search the patient's documented allergies and intolerances. Returns each entry with `display` (allergen name from the first coding), `code` (typically RxNorm or SNOMED), `severity` (e.g., 'mild', 'moderate', 'severe'), `narrative` (free-text reaction description), `status`, and `onset_date` (ISO 8601 or null). Patient scope is enforced. Defaults to non-deleted committed entries, ordered most-recently-onset first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the allergen's display (e.g., 'penicillin', 'peanut', 'sulfa'). |
| `severity` | string | no | Filter to a specific severity. Common values: 'mild', 'moderate', 'severe'. Match is case-insensitive exact. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `display`, `code`, `severity`, `narrative`, `status`, `onset_date`.

**Backing data model:** `AllergyIntolerance`.

#### `find_immunizations`

**Category:** `@clinical_reads`

Search the patient's immunization history. Returns each entry with `display` (vaccine name from the first coding, typically CVX), `code`, `date_administered` (ISO 8601 or null), `status` (e.g., 'administered', 'refused'), `manufacturer`, and `lot_number`. Patient scope is enforced. Ordered most-recent first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the vaccine's display (e.g., 'influenza', 'covid', 'tdap', 'mmr'). |
| `given_on_or_after` | string (date) | no | ISO 8601 date. Only return immunizations with date_ordered >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `display`, `code`, `given_on`, `status`.

**Backing data model:** `Immunization`.

#### `find_vitals`

**Category:** `@clinical_reads`

Search the patient's recorded vital signs — blood pressure, heart rate, temperature, weight, height, BMI, respiratory rate, oxygen saturation, and similar measurements (any Observation in the FHIR `vital-signs` category). Returns each measurement with `name`, `value`, `units`, `code` (typically LOINC from the first coding), and `date` (ISO 8601 effective_datetime). Patient scope is enforced. Defaults to the 10 most recent.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the observation's name (e.g., 'blood pressure', 'weight', 'temperature', 'pulse'). |
| `observed_on_or_after` | string (date) | no | ISO 8601 date. Only return measurements with effective_datetime >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 10. |

**Returns:** Array of objects with `id`, `name`, `value`, `units`, `observed_at`.

**Backing data model:** `Observation`.

#### `find_tasks`

**Category:** `@task_reads`

Search tasks linked to the current patient (clinician follow-ups, outreach reminders, etc.). Returns each task with `id`, `title`, `status` ('OPEN', 'COMPLETED', 'CLOSED'), `due` (ISO 8601 or null), and `task_type`. Defaults to OPEN tasks ordered by due date.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `status` | string (enum) | no | Filter to a specific status. If omitted, defaults to OPEN tasks only. One of: `COMPLETED`, `CLOSED`, `OPEN`. |
| `title_contains` | string | no | Case-insensitive substring match on the task title. |
| `due_on_or_after` | string (date) | no | ISO 8601 date. Only return tasks with due >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `title`, `status`, `due` (ISO 8601), `assignee_name`, `team_name`, `labels`, `created`.

**Backing data model:** `Task`.

#### `find_messages`

**Category:** `@message_reads`

Search the patient's messages (clinician ↔ patient correspondence via the patient portal). Returns each message with `id`, `content`, `sender_role` ('patient' or 'staff'), `sender_name`, `recipient_role`, `recipient_name`, `sent_at` (ISO 8601), and `read_at` (ISO 8601 or null). Defaults to the 20 most recent. Use `from_patient_only=true` to see only incoming messages from the patient (e.g., to draft a reply); `unread_only=true` to scope to messages the recipient hasn't read yet; `since=YYYY-MM-DD` to look at a recent window.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `from_patient_only` | boolean | no | When true, restrict to messages where the sender is a patient (i.e., incoming messages from this patient to their care team). Useful for finding the latest message to reply to. |
| `unread_only` | boolean | no | When true, restrict to messages with no `read` timestamp yet — i.e., the recipient hasn't opened them. |
| `since` | string (date) | no | ISO 8601 date. Only return messages with created >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 20. |

**Returns:** Array of objects with `id`, `content`, `sender_role` ('patient'|'staff'), `sender_name`, `recipient_role`, `recipient_name`, `sent_at`, `read_at`.

**Backing data model:** `Message`.

#### `find_appointments`

**Category:** `@clinical_reads`

Search the patient's appointments. Returns each appointment with `id`, `status`, `start_time` (ISO 8601), `duration_minutes`, `provider_name`, and `description`. Defaults to upcoming appointments ordered by start_time ascending; pass `upcoming_only=false` to include past appointments.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `status` | string (enum) | no | Filter to a specific appointment progress status. Values track the workflow from booking to completion: 'unconfirmed' (booked, not yet confirmed), 'attempted', 'confirmed', 'arrived', 'roomed', 'exited' (visit completed), 'noshowed', 'cancelled'. One of: `unconfirmed`, `attempted`, `confirmed`, `arrived`, `roomed`, `exited`, `noshowed`, `cancelled`. |
| `starts_on_or_after` | string (date) | no | ISO 8601 date. Only return appointments with start_time >= this. |
| `starts_on_or_before` | string (date) | no | ISO 8601 date. Only return appointments with start_time <= this. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `start_time` (ISO 8601), `status`, `appointment_type`, `provider_name`, `note_type`.

**Backing data model:** `Appointment`.

#### `find_encounters`

**Category:** `@clinical_reads`

Search the patient's encounters. Returns each encounter with `id`, `state`, `medium` (e.g., 'in-person', 'phone', 'telehealth'), `start_time` (ISO 8601 or null), and `end_time` (ISO 8601 or null). Defaults to the 25 most-recent encounters ordered by start_time descending.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `state` | string (enum) | no | Filter to a specific encounter state. Three-letter codes: 'STA' (Started), 'PLA' (Planned), 'CON' (Concluded), 'CAN' (Cancelled). One of: `STA`, `PLA`, `CON`, `CAN`. |
| `started_on_or_after` | string (date) | no | ISO 8601 date. Only return encounters with start_time >= this. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `state` (new|locked|unlocked|...), `note_type`, `started_at`, `provider_name`.

**Backing data model:** `Encounter`.

#### `find_notes`

**Category:** `@clinical_reads`

Search the patient's notes (encounter documents). Each row has `id`, `title`, `note_type`, `state` (3-letter code from NoteStates — e.g. 'NEW' (Created), 'LKD' (Locked), 'ULK' (Unlocked), 'SGN' (Signed)), `datetime_of_service`, and `provider_name`. Filter by `state` to find open vs locked notes, by `note_type` to scope to a category, or by `since` to look at recent history only. Defaults to most-recent-first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `state` | string (enum) | no | Restrict to notes in a specific lifecycle state. Three-letter NoteStates code — pick from the enum. Filters on the canonical current state, not the note's initial state. Common values: 'NEW' (created/open), 'LKD' (locked), 'ULK' (unlocked), 'SGN' (signed), 'DLT' (deleted). One of: `NEW`, `PSH`, `LKD`, `ULK`, `DLT`, `RLK`, `RST`, `RCL`, `UND`, `DSC`, `SGN`, `SCH`, `BKD`, `CVD`, `CLD`, `NSW`, `RVT`, `CNF`. |
| `note_type` | string (enum) | no | Restrict to notes whose category matches. Broad bucket from NoteTypeCategories (the canonical category enum). Common values: 'encounter' (catch-all for in-person / telehealth / phone / video / home / lab visits), 'inpatient', 'review' (chart review), 'message', 'letter', 'appointment'. For a more specific match like 'Telehealth' vs 'Office visit' (both encounter), use `note_type_name_contains`. One of: `message`, `letter`, `inpatient`, `review`, `encounter`, `appointment`, `task`, `data`, `ccda`, `schedule_event`. |
| `note_type_name_contains` | string | no | Case-insensitive substring match on the note type's display name (e.g., 'Telehealth', 'Office visit', 'Chart review', 'Home visit'). More granular than `note_type` — use to disambiguate within a category. |
| `since` | string (date) | no | ISO 8601 date. Only return notes with datetime_of_service >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id` (UUID), `dbid` (integer — Canvas-internal navigation handle), `title`, `note_type` (NoteTypeCategories enum value — e.g., 'encounter', 'inpatient', 'review'), `note_type_name` (the type's display name — e.g., 'Telehealth', 'Office visit', 'Chart review'), `state` (NoteStates code or null), `datetime_of_service` (ISO 8601), `provider_name`.

**Backing data model:** `Note`.

#### `get_open_note`

**Category:** `@clinical_reads`

Return metadata for the patient's current open note (the most-recent note in a mutable state — NEW, UNLOCKED, or CONVERTED). Use this when the user references 'this note' or 'the open note' and the agent needs the note_id to drill into it or stage a command on it. Returns the same row shape as one find_notes entry, or null if no open note exists.

**Arguments:** none.

**Returns:** Object matching find_notes' row shape (`id`, `dbid`, `title`, `note_type`, `note_type_name`, `state`, `datetime_of_service`, `provider_name`), or null if the patient has no notes in an open state.

#### `get_note_content`

**Category:** `@clinical_reads`

Read the contents of a specific note in document order — the free-text narrative the clinician typed interleaved with the structured clinical commands they committed (Plan, Assess, Diagnose, Prescribe, LabOrder, etc.). Use this when the user asks about a specific note ('what's in this note?', 'did today's visit address X?', 'summarize the assessment') so the agent can answer without the clinician having to re-read the note themselves. Skips entered-in-error commands and empty text blocks. Patient scope is enforced — a note belonging to a different patient returns null.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `note_id` | string | yes | UUID of the note to read. From a prior find_notes or get_open_note call (the row's `id` field). |

**Returns:** Object with the note's metadata (`id`, `dbid`, `title`, `note_type`, `note_type_name`, `state`, `datetime_of_service`, `provider_name`) plus a `content` array of items in document order. Each item is either `{type: 'text', value: <free-text>}` (the clinician's narrative between commands) or `{type: 'command', uuid, schema_key, state, data}` (a structured chart command — schema_key like 'plan'/'assess'/'labOrder', data containing the command-specific fields). Returns null if no note with that id exists for the current patient.

#### `find_goals`

**Category:** `@clinical_reads`

Search the patient's care-plan goals. Returns each goal with `goal_statement`, `lifecycle_status` (e.g., 'active', 'completed', 'cancelled'), `achievement_status` (e.g., 'in-progress', 'achieved'), `priority` ('high-priority', 'medium-priority', 'low-priority'), `start_date` (ISO 8601 or null), `due_date` (ISO 8601 or null), and `progress` (free-text note). Defaults to active goals ordered by most-recent start_date.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `statement_contains` | string | no | Case-insensitive substring match on the goal_statement text. |
| `lifecycle_status` | string (enum) | no | Filter to a specific GoalLifecycleStatus value (e.g., 'active', 'completed', 'cancelled'). One of: `proposed`, `planned`, `accepted`, `active`, `on-hold`, `completed`, `cancelled`, `rejected`. |
| `achievement_status` | string (enum) | no | Filter to a specific GoalAchievementStatus value (e.g., 'in-progress', 'achieved', 'not-achieved'). One of: `in-progress`, `improving`, `worsening`, `no-change`, `achieved`, `sustaining`, `not-achieved`, `no-progress`, `not-attainable`. |
| `priority` | string (enum) | no | Filter to a specific GoalPriority value ('high-priority', 'medium-priority', 'low-priority'). One of: `high-priority`, `medium-priority`, `low-priority`. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `goal_statement`, `lifecycle_status`, `achievement_status`, `priority`, `start_date`, `due_date`.

**Backing data model:** `Goal`.

#### `find_imaging_reports`

**Category:** `@clinical_reads`

Search the patient's imaging reports. Returns each report with `id`, `name` (test or modality, e.g., 'Chest X-ray'), `assigned_date` (ISO 8601 or null), `source` (e.g., 'internal', 'external'), and `requires_signature` (bool). Patient scope is enforced and junked reports are excluded. Defaults to the 25 most-recent reports.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the report name (e.g., 'chest', 'mammo', 'mri'). |
| `assigned_on_or_after` | string (date) | no | ISO 8601 date. Only return reports with assigned_date >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, `result_status`, `assigned_at`, `narrative`.

**Backing data model:** `ImagingReport`.

#### `find_referrals`

**Category:** `@clinical_reads`

Search the patient's outgoing referrals. Returns each referral with `id`, `clinical_question`, `priority`, `notes` (free-text), `date_referred` (ISO 8601), `service_provider_name`, and `forwarded` (bool). Ordered most-recent first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `question_contains` | string | no | Case-insensitive substring match on the clinical_question field. |
| `priority` | string | no | Filter to a specific priority (free-text on Referral; values depend on the customer's configuration). Case-insensitive. |
| `referred_on_or_after` | string (date) | no | ISO 8601 date. Only return referrals with date_referred >= this. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `service_provider_name`, `clinical_question`, `priority`, `status`, `originated_at`.

**Backing data model:** `Referral`.

#### `find_care_team_members`

**Category:** `@clinical_reads`

Return the staff members on the patient's care team. Each result has `staff_name`, `role_display` (e.g., 'Primary Care Provider', 'Care Manager'), `role_code`, `status` (e.g., 'active', 'inactive'), and `is_lead` (true for the patient's primary contact). Ordered with the lead member first, then by role.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `role_contains` | string | no | Case-insensitive substring match on role_display (e.g., 'primary', 'manager'). |
| `status` | string (enum) | no | Filter to a specific CareTeamMembershipStatus value (e.g., 'active', 'inactive', 'suspended', 'proposed'). One of: `proposed`, `active`, `suspended`, `inactive`, `entered-in-error`. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `staff_name`, `role`, `lead`, `status`.

**Backing data model:** `CareTeamMembership`.

#### `find_note_types`

**Category:** `@config_reads`

List the customer's configured NoteType rows. Returns each type with `id` (the UUID to pass as `note_type_id` to note-creation tools), `name` (display name shown in the UI), `category` (NoteTypeCategories enum value: 'encounter', 'review', 'data', 'task', 'inpatient', 'letter', 'message', 'appointment', 'schedule_event', 'ccda'), `is_active`, and `is_visible`. Customer-level config — NOT patient-scoped; the patient_id on ctx is ignored. Use to resolve a friendly handle ('chart review note', 'office visit') into the UUID note-write tools need.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `category` | string (enum) | no | Restrict to a single NoteTypeCategories value — e.g. 'review' for chart-review notes, 'encounter' for visit notes, 'letter' for letters. One of: `message`, `letter`, `inpatient`, `review`, `encounter`, `appointment`, `task`, `data`, `ccda`, `schedule_event`. |
| `name_contains` | string | no | Case-insensitive substring match on the type's display name (e.g. 'review', 'telehealth', 'office'). |
| `active_only` | boolean | no | When true (default), restrict to currently active types (is_active and is_visible). Set false to include deprecated or hidden types. |
| `limit` | integer | no | Maximum results. Defaults to 50. |

**Returns:** Array of objects with `id`, `name`, `category` (NoteTypeCategories), `is_active`, `is_visible`, `is_billable`, `is_sig_required`.

**Backing data model:** `NoteType`.

#### `find_practice_locations`

**Category:** `@config_reads`

List the customer's configured PracticeLocation rows. Returns each location with `id` (the UUID to pass as `practice_location_id` to note-creation tools), `full_name`, `short_name`, `place_of_service_code` (CMS POS code), and `active`. Customer-level config — NOT patient-scoped. Use to resolve a friendly handle ('main clinic', 'downtown office') into the UUID note-write tools need.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `active_only` | boolean | no | When true (default), restrict to active locations. |
| `name_contains` | string | no | Case-insensitive substring match on full_name (e.g. 'main', 'downtown'). |
| `limit` | integer | no | Maximum results. Defaults to 25. |

**Returns:** Array of objects with `id`, `full_name`, `short_name`, `place_of_service_code`, `active`.

**Backing data model:** `PracticeLocation`.

#### `find_lab_partners`

**Category:** `@config_reads`

List the customer's configured lab partners (LabCorp, Quest, in-house, etc.). Returns each with `id` (UUID to pass as `lab_partner` to `originate_lab_order`), `name`, `active`, and `electronic_ordering_enabled`. Customer-level config — NOT patient-scoped. Step 1 of the order-lab flow: pick a partner here, then call `find_lab_partner_tests(lab_partner_id=<id>)` to discover the orderable tests for that partner.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the partner's name (e.g. 'labcorp', 'quest', 'generic'). |
| `active_only` | boolean | no | When true (default), restrict to active partners. |
| `electronic_ordering_only` | boolean | no | When true, restrict to partners that accept electronic orders (filters out paper-only partners). |
| `limit` | integer | no | Maximum results. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, `active`, `electronic_ordering_enabled`.

**Backing data model:** `LabPartner`.

#### `find_lab_partner_tests`

**Category:** `@config_reads`

Search a lab partner's compendium of orderable tests. Returns each test with `id` (UUID) and `order_code` (the partner's own catalog code) — EITHER value is accepted by `originate_lab_order`'s `tests_order_codes` argument. Also returns `order_name` (display name) and `cpt_code`. Customer-level config — NOT patient-scoped. EXACTLY ONE of `lab_partner_id` or `lab_partner_name` is required to scope the search; without it the result set is empty. Workflow: (1) `find_lab_partners` to choose a partner; (2) `find_lab_partner_tests(lab_partner_id=<id>, search='glucose')` to find tests; (3) `originate_lab_order(lab_partner=<id>, tests_order_codes=[<order_code>, ...])`.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `lab_partner_id` | string | no | UUID of the lab partner whose tests to search — from `find_lab_partners`. Either this or `lab_partner_name`. |
| `lab_partner_name` | string | no | Case-insensitive exact name of the lab partner — alternative to `lab_partner_id`. Either this or `lab_partner_id`. |
| `search` | string | no | Case-insensitive substring match across `order_name`, `order_code`, and `keywords` — same shape as the chart-UI autocomplete (e.g. 'glucose', 'CBC', 'lipid'). |
| `cpt_contains` | string | no | Case-insensitive substring match on the test's CPT code. |
| `limit` | integer | no | Maximum results. Defaults to 25. |

**Returns:** Array of objects with `id`, `order_code`, `order_name`, `cpt_code`.

**Backing data model:** `LabPartnerTest`.

#### `find_medication_statements`

**Category:** `@clinical_reads`

Search the patient's recorded medication statements — patient-reported or self-administered medications (distinct from active prescriptions which `find_medications` covers). Returns each statement with `medication_name`, `start_date` (ISO 8601 or null), `end_date` (ISO 8601 or null), `dose_form`, `dose_route`, `dose_frequency_interval`, and `sig_original_input` (the patient's verbatim sig).

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the medication's first-coding display. |
| `started_on_or_after` | string (date) | no | ISO 8601 date. Only return statements with start_date >= this. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `medication_name`, `narrative`, `recorded_at`.

**Backing data model:** `MedicationStatement`.

#### `find_external_events`

**Category:** `@clinical_reads`

Search external healthcare events recorded for the patient — typically HL7 feeds from external systems (ADT, ORM, etc.). Each event has `event_type` (e.g., 'ADT', 'ORM'), `event_datetime` (ISO 8601), `facility_name` (from the linked external visit), and `information_source`. Useful for understanding the patient's encounters outside the EHR. Ordered most-recent first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `event_type` | string | no | Filter to a specific event_type (e.g., 'ADT' for admit/discharge/transfer, 'ORM' for orders). Case-insensitive exact match. |
| `occurred_on_or_after` | string (date) | no | ISO 8601 date. Only return events with event_datetime >= this. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `event_type`, `event_datetime`, `facility_name`, `information_source`.

**Backing data model:** `ExternalEvent`.

#### `find_prescriptions`

**Category:** `@clinical_reads`

Search the patient's prescription records (actual Rx events — distinct from `find_medications` which surfaces the medication list). Each result has `medication_name`, `status`, `written_date` (ISO 8601), `dispensed_date` (ISO 8601 or null), `end_date` (ISO 8601 or null), `sig_original_input`, `dose_form`, `dose_route`, `dose_frequency_interval`, and `is_refill`. Patient scope is enforced. Defaults to committed prescriptions ordered most-recent first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the medication's first-coding display. |
| `status` | string | no | Filter to a specific prescription status (e.g., 'active', 'completed', 'cancelled'). Case-insensitive. |
| `written_on_or_after` | string (date) | no | ISO 8601 date. Only return prescriptions with written_date >= this. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `medication_name`, `status`, `written_date`, `dispensed_date`, `quantity_to_dispense`, `days_supply`, `is_refill`, `sig_original_input`.

**Backing data model:** `Prescription`.

#### `find_questionnaire_responses`

**Category:** `@clinical_reads`

Search the patient's completed and in-progress questionnaire responses (Interviews). Each result includes `name`, `progress_status`, `questionnaire_names`, `answered_at` (ISO 8601), and `responses` — an array of per-question answers with the question text, the human-readable selection, and `response_value` (the question option's underlying value string, often numeric for scored instruments like PHQ-9 or Stress). For scored questionnaires `response_value` is what you'd chart or sum. For non-scored / categorical ones it may be text — in that case offer the clinician a numeric conversion before plotting and confirm their interpretation before treating it as a score. Patient scope is enforced; non-committed interviews are excluded.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the interview's name (e.g., 'PHQ', 'depression', 'GAD', 'stress'). |
| `progress_status` | string | no | Filter to a specific progress_status code (e.g., 'F' for finished/complete, 'S' for started, 'N' for new). Case-insensitive. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, `progress_status`, `questionnaire_names`, `answered_at`, and `responses` (per-question array of `question`, `response_text`, `response_value`).

**Backing data model:** `Interview`.

#### `find_stop_medication_events`

**Category:** `@clinical_reads`

Search records of medications the patient stopped. Each event has `medication_name`, `rationale` (free-text reason for stopping, captured by the clinician), and `stopped_at` (ISO 8601). Useful for understanding why a medication is no longer active. Ordered most-recent first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the stopped medication's first-coding display. |
| `rationale_contains` | string | no | Case-insensitive substring match on the rationale text (e.g., 'side effects', 'ineffective', 'allergy'). |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `medication_name`, `rationale`, `stopped_at`.

**Backing data model:** `StopMedicationEvent`.

#### `find_banner_alerts`

**Category:** `@clinical_reads`

Search the patient's banner alerts (visual flags shown on the chart). Returns each banner's `key`, `narrative`, `intent` (info/warning/alert), `placement` (list), `href` (or null), and `status` (active/inactive). Use this to discover what's already flagged before adding a duplicate, or to find a banner's key for `remove_banner_alert`. Defaults to active banners only.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `narrative_contains` | string | no | Case-insensitive substring match on the banner's narrative text (e.g., 'mammogram', 'INR'). |
| `intent` | string (enum) | no | Restrict to one visual intent: 'info', 'warning', or 'alert'. One of: `info`, `warning`, `alert`. |
| `include_inactive` | boolean | no | When true, also return banners with status='inactive' (historical/removed). Default false — active only. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `key`, `narrative`, `intent`, `placement` (array of strings), `href`, `status`.

**Backing data model:** `BannerAlert`.

#### `find_protocol_cards`

**Category:** `@clinical_reads`

Search the patient's protocol cards (clinical decision support surfaces shown on the chart). Each card has a `protocol_key` (pass to `add_or_update_protocol_card` as `card_key` to update it), `title`, `narrative`, `status` (due / satisfied / not_applicable / pending / not_relevant), and `plugin_name` identifying which plugin staged it. Use this to discover what's already flagged before adding a new card, to find prior cards your plugin staged that need a status update, or to inspect cards staged by other plugins for context. Defaults to all statuses; filter to active ones via `active_only=true`.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `title_contains` | string | no | Case-insensitive substring match on the card's title. |
| `status` | string | no | Restrict to one lifecycle status: 'due', 'satisfied', 'not_applicable', 'pending', 'not_relevant'. |
| `plugin_name` | string | no | Restrict to cards staged by a specific plugin (exact match). Use to scope find results to your own plugin's cards. |
| `active_only` | boolean | no | When true, return only cards with status='due' or 'pending'. Default false — return cards in any status. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `protocol_key`, `title`, `narrative`, `status`, `plugin_name`, `next_review` (ISO 8601 or null), `snoozed`.

**Backing data model:** `ProtocolCurrent`.

#### `get_patient_demographics`

**Category:** `@clinical_reads`

Return basic demographics for the current patient: legal name, preferred name, MRN, date of birth, computed age in years, sex_at_birth, gender_identity, preferred_pronouns, and whether they're marked deceased. Takes no arguments.

**Arguments:** none.

**Returns:** Object with `first_name`, `middle_name`, `last_name`, `preferred_name`, `mrn`, `birth_date`, `age_years`, `sex_at_birth`, `gender_identity`, `preferred_pronouns`, `deceased`.

#### `originate_review_note`

**Category:** `@clinical_writes`

Stage a draft review-category note for the patient with a single Plan command containing the narrative. NEVER commits — the note + plan draft sit unsigned for the clinician to review, edit, and sign. Use when the clinician asks to draft a chart-review note, lab-review note, or similar narrative summary that isn't tied to a live visit. Before calling: (1) `find_note_types(category='review')` to get a `note_type_id`; (2) `find_practice_locations` to get a `practice_location_id`. Patient + requesting-staff come from the agent's scope automatically.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `narrative` | string | yes | The body of the Plan command on the new note. Plain prose, no markdown. This is what becomes the note's primary content. |
| `note_type_id` | string | yes | UUID of a NoteType row with category='review' — get from `find_note_types(category='review')`. The customer's review note type IDs vary; don't guess. |
| `practice_location_id` | string | yes | UUID of a PracticeLocation row — get from `find_practice_locations`. The customer's locations vary; don't guess. |
| `title` | string | no | Optional note title (e.g., 'Lab review — 2026-05-15'). Falls back to the NoteType's default if omitted. |
| `datetime_of_service` | string (date-time) | no | Optional ISO 8601 datetime. Defaults to now if omitted. Use for back-dated reviews. |

**Returns:** `{ok: true, note_id: <uuid>, command: 'plan', committed: false}`. Two effects are bundled: CREATE_NOTE for the review shell and the Plan command originating onto it. Clinician reviews/edits/signs.

**Backing Command:** `PlanCommand`.
<!-- AUTOGEN:reads END -->

### Writes

Effect tools — each stages a Canvas Effect into the run's accumulator
that the platform dispatches after `run()` returns. None of them
commit chart state outright. Task and banner tools take their target
identifier from the response of a prior `create_*` or `find_*` call;
the "Returns" line on each tool calls out which fields chain.

<!-- AUTOGEN:writes START -->
#### `add_banner_alert`

**Category:** `@clinical_alerts`

Surface a banner alert on the patient — visible to anyone viewing the chart. Use to flag clinically meaningful state the clinician should notice on their next visit (e.g., 'overdue mammogram', 'on warfarin — INR last drawn 8 months ago'). Narrative is truncated to 90 chars. Banners persist until removed; don't create duplicates for the same finding. Returns the generated key so the banner can be referenced/removed later.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `narrative` | string | yes | Short banner text — what the clinician should see. Truncated to 90 chars. E.g. 'Overdue colonoscopy — screening interval was 10y.' |
| `intent` | string (enum) | yes | Visual emphasis. 'info' for neutral context, 'warning' for issues that need attention, 'alert' for safety-critical. One of: `info`, `warning`, `alert`. |
| `placement` | array of string (enum) | yes | Where the banner appears. Most clinical alerts want ['chart']; add 'timeline' to also surface on the patient timeline. Use 'profile' for identity/demographic flags. |
| `href` | string | no | Optional URL the banner links to. Use for deep-links to supporting context (e.g., the lab result page). |

**Returns:** `{ok: true, banner_key: <uuid>}` — pass `banner_key` to `remove_banner_alert` later to take the banner down.

**Backing Effect:** `AddBannerAlert`.

#### `remove_banner_alert`

**Category:** `@clinical_alerts`

Remove a previously-staged banner alert from the patient's chart. Takes the banner's `key` — obtained either from a prior `add_banner_alert` call (returned as `banner_key` in the response) or from `find_banner_alerts`. Use when the underlying clinical issue has been addressed (e.g., the overdue screening was completed) and the banner should no longer display.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `banner_key` | string | yes | The banner's key — exactly as returned by add_banner_alert (``banner_key`` in the response) or find_banner_alerts (``key`` in each row). |

**Returns:** `{ok: true}`.

**Backing Effect:** `RemoveBannerAlert`.

#### `create_task`

**Category:** `@task_writes`

Create a follow-up Task for the patient — appears in the clinician's task queue for them to act on later. Use for things the clinician should do but that can't be staged as a chart command (call patient, schedule follow-up visit, review external records). The task is not assigned to a specific user; team/assignee routing happens via the instance's task triage rules. Title is truncated to 200 chars. Returns the generated task_id so it can be referenced later.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Plain-text task title (truncated to 200 chars). |

**Returns:** `{ok: true, task_id: <uuid>}` — pass `task_id` to `update_task` or `add_task_comment` to close or annotate the task later.

**Backing Effect:** `AddTask`.

#### `update_task`

**Category:** `@task_writes`

Update an existing task — typically to close it (status=COMPLETED), reopen it (status=OPEN), or change its title/due. The task_id must come from a prior `find_tasks` or `create_task` call; this tool does not look tasks up by content. Title is truncated to 200 chars. Only the fields you supply are updated; omitted fields are left as-is.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `task_id` | string | yes | The task's UUID — from a prior find_tasks/create_task call. |
| `status` | string (enum) | no | New status. 'COMPLETED' marks the task done, 'CLOSED' dismisses it without completion, 'OPEN' reopens. Optional — omit to leave status unchanged. One of: `COMPLETED`, `CLOSED`, `OPEN`. |
| `title` | string | no | Updated task title (truncated to 200 chars). Optional. |
| `due_on` | string (date) | no | Updated due date (ISO 8601 YYYY-MM-DD). Optional. |

**Returns:** `{ok: true}`.

**Backing Effect:** `UpdateTask`.

#### `add_task_comment`

**Category:** `@task_writes`

Add a comment to an existing task — use to explain *why* a task was created/closed or to add context the clinician should see when they pick up the task. The task_id must come from a prior find_tasks or create_task call.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `task_id` | string | yes | The task's UUID — from a prior find_tasks/create_task call. |
| `body` | string | yes | The comment text. Plain text; no markdown. |

**Returns:** `{ok: true}`.

**Backing Effect:** `AddTaskComment`.

#### `add_or_update_protocol_card`

**Category:** `@clinical_alerts`

Stage or update a protocol card on the patient — a clinical decision support surface with title, narrative, and a list of recommended actions the clinician can take. Pass `card_key` to update an existing card (idempotent — call again to refresh narrative/status as the underlying clinical picture changes); omit to create a new one. Status drives visual treatment: 'due' (needs action), 'satisfied' (done), 'not_applicable' (doesn't apply to this patient), 'pending' (in progress), 'not_relevant' (dismissed). Title and narrative are truncated to 200 and 500 chars respectively. Returns the card_key so the same card can be updated later.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Short card title — what the clinician sees first. Truncated to 200 chars. E.g. 'Diabetes management — A1c overdue'. |
| `narrative` | string | yes | Body text explaining the clinical context and why this is surfacing now. Truncated to 500 chars. |
| `status` | string (enum) | no | Card lifecycle status. Defaults to 'due' if omitted. One of: `due`, `satisfied`, `not_applicable`, `pending`, `not_relevant`. |
| `card_key` | string | no | Stable key identifying the card. Supply the key from a prior call to update that card; omit to create a new one (a UUID is generated). |
| `recommendations` | array of object | no | Optional recommended actions surfaced beneath the card. Each is an object with `title` (required, what the action is), optional `button` (call-to-action text), optional `href` (link the button opens), and optional `commands` — a list of chart commands the button stages on the open note when clicked. When the clinician clicks the button, the platform stages each originated command as a draft for the clinician to review, edit, and commit. |
| `due_in` | integer | no | Days from now until the card is 'due' — drives the 'Next due' text the clinician sees on the card. Use positive integers (e.g., 90 for 'recheck in 3 months'). Default -1 means no specific due date. |
| `can_be_snoozed` | boolean | no | When true, the chart UI shows a snooze affordance on the card so the clinician can temporarily hide it without marking it satisfied. Recommended for cross-visit follow-up cards. Default false. |
| `feedback_enabled` | boolean | no | When true, the chart UI surfaces a feedback affordance on the card — typically a dismiss / 'not relevant' control. Recommended for agent-generated cards so the clinician has a way to push back when the recommendation doesn't apply. Default false. |

**Returns:** `{ok: true, card_key: <uuid>}` — pass `card_key` back to update the same card on a subsequent run.

**Backing Effect:** `ProtocolCard`.

#### `originate_plan`

**Category:** `@clinical_writes`

Stage a draft Plan command on the patient's current open note for the clinician to review, edit, and commit. NEVER commits — the clinician sees the draft in the chart and decides whether to keep it. Use when the conversation has produced a concise plan paragraph worth surfacing on the note.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `narrative` | string | yes | The plan text. Plain prose; no markdown. Keep it concise — this becomes the body of the Plan command on the note. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `PlanCommand`.

#### `originate_prescribe_medication`

**Category:** `@clinical_writes`

Stage a draft Prescribe command on the patient's current open note for the clinician to review, edit, and commit. NEVER commits — the clinician sees the draft in the chart and decides whether to send it. Use only when the clinician explicitly asks to prescribe.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `fdb_code` | string | no | FDB code identifying the medication. If unknown, omit; the clinician will fill it in when reviewing the draft. |
| `sig` | string | yes | Patient instructions (e.g. 'Take 1 tablet by mouth daily'). |
| `indications_icd10` | array of string | no | ICD-10 codes justifying the prescription (max 2). Optional. |
| `days_supply` | integer | no | Days supply for the prescription. Optional. |
| `refills` | integer | no | Refills (0 = no refills). Optional. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `PrescribeCommand`.

#### `originate_lab_order`

**Category:** `@clinical_writes`

Stage a draft Lab Order command on the patient's current open note for the clinician to review and commit. NEVER commits. Use when the clinician asks to order labs.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `tests_order_codes` | array of string | yes | Order codes for the tests to include. At least one required. |
| `diagnosis_codes` | array of string | no | ICD-10 codes for diagnoses justifying the order. |
| `lab_partner` | string | no | Lab partner UUID or name. Optional; the clinician can fill it in when reviewing. |
| `comment` | string | no | Optional free-text instructions to the lab. |
| `fasting_required` | boolean | no | Whether the patient needs to fast before collection. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `LabOrderCommand`.

#### `originate_diagnose_condition`

**Category:** `@clinical_writes`

Stage a draft Diagnose command on the patient's current open note for the clinician to review and commit. NEVER commits. Use when the clinician wants to capture a new diagnosis.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `icd10_code` | string | yes | ICD-10 code for the condition (e.g. 'E11.9'). |
| `today_assessment` | string | no | Today's assessment narrative for this diagnosis. |
| `background` | string | no | Optional background/context for the diagnosis. |
| `approximate_date_of_onset` | string (date) | no | ISO 8601 date of approximate onset. Optional. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `DiagnoseCommand`.

#### `originate_goal`

**Category:** `@clinical_writes`

Stage a draft Goal command on the patient's current open note for the clinician to review and commit. NEVER commits. Use to capture a discrete clinical goal (e.g., 'A1c < 7.0 within 6 months', 'walking 30 minutes 5x/week'). The narrative goes in goal_statement.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `goal_statement` | string | yes | Plain-text statement of the goal. |
| `priority` | string (enum) | no | Goal priority. Optional. One of: `high-priority`, `medium-priority`, `low-priority`. |
| `achievement_status` | string (enum) | no | Current achievement status. Default 'in-progress' if omitted. One of: `in-progress`, `improving`, `worsening`, `no-change`, `achieved`, `sustaining`, `not-achieved`, `no-progress`, `not-attainable`. |
| `due_date` | string (date) | no | ISO 8601 target date for the goal. Optional. |
| `progress` | string | no | Optional free-text note about current progress. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `GoalCommand`.

#### `originate_assessment`

**Category:** `@clinical_writes`

Stage a draft Assess command on the patient's current open note — the clinician's assessment of one of the patient's existing conditions ('how is this condition doing today'). NEVER commits. Requires the condition_id from a prior `find_conditions` call.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `condition_id` | string | yes | UUID of the condition being assessed — from a prior find_conditions call (the row's `id` field). |
| `status` | string (enum) | no | Status of the condition today relative to its prior state. One of: `improved`, `stable`, `deteriorated`. |
| `narrative` | string | no | Today's assessment narrative for this condition. |
| `background` | string | no | Optional background/context. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `AssessCommand`.

#### `originate_follow_up`

**Category:** `@clinical_writes`

Stage a draft Follow-Up command on the patient's current open note to schedule a return visit. NEVER commits. Use when the clinician wants to plan a follow-up appointment (e.g., 'recheck in 2 weeks').

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `requested_date` | string (date) | no | ISO 8601 target date for the follow-up. |
| `comment` | string | no | Free-text reason for the follow-up (visible to scheduling). E.g., 'recheck BP after med adjustment'. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `FollowUpCommand`.

#### `originate_stop_medication`

**Category:** `@clinical_writes`

Stage a draft Stop-Medication command on the patient's current open note to discontinue an active medication. NEVER commits. Requires medication_id from a prior `find_medications` call. Use when the clinician decides to stop a med (side effects, ineffective, completed course).

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `medication_id` | string | yes | UUID of the medication to stop — from a prior find_medications call (the row's `id` field). |
| `rationale` | string | no | Reason for stopping (e.g., 'side effects', 'completed course', 'ineffective'). Visible to anyone reviewing the chart. |

**Returns:** `{ok: true, note_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit.

**Backing Command:** `StopMedicationCommand`.

#### `originate_message`

**Category:** `@message_writes`

Stage a draft message from the requesting staff to this patient for the staff to review, edit, and send. NEVER sends — drafts land in the staff's outbox; the clinician hits Send. Use when the clinician explicitly asks to reply to or message the patient (e.g., 'draft a reply about her A1c', 'message the patient about their lab results'). Pull recent inbound messages via `find_messages(from_patient_only=true)` first so the draft reflects the actual conversation. Keep drafts patient-readable: plain English, short sentences, no jargon unless the clinician asked for a technical tone.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `content` | string | yes | The message body the patient will read. Plain text only — no markdown headings or HTML. Address the patient directly. Sign off as the staff member if appropriate; the patient sees the sender's name on the message header either way. |

**Returns:** `{ok: true, status: 'draft'}`. The draft sits unsent in the staff's outbox; the clinician reviews and decides whether to send.

**Backing Effect:** `Message`.
<!-- AUTOGEN:writes END -->
