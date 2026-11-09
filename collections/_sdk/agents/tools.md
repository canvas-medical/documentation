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
permission filter: the plugin's manifest (not the agent itself)
declares which tools any given agent can use.

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
`run()`. The platform applies the emitted effects through
`handle_effect` in order *after* the run completes — the model
decides *what* to emit; the platform decides *when*. An effect that
fails stops the rest, and the effects before it stay applied. Effect tools
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
    returns_description="Array of objects with `id`, `code`, `display`, `onset_date`.",
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
    name="originate_prescription_draft",
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
  differently). Patient scope flows through the Command. The tool
  refuses a command type the instance has turned off, as the chart's
  command menu leaves it out.
- **`add_effect_tool`** — patient-scoped Effects that aren't pinned
  to a specific note (tasks, banner alerts, protocol cards). Auto-
  injects `patient_id` from ctx onto the Effect; `inject_ctx={}` to
  opt out (e.g., for `update_task`, which is identified by `task_id`).
  A tool that takes a record id from the model should check the record
  belongs to `ctx["patient_id"]` in `pre_build` and raise otherwise, as
  the SDK's task, assessment, and stop-medication tools do.

Neither helper accepts a field that would set what the run supplies: a
field named, or mapped with `command_field`, onto an injected kwarg
(`patient_id` by default for `add_effect_tool`, the note for
`originate_command_tool`) raises `ValueError` when the tool is
registered.

Both write helpers record the effect type they stage, which is what
lets granting the tool let the agent return that effect (see
[Permissions](#manifest-driven-permissions)).

### Escape hatch: `@tools.tool`

For tools that don't fit any of the three helper shapes — scalar
reads that return a fixed-shape object, custom workflows that span
multiple Effects, integrations with non-Canvas APIs — drop down to
the raw decorator and hand-build the executor:

```python?partial=true
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

A raw tool that stages effects must declare their types with
`effect_types`, for example `effect_types=("CREATE_TASK",)`. An agent
can return only the effect types its granted tools declare, so an
undeclared effect is dropped. An unknown name fails at import.

## Executor signature

The helpers generate executors with this signature behind the scenes;
you only write one directly when using the raw `@tools.tool`
decorator. Either way, every executor takes the same two arguments:

```python
from typing import Any


def my_tool(arguments: dict, *, ctx: dict) -> Any: ...
```

- `arguments` — the model's `tool_use.input` dict. The model chose
  these values from the input schema. Validate as needed before use.
- `ctx` — the platform's per-run context, built from the run's subject.
  The model never sees this. Its keys:
  - `patient_id` — string UUID of the patient the run is about, checked
    by the platform. `None` for a run that isn't about a patient; read it
    with `require_patient_id(ctx)` in a tool that needs one, so the model
    gets an error rather than an empty result.
  - `note_id` — the note the run is about, or for a run a staff member
    started, that staff member's open note on the patient.
  - `staff_id` — the staff member whose action started the run. Message
    drafts are attributed to them. `None` for a run nobody on staff
    started.
  - `effects` — the list to append staged Effects to (used by effect tools).
  - `gateway`, `parent_tools` — the run's gateway and the agent's granted
    tools, for tools that run sub-agents or make a model call of their own,
    as the standard `read_document` does. `edit_staged_command` and
    `delete_staged_command` read `parent_tools` to check the grant, and
    refuse without it.
  - Any agent-specific keys the agent passed to `run_tool_loop(ctx=...)`.

Use `ctx` for anything the model shouldn't choose — patient scoping,
note targeting, the effects accumulator. Never trust `arguments` for
scope (a malicious or hallucinating model could try to switch
patients via an argument). The SDK's `standard_tools` enforce scope
this way: `find_medications` reads `ctx["patient_id"]` and filters
the query on it regardless of what the model passes. An agent's
`run_tool_loop` can't replace `patient_id`, `staff_id`, or `note_id`, so
in the tool loop that filter is the patient the platform checked. That
bounds the model, not plugin code: code that calls a tool through
`self.tools.execute(..., ctx={...})` or the `run_tool_loop` function
chooses its own context. The platform's check on the run's effects is
the authoritative layer, and reads have no such check.

## Attaching tools to an agent

Declare the registry as a class attribute on your `AgentPlugin`
subclass:

```python?partial=true
from my_plugin.agents.advisor_tools import tools as _registered_tools

class LongitudinalCareAdvisor(AgentPlugin):
    tools = _registered_tools

    def run(self, state, gateway, trigger_payload):
        # run_tool_loop offers the model self.tools, the manifest-scoped view,
        # and runs each tool call it makes with the run's ctx.
        result = self.run_tool_loop(gateway, system=SYSTEM_PROMPT, messages=messages)
        return AgentRunResult(state=state, effects=result.effects)
```

Inside `run()`, always use `self.tools` — that's the platform-scoped
view (see [Permissions](#manifest-driven-permissions)).
`self.run_tool_loop` uses it for you; see
[Lifecycle](/sdk/agents-lifecycle/#running-the-model-with-run_tool_loop). The
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

`run_tool_loop` dispatches tool calls for you. If you call the model
yourself, build the context once with `self.tool_context(gateway)` and
dispatch each `ToolUseBlock` through the registry the same way it does:

```python?partial=true
import json

tool_ctx = self.tool_context(gateway)  # once per run, before the first tool call

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
different tool). A call that raises keeps none of the effects it
staged before raising, so a retry never duplicates them. A tool built
for the run's patient raises in a run that is not about one.

`run_tool_loop` also handles a turn cut off by `max_tokens`: the tool
calls before the last run, and the last, where generation stopped and
whose input may be incomplete, is answered with an error asking the
model to make it again.

## Sub-agents

A tool can fan out to focused sub-agents, each with its own persona,
a subset of the agent's granted tools, and its own turn limit, and
return what they found. `run_subagent` runs one; `run_subagents` runs
several at once and returns `{spec.name: final_text}`:

```python?partial=true
from canvas_sdk.agents import SubAgentSpec, run_subagents

SPECS = [
    SubAgentSpec(
        name="labs",
        system_prompt="Summarize the patient's lab trends in two sentences.",
        allowed_tool_names=frozenset({"find_lab_results"}),
    ),
    SubAgentSpec(
        name="medications",
        system_prompt="List the patient's active medications and recent changes.",
        allowed_tool_names=frozenset({"find_medications", "find_prescriptions"}),
    ),
]


@tools.tool(name="chart_overview", description="...", input_schema={"type": "object"})
def chart_overview(arguments, *, ctx):
    return run_subagents(
        SPECS,
        "Review this patient's chart.",
        parent_tools=ctx["parent_tools"],
        parent_ctx=ctx,
        gateway=ctx["gateway"],
    )
```

- A sub-agent's tools are its `allowed_tool_names` intersected with the
  agent's grant, and keep the grant's approval, so fanning out never
  widens what the agent may do.
- Effects a sub-agent's tools stage go into the run's effects, like the
  agent's own.
- Every sub-agent's model calls count toward the run's
  `max_model_calls`, and the run's deadline applies to them.
- `run_subagents` runs at most `max_parallel` (default 4, at most 8)
  at once. A sub-agent that fails returns a `"(sub-agent ... failed:
  ...)"` string; a gateway error or the run's deadline ends the run.
- A sub-agent that stops before ending its turn returns `""`. Its text
  is for the parent, so none of it streams to the person waiting.

## Result size

`run_tool_loop` sends the model at most 50,000 characters of one tool's
result and cuts the rest, with a note saying so. A tool whose answer
cannot be split, such as one patient's full set of outside records, can
register a larger limit with `max_result_chars`, on `@tools.tool` or
`filter_search_tool`, up to 200,000:

```python?partial=true
@tools.tool(
    name="get_outside_records",
    description="Every outside record on file for the patient, with its codes.",
    input_schema={"type": "object", "properties": {}},
    categories=("clinical_reads",),
    max_result_chars=200_000,
)
def get_outside_records(arguments, *, ctx):
    ...
```

A limit above 200,000 raises `ValueError` when the tool registers, so
`canvas validate` reports it before install. Every result stays in the
conversation and is sent again on each later model call, so a larger
limit costs input tokens for the rest of the run; prefer filters or a
lower `limit` when the model rarely needs everything. In a platform
run, the results of all tool calls, sub-agents included, add up to at
most 600,000 characters, and a result past that is cut with a note
telling the model to answer from what it has.

## Progress labels

For an agent whose manifest sets `progress` to `activity` or `reply`, the
person waiting on a run sees a label as each tool starts and finishes (see
[Showing a run's progress](/sdk/agents-lifecycle/#showing-a-runs-progress)).
Give a tool its label with `progress_label`, on `@tools.tool` or
`filter_search_tool`, naming what it does and never its arguments:

```python?partial=true
@tools.tool(
    name="get_outside_records",
    description="Every outside record on file for the patient, with its codes.",
    input_schema={"type": "object", "properties": {}},
    progress_label="Reading outside records",
)
def get_outside_records(arguments, *, ctx):
    ...
```

`tools.set_progress_labels({...})` labels tools registered through a helper
that takes no `progress_label`, such as `originate_command_tool`. It raises
`ValueError` for a name that isn't a registered tool. A tool without a label
shows `Looking something up`, and every tool in `standard_tools` has one.

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

1. Reads `tools.allowed` and `tools.denied` from the manifest entry
   for this agent.
2. Resolves them with `ToolRegistry.resolve_allowed`: tool names and
   `@category` groups in `tools.allowed` expand against the agent's
   registry, `tools.denied` is subtracted, and unknown names resolve
   to nothing. The result becomes `self.tools_allowed`.
3. Replaces `self.tools` with a *scoped* registry containing only
   those tools — disallowed entries aren't in the registry at all.
4. Marks the granted tools named in `tools.approve` (names and
   `@category` groups, resolved the same way) to
   [propose their changes](/sdk/agents-lifecycle/#approve-before-write)
   for the requester to approve instead of making them. Approval covers
   the change, not just the tool: any other granted tool that stages an
   effect type a listed tool stages proposes too.
5. After `run()` returns, drops any effect the agent returned whose
   type no granted tool stages. An effect type that only tools in
   `tools.approve` stage is kept only when it's wrapped in a proposal.

An agent entry with no `tools.allowed` gets no tools, and so can
return no effects.

The standard `edit_staged_command` and `delete_staged_command` tools
also check the grant, so an agent can't change a draft it couldn't
have staged. They change a kind of command only when the agent is
granted an `originate_*` tool that stages it. When that originate tool
is in `tools.approve`, they must be too, or they refuse. Two exceptions
apply today: they refuse to edit or delete imaging order, referral,
reason for visit, and HPI drafts, and when they are in `tools.approve`,
they can't see drafts the same run staged, so they change only drafts
already in the note.

After step 3, `self.tools.definitions()` returns only the allowlisted
subset (the model never sees the others) and
`self.tools.execute("disallowed_name", ...)` raises `ValueError`
because the executor isn't reachable. There's no per-call `allowed=`
parameter to remember — the registry itself is pre-filtered.

**Why this matters**: the manifest is the single source of truth for
the effects an agent can return. Someone reviewing your plugin can read
the manifest and know which tools each agent has and which of their
changes need approval. Step 5 holds even for agent code that
builds an effect directly or calls the imported, unscoped registry:
an agent granted only `@clinical_reads` and `@clinical_alerts` can
stage protocol cards and banners, but any task, command, or message it
returns is dropped.

The grant doesn't bound everything a tool does:

- A tool can write your Custom Data directly (see
  [Writing Custom Data](#writing-custom-data)) and make outbound
  `Http` calls. Neither is an effect, so neither is filtered.
- What a granted tool does depends on the requester: their
  permissions decide which tools are offered and which effects apply,
  and a Canvas Bot or superuser run isn't limited by permissions.

## Citing what the tools read

A reply can cite the chart records it draws on, so a user can check each
statement against the record behind it. The model writes `[[cite:<id>]]`
after a statement, with the `id` of a row a read tool returned; add
`CITATION_GUIDANCE` to your system prompt to ask for that.
`canvas_sdk.agents.citations` turns the markers into numbered references:

- `Sources(tools)` collects, from a conversation's stored messages, every
  row a citable tool returned. Add the messages in order with `add` or
  `add_all`.
- `cite(text, sources)` replaces each marker with `[1]`, `[2]`, … and
  returns a `Citation` per cited record. A marker whose id no citable tool
  returned is removed, so a citation is always a row a tool read.
- A `Citation` (`to_dict()` for JSON) describes the record from that row:
  `kind` (such as "Lab result"), `label`, `detail`, `date`, and a
  `note_dbid` for a note, or for a record whose row names the note it was
  made on (such as an order from `find_open_loops`), which a chart surface
  can navigate to. It never carries text the model wrote.

```python?partial=true
from canvas_sdk.agents.citations import Sources, cite

sources = Sources(tools)
for message in conversation:
    if message["role"] == "assistant":
        text, citations = cite(reply_text(message), sources)
        render(text, [citation.to_dict() for citation in citations])
    sources.add(message)
```

A tool registered with `filter_search_tool(model=...)` is citable, keyed by
the `id` in each row it returns. Pass `citable=False` for a tool that reads
configuration rather than the patient's records, as the standard
`find_note_types`, `find_practice_locations`, `find_lab_partners`, and
`find_lab_partner_tests` do. A tool registered with `@tools.tool` is citable
when it passes `cites="<record type>"`, which names its rows' record type;
the standard `find_open_loops` cites its rows as `"OpenLoop"`,
`find_documents` as `"Document"`, `find_history` as `"History"`, and
`find_pharmacy_requests` as `"PharmacyRequest"`.

## Reading your plugin's Custom Data

An agent runs with its plugin's [Custom Data](/sdk/custom-data/)
namespace and the access its manifest declares, as a handler does, so a
tool can read your plugin's own tables. A `filter_search_tool` over a
`CustomModel` is the usual shape:

```python?partial=true
from canvas_sdk.agents import FilterSpec, ToolRegistry
from my_plugin.models import OutreachAttempt

tools = ToolRegistry()


@tools.filter_search_tool(
    name="find_outreach_attempts",
    description=(
        "Search this plugin's record of outreach to the patient: each call, "
        "text, or letter, when it was made, and whether the patient answered."
    ),
    queryset_factory=lambda args, pid: OutreachAttempt.objects.filter(patient__id=pid),
    filters={
        "channel": FilterSpec(
            type="string",
            description="Only attempts on this channel.",
            enum=["call", "text", "letter"],
            apply=lambda qs, v: qs.filter(channel=v),
        ),
    },
    ordering=("-attempted_at",),
    model=OutreachAttempt,
    returns_description="Array of objects with `id`, `channel`, `attempted_at`, `answered`.",
    progress_label="Reading outreach attempts",
)
def _serialize_attempt(attempt):
    return {
        "id": str(attempt.dbid),
        "channel": attempt.channel,
        "attempted_at": attempt.attempted_at.isoformat(),
        "answered": attempt.answered,
    }
```

The SDK scopes its own tools to the run's patient; a tool over your
tables is scoped only by the query you write:

- **Filter by the run's patient.** `queryset_factory` receives the run's
  patient as `pid`; filter on it through the model's `PatientProxy`
  foreign key, and never take a patient from the model's arguments. A
  row id the model passes is untrusted too: check it belongs to the
  patient before using it.
- **Keep to what the requester can see.** The platform checks that the
  requester can see the run's patient, but it does not know which rows
  of a table that spans many patients, such as a work queue, belong to
  patients outside the requester's patient groups. A tool over such a
  table must apply that boundary itself, or stay patient-scoped.
- **Treat stored text as data.** Text in your tables that came from a
  patient or an outside system reaches the model as data, as documents
  and messages do.

A `filter_search_tool` with `model=` is citable, so a reply can cite
your rows as it cites chart records. A citation finds its row by `id`
alone, and a `dbid` repeats across tables: when rows of two of your
tables share an `id`, neither can be cited. To cite rows from more than
one table, make their ids unique, for example by prefixing the table
(`f"outreach-{attempt.dbid}"`).

### Writing Custom Data

A tool that saves a `CustomModel` writes to the database directly. Every
control on an agent's writes works on the effects it returns, so none
of them applies to that write:

- The tool grant bounds the effects an agent can return, not what a tool
  writes.
- The requester's permissions are checked against effects, not against
  your tables.
- `tools.approve` turns the effects each tool call stages into one proposal. A tool
  that stages no effect returns its own result, so a tool listed there
  that saves a row saves it at once.
- A run that fails or runs out of time has its effects dropped and its
  state left unsaved, but a row a tool already saved stays. A run the
  platform retries after a gateway outage runs its tools again.

Write your tables in `save_state`, which runs only after `run()` returns
in time, from what the run decided. When a tool must write as the run
goes, keep the write to your plugin's own bookkeeping and make it
idempotent. Anything a person should approve, or that changes the chart,
belongs in an effect.

## Incoming documents

An agent can work an incoming document, such as a fax just received, before
anyone files it. A handler on `DOCUMENT_RECEIVED` starts the run about that
document:

```python?partial=true
from canvas_sdk.effects.agent import RunAgentEffect

RunAgentEffect(
    agent_id="my_plugin.agents.intake:IntakeAgent",
    scope=RunAgentEffect.Scope.DOCUMENT,
    document_id=self.event.target.id,
).apply()
```

The platform checks the document is in the data integration queue and hands
it to the intake tools as `ctx["document_id"]`. Grant them with
`@intake_reads` and `@intake_writes`:

- `read_incoming_document` answers a question from the document's file, and
  `find_document_types` and `find_report_templates` list what it can be filed
  as.
- `match_patient` and `suggest_patient` take the name, birth date, and MRN as
  the document gives them and match them in code. The MRN can be Canvas's or
  one an outside organization keeps for the patient, such as the sending lab's.
  A patient is suggested only when exactly one matches. Canvas's MRN counts
  only with the last name or birth date agreeing, and another organization's
  only when it is a current medical record number and both agree. The model is
  told a patient's id, never their details.
- On a scan or fax, the model also passes each identifier `as_printed`,
  exactly as the page shows it, with the `legibility`, `handwritten`, and
  `pages_disagree`. The code then refuses identifiers marked illegible or
  handwritten, pages that disagree, and any value passed that the print does
  not support, such as a birth date read day-first. It checks only the
  identifiers the model passes, and a name agrees when every word read is
  printed. So a suggestion can still name a patient when the model leaves out
  a printed MRN that belongs to someone else, reads only part of a printed
  name, or passes no first name. Have a person confirm every suggested
  patient. When the identifiers as read match no one, it
  tries the readings a fax misread (0/O, 1/I/l, 5/S, 8/B; never the birth
  date), a dropped middle initial, or a first/last swap would explain, and
  suggests a patient only when every reading that matches names that one,
  labeled for the reviewer to check. With more readings than it can check, it
  names no one.
- `suggest_patient`, `categorize_document`, `prefill_document_fields`, and
  `assign_document_reviewer` suggest on the document's review form. They file
  nothing: a person confirms each suggestion in Canvas, and the review stays
  required. Each suggestion is labeled "AI suggested" on the form. The patient,
  type, and value suggestions also show a confidence level: for the patient,
  high when three of Canvas's own identifiers the model passed agree and
  medium otherwise, whatever else the page prints; for
  the type and the values, the confidence the model passes, when it passes one.

Every intake tool needs `api.access_dataintegration`, the queue's permission.
A staff member starting a run about a document also has to see every patient,
since matching searches every patient.

## Scheduling

`@scheduling_reads` lists the practice's providers (`find_providers`) and
searches open times the way the native booking screens do
(`find_appointment_slots`, with time-zone-aware start and end at most 31 days
apart). A slot is not held, so book soon after finding it.

`@scheduling_writes` books, reschedules, and cancels the run's patient's
appointments. Each refuses an appointment that is not the run's patient's, and
each takes effect when applied rather than staying a draft. The platform does
not require approval for them: without `tools.approve`, a booking, reschedule,
or cancel applies when the run ends. List `@scheduling_writes` under
`tools.approve` for an agent that offers them to a person. For a
run a staff member started, each needs what the chart checks: `add_appointment`
to book or reschedule, and `change_appointment` with
`add_notestatechangeevent` to cancel.

`find_patient` (`@patient_search`) names the one patient a set of identifiers
matches, for an agent that works for whoever a person asks about. It needs the
`PATIENT_SEARCH` capability. Every other tool still acts only on the run's
patient: a patient the search names is for the agent to tell the person, or to
start a run about.

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
- **Check record ids the model supplies.** The model reads chart text,
  including patient-written messages, so treat an id it passes (a task,
  a condition, a medication) as untrusted and confirm it belongs to
  `ctx["patient_id"]` before staging anything.
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

A tool listed below as offered only to runs with a permission is
offered to every Canvas Bot and superuser run, since permissions don't
limit those runs; a capability limits every run.

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
- **`@claims_reads`** (6 tools): `find_claims`, `get_claim`, `summarize_claims`, `find_claim_queues`, `find_claim_labels`, `find_claim_assignees`
- **`@claims_writes`** (8 tools): `move_claim_to_queue`, `assign_claim`, `unassign_claim`, `add_claim_labels`, `remove_claim_labels`, `add_claim_comment`, `add_claim_banner`, `remove_claim_banner`
- **`@clinical_alerts`** (3 tools): `add_banner_alert`, `remove_banner_alert`, `add_or_update_protocol_card`
- **`@clinical_reads`** (30 tools): `find_medications`, `find_conditions`, `find_lab_results`, `find_assessments`, `find_allergies`, `find_immunizations`, `find_vitals`, `find_appointments`, `find_encounters`, `find_notes`, `get_open_note`, `get_note_content`, `search_note_text`, `find_goals`, `find_imaging_reports`, `find_referrals`, `find_open_loops`, `find_documents`, `find_history`, `find_care_team_members`, `find_medication_statements`, `find_external_events`, `find_prescriptions`, `find_pharmacy_fills`, `find_pharmacy_requests`, `find_questionnaire_responses`, `find_stop_medication_events`, `find_banner_alerts`, `find_protocol_cards`, `get_patient_demographics`
- **`@clinical_writes`** (24 tools): `originate_plan`, `originate_prescribe_medication`, `originate_lab_order`, `originate_diagnose_condition`, `originate_goal`, `originate_assessment`, `originate_follow_up`, `originate_stop_medication`, `originate_review_note`, `originate_medical_history`, `originate_medication_statement`, `originate_allergy`, `originate_family_history`, `originate_surgical_history`, `originate_immunization_statement`, `originate_vitals`, `originate_resolve_condition`, `originate_remove_allergy`, `edit_staged_command`, `delete_staged_command`, `originate_imaging_order`, `originate_refer`, `originate_reason_for_visit`, `originate_hpi`
- **`@config_reads`** (7 tools): `find_note_types`, `find_practice_locations`, `find_lab_partners`, `find_lab_partner_tests`, `find_clinical_codes`, `find_service_providers`, `find_reason_for_visit_codes`
- **`@document_reads`** (1 tool): `read_document`
- **`@intake_reads`** (4 tools): `read_incoming_document`, `match_patient`, `find_document_types`, `find_report_templates`
- **`@intake_writes`** (4 tools): `suggest_patient`, `categorize_document`, `prefill_document_fields`, `assign_document_reviewer`
- **`@message_reads`** (1 tool): `find_messages`
- **`@message_writes`** (1 tool): `originate_message`
- **`@patient_search`** (1 tool): `find_patient`
- **`@scheduling_reads`** (2 tools): `find_providers`, `find_appointment_slots`
- **`@scheduling_writes`** (3 tools): `book_appointment`, `reschedule_appointment`, `cancel_appointment`
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

Search the patient's conditions with optional filters. Returns each matching condition with `code` (the first coding's identifier — typically ICD-10), `display`, `clinical_status` (active, resolved, remission, relapse, investigative), `onset_date` (ISO 8601 or null), and `resolution_date` (ISO 8601 or null). Defaults to active conditions only, ordered most-recently-onset first. Past surgeries are not conditions here: read them with `find_history`.

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

Search the patient's committed lab results. Returns each matching value with `test` (lab name), `value`, `units`, `abnormal_flag` (e.g. 'H', 'L', or null when normal), `reference_range` (as the lab reported it, or null), and `date` (the report's original_date, ISO 8601). Defaults to the 10 most-recent results.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the lab's coding name (e.g. 'a1c', 'hemoglobin'). |
| `observed_on_or_after` | string (date) | no | ISO 8601 date. Only return results with date >= this. |
| `abnormal_only` | boolean | no | When true, restrict to values with a non-empty abnormal_flag. Useful for spotting out-of-range results quickly. |
| `limit` | integer | no | Max results. Defaults to 10. |

**Returns:** Array of objects with `id`, `test`, `value`, `units`, `abnormal_flag` (e.g. 'H', 'L', or null), `reference_range`, `date`.

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

**Returns:** Array of objects with `id`, `display`, `code`, `date_administered`, `status`, `manufacturer`, `lot_number`.

**Backing data model:** `Immunization`.

#### `find_vitals`

**Category:** `@clinical_reads`

Search the patient's recorded vital signs — blood pressure, heart rate, temperature, weight, height, BMI, respiratory rate, oxygen saturation, and similar measurements (any Observation in the FHIR `vital-signs` category). Returns each measurement with `name`, `value`, `units`, `code` (typically LOINC from the first coding), and `date` (ISO 8601 effective_datetime). Patient scope is enforced. Defaults to the 10 most recent.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive match on the observation's name, treating spaces, underscores, and hyphens alike. Canvas records vitals under names such as 'blood_pressure', 'pulse', 'body_temperature', 'respiration_rate', 'oxygen_saturation', 'weight', and 'height'; 'blood pressure' matches 'blood_pressure'. |
| `observed_on_or_after` | string (date) | no | ISO 8601 date. Only return measurements with effective_datetime >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 10. |

**Returns:** Array of objects with `id`, `name`, `value`, `units`, `code`, `date` (ISO 8601).

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

**Returns:** Array of objects with `id`, `title`, `status`, `due` (ISO 8601), `task_type`.

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

**Returns:** Array of objects with `id`, `status`, `start_time` (ISO 8601), `duration_minutes`, `provider_name`, `description`.

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

**Returns:** Array of objects with `id`, `state` (new|locked|unlocked|...), `medium`, `start_time`, `end_time`.

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

Return metadata for the patient's current open note (the most-recent note in a mutable state — NEW, UNLOCKED, or CONVERTED), limited to the requesting clinician's notes when there is one. Use this when the user references 'this note' or 'the open note' and the agent needs the note_id to drill into it or stage a command on it. Returns the same row shape as one find_notes entry, or null if no open note exists.

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

#### `search_note_text`

**Category:** `@clinical_reads`

Find the patient's notes whose free text mentions the given words ('the note that mentions chest pain', 'when did we discuss sleep apnea'). Matches notes containing every word, in any order and any case, newest first, each with a snippet around the match. Searches only the narrative the clinician typed; structured commands are read with get_note_content. Use the row's `id` with get_note_content to read the whole note.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `text` | string | yes | Words to find, such as 'chest pain'. A note matches when it contains every word. |
| `limit` | integer | no | Maximum notes to return. Defaults to 10. |

**Returns:** Array of objects matching find_notes' row shape (`id`, `dbid`, `title`, `note_type`, `note_type_name`, `state`, `datetime_of_service`, `provider_name`) plus `snippet`, the note's text around the match. Empty when no note mentions every word.

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

**Returns:** Array of objects with `id`, `goal_statement`, `lifecycle_status`, `achievement_status`, `priority`, `start_date`, `due_date`, `progress`.

**Backing data model:** `Goal`.

#### `find_imaging_reports`

**Category:** `@clinical_reads`

Search the patient's imaging reports. Returns each report with `id`, `name` (test or modality, e.g., 'Chest X-ray'), `date` (when the study was done, ISO 8601 or null), `assigned_date` (ISO 8601 or null), `source` (e.g., 'internal', 'external'), `requires_signature` (bool), and `has_file`. What the radiologist found is in the report's file: read it with `read_document`. Patient scope is enforced and junked reports are excluded. Defaults to the 25 most-recent reports.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the report name (e.g., 'chest', 'mammo', 'mri'). |
| `assigned_on_or_after` | string (date) | no | ISO 8601 date. Only return reports with assigned_date >= this value. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, `date`, `assigned_date`, `source`, `requires_signature`, `has_file`.

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

**Returns:** Array of objects with `id`, `clinical_question`, `priority`, `notes`, `date_referred`, `service_provider_name`, `forwarded`.

**Backing data model:** `Referral`.

#### `find_open_loops`

**Category:** `@clinical_reads`

Reconcile the patient's lab orders, imaging orders, and referrals with what came back: for each order, whether its result (or a referral's consult report) arrived, whether anyone reviewed it, and how many days it has waited. Use it to answer 'did the labs come back', 'was the study done', 'did we get the consult report', and to brief a clinician on what is still open since a visit. Status is `awaiting_result`, `awaiting_review`, or `closed`; only open orders are returned unless include_closed is true. Newest orders first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `ordered_on_or_after` | string (date) | no | ISO 8601 date. Only orders placed on or after this date; pass the last visit's date of service for 'since the last visit'. Defaults to 180 days ago. |
| `include_closed` | boolean | no | When true, also return orders already resulted and reviewed. |

**Returns:** Array of objects with `id` (the order or referral), `type` (Lab order, Imaging order, Referral), `item`, `ordered_on`, `ordered_by`, `status` (awaiting_result|awaiting_review|closed), `resulted_on`, `days_waiting`, `summary`, `note_dbid` (the note it was ordered on), plus `pending_tests` for lab orders and `clinical_question` for referrals.

#### `find_documents`

**Category:** `@clinical_reads`

List consult reports (letters and visit notes specialists send back, filed on the chart) and outside records (documents from other providers) for the patient, newest first. Each has its specialty or name, dates, review status, a short staff comment made when it was filed, and whether a file is attached. What a document says is only in its file: read it with `read_document`. Use this for 'did the cardiology report come in', 'what outside records do we have', and to find a document to read.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `kind` | string (enum) | no | Only consult reports or only outside records. Omit for both. One of: `consult_report`, `outside_record`. |
| `name_contains` | string | no | Case-insensitive match on the specialty or document name, category, or staff comment (e.g. 'cardiology', 'echo', 'discharge'). |
| `dated_on_or_after` | string (date) | no | ISO 8601 date. Only documents dated on or after it. |
| `unreviewed_only` | boolean | no | When true, only documents nobody has finished reviewing. |
| `limit` | integer | no | Maximum documents of each kind. Defaults to 15. |

**Returns:** Array of objects with `id`, `type` (Consult report, Outside record), `name`, `date`, `received`, `review` (reviewed|in review|not reviewed), `comment`, and `has_file`; consult reports add `from`, `referral_id`, and `note_dbid` (the review note); outside records add `category`.

#### `find_history`

**Category:** `@clinical_reads`

Search the patient's history: past surgeries (`surgical`), conditions in their relatives (`family`), vaccines recorded as given elsewhere (`immunization`; `find_immunizations` has those given at the practice), and procedures done at the practice (`procedure`). Use it for 'has she had her gallbladder out', 'any family history of colon cancer', 'when was her last tetanus shot'. Each entry has its name, a date where one was recorded, and the note it was recorded in.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `kind` | string (enum) | no | Only one kind of history. Omit for all four. One of: `surgical`, `family`, `immunization`, `procedure`. |
| `name_contains` | string | no | Case-insensitive match on the surgery, condition, vaccine, or procedure name (e.g. 'cholecystectomy', 'colon', 'tetanus'). |
| `limit` | integer | no | Maximum entries of each kind. Defaults to 25. |

**Returns:** Array of objects with `id`, `type` (Surgical history, Family history, Immunization history, Procedure), `name`, `note_dbid`, and `comment`; surgeries add `date` (when it was done), family history adds `relation`, immunizations add `date` and `evidence`, and procedures add `date`, `status`, and `provider`.

#### `read_document`

**Category:** `@document_reads`

Read a document's attached file and answer a question from it, with page numbers. Use it when the answer is in what the document says, e.g. 'what did cardiology recommend', 'what did the MRI show', or 'what did the discharge summary say about her medications'. Takes the `id` of a consult report or outside record from `find_documents`, or of an imaging report from `find_imaging_reports`, that `has_file`. Reads the whole file with a separate model call, so it is slow and costly: ask one focused question, and do not call it for every document.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `document_id` | string | yes | The `id` of a document from `find_documents` or an imaging report from `find_imaging_reports`. |
| `question` | string | yes | What to find in the document, in the clinician's words. |

**Returns:** Object with `ok`, `document_id`, `name`, `answer` (the answer, with page numbers), and `note`; `ok: false` with `error` when the document has no readable file.

#### `find_care_team_members`

**Category:** `@clinical_reads`

Return the staff members on the patient's care team. Each result has `staff_name`, `role_display` (e.g., 'Primary Care Provider', 'Care Manager'), `role_code`, `status` (e.g., 'active', 'inactive'), and `is_lead` (true for the patient's primary contact). Ordered with the lead member first, then by role.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `role_contains` | string | no | Case-insensitive substring match on role_display (e.g., 'primary', 'manager'). |
| `status` | string (enum) | no | Filter to a specific CareTeamMembershipStatus value (e.g., 'active', 'inactive', 'suspended', 'proposed'). One of: `proposed`, `active`, `suspended`, `inactive`, `entered-in-error`. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `staff_name`, `role_display`, `role_code`, `status`, `is_lead`.

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

**Returns:** Array of objects with `id`, `medication_name`, `start_date`, `end_date`, `dose_form`, `dose_route`, `dose_frequency_interval`, `sig_original_input`.

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

Search the prescriptions written for the patient here (actual Rx events, distinct from `find_medications`, which is the medication list, and from `find_pharmacy_fills`, which is what pharmacies dispensed). Each result has `medication_name`, `status` (where the prescription stands on its way to the pharmacy), `written_date`, `dispensed_date`, `end_date`, `sig_original_input`, `dispense_quantity`, `days_supply`, `refills` (refills allowed), `pharmacy`, `prescriber`, `dose_form`, `dose_route`, `dose_frequency_interval`, `is_refill`, `response` (set when the prescription answers a pharmacy's refill request: Approved, Denied, ...), and `error` (why sending failed, when `status` is error). Patient scope is enforced. Defaults to committed prescriptions ordered most-recent first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the medication's first-coding display. |
| `status` | string (enum) | no | Only prescriptions with this status: e.g. 'error' for prescriptions the pharmacy never received, 'delivered' for those it did. One of: `open`, `pending`, `ultimately-accepted`, `error`, `cancel-requested`, `canceled`, `cancel-denied`, `received`, `signed`, `inqueue`, `transmitted`, `delivered`. |
| `written_on_or_after` | string (date) | no | ISO 8601 date. Only return prescriptions with written_date >= this. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `medication_name`, `status`, `written_date`, `dispensed_date`, `end_date`, `sig_original_input`, `dispense_quantity`, `days_supply`, `refills`, `pharmacy`, `prescriber`, `dose_form`, `dose_route`, `dose_frequency_interval`, `is_refill`, `response`, `error`, `note_dbid`.

**Backing data model:** `Prescription`.

#### `find_pharmacy_fills`

**Category:** `@clinical_reads`

Search what pharmacies dispensed to the patient, from the pharmacy network's medication history: whatever prescriber wrote it, here or elsewhere. Use it for 'is she filling her statin', 'when did he last pick up his inhaler', or 'who else prescribes for this patient'. Each fill has `drug`, `last_fill_date`, `days_supply`, `supply_ends` (last fill plus days supply), `quantity`, `refills_remaining`, `fill_number`, `sig`, `pharmacy`, `prescriber`, `written_date`, and `retrieved` (when the history was requested). The history is only on file once someone requests it for the patient and is current as of `retrieved`; no results means no history is on file, not that nothing was filled.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the drug description. |
| `filled_on_or_after` | string (date) | no | ISO 8601 date. Only fills last filled on or after this date. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `drug`, `last_fill_date`, `days_supply`, `supply_ends`, `quantity`, `refills_remaining`, `fill_number`, `sig`, `pharmacy`, `prescriber`, `written_date`, `retrieved`.

**Backing data model:** `MedicationHistoryMedication`.

#### `find_pharmacy_requests`

**Category:** `@clinical_reads`

List what pharmacies have asked the practice about the patient's prescriptions, newest first: refill requests (renew a prescription that has run out of refills) and change requests (a generic or therapeutic substitution, a prior authorization, a clarification). Each has the medication, what the pharmacy asked, when it arrived, and `status`: waiting (nobody has answered), answered (with the prescriber's `response`), or ignored (set aside without an answer). Use it for 'any refill requests waiting', 'did we answer the pharmacy about her lisinopril', or 'why did the pharmacy ask for a prior auth'.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `kind` | string (enum) | no | Only refill requests or only change requests. Omit for both. One of: `refill`, `change`. |
| `status` | string (enum) | no | Only requests with this status, e.g. 'waiting'. One of: `waiting`, `answered`, `ignored`. |
| `limit` | integer | no | Maximum requests of each kind. Defaults to 15. |

**Returns:** Array of objects with `id`, `type` (Refill request, Change request), `received`, `medication`, `pharmacy`, `status` (waiting|answered|ignored), `response`, and `note_dbid` (the note the answer was made in); refills add `sig`, `quantity`, `days_supply`, and `last_fill_date`; changes add `change` (what kind) and `requested` (the medications the pharmacy proposed).

#### `find_questionnaire_responses`

**Category:** `@clinical_reads`

Search the patient's completed and in-progress questionnaire responses (Interviews). Each result includes `name`, `progress_status`, `questionnaire_names`, `answered_at` (ISO 8601), and `responses` — an array of per-question answers with the question text, the human-readable selection, and `response_value` (the question option's underlying value string, often numeric for scored instruments like PHQ-9 or Stress). For scored questionnaires `response_value` is what you'd chart or sum. For non-scored / categorical ones it may be text — in that case offer the clinician a numeric conversion before plotting and confirm their interpretation before treating it as a score. Patient scope is enforced; non-committed interviews are excluded.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring match on the interview's name (e.g., 'PHQ', 'depression', 'GAD', 'stress'). |
| `progress_status` | string | no | Filter to a specific progress_status code (e.g., 'F' for finished/complete, 'S' for started, 'N' for new). Case-insensitive. |
| `limit` | integer | no | Maximum results to return. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, `status`, `progress_status`, `questionnaire_names`, `answered_at`, and `responses` (per-question array of `question`, `response_text`, `response_value`).

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

#### `find_claims`

**Category:** `@claims_reads`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Search claims with optional filters, most recently created first. Excludes trashed claims unless `queue` names the trash queue. Each row has the claim's `id`, its queue, patient, date of service, current payer, assignee or team, balances, and labels. Use get_claim for one claim's full detail. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `queue` | string | no | Queue `name` or `display_name` from find_claim_queues, matched case-insensitively. |
| `patient_id` | string | no | Only claims for this patient's `id`. |
| `assignee_id` | string | no | Only claims assigned to this staff `id`, from find_claim_assignees. |
| `team_id` | string | no | Only claims assigned to this team `id`, from find_claim_assignees. |
| `unassigned` | boolean | no | When true, only claims with no assignee and no team. |
| `label` | string | no | Only claims carrying this label name, matched case-insensitively. |
| `payer_name_contains` | string | no | Case-insensitive substring of the current payer's name. |
| `min_balance` | number | no | Only claims whose patient plus coverage balance is at least this. |
| `service_on_or_after` | string (date) | no | ISO 8601 date; only claims whose note's date of service is on or after it. |
| `service_on_or_before` | string (date) | no | ISO 8601 date; only claims whose note's date of service is on or before it. |
| `limit` | integer | no | Maximum results. Defaults to 25. |

**Returns:** Array of objects with `id`, `queue`, `queue_display`, `patient_id`, `patient_name`, `date_of_service`, `payer_name`, `assignee`, `team`, `patient_balance`, `coverage_balance` (decimal strings), `labels`, `snoozed_until`.

#### `get_claim`

**Category:** `@claims_reads`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Return one claim's full detail: queue, assignee, balances, narrative, coverages, providers, diagnosis codes, active line items with modifiers and diagnosis pointers, labels, active banners, and recent comments. Omit `claim_id` for the claim the agent was opened from. The patient section carries the name and sex only. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** Object with the find_claims row fields plus `narrative`, `account_number`, `prior_auth`, `total_charges`, `patient` (`first_name`, `last_name`, `sex`), `coverages`, `provider`, `diagnosis_codes`, `line_items`, `banners`, and `recent_comments`.

#### `summarize_claims`

**Category:** `@claims_reads`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Count claims and total their balances per queue, excluding trashed claims. Optionally limited to one assignee or team. Use this for questions like 'how many claims are waiting on coding review' or 'what is my open balance'. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `assignee_id` | string | no | Only claims assigned to this staff `id`. |
| `team_id` | string | no | Only claims assigned to this team `id`. |

**Returns:** Array, in queue order, of objects with `queue`, `queue_display`, `count`, `patient_balance`, and `coverage_balance` (decimal strings).

#### `find_claim_queues`

**Category:** `@claims_reads`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

List the instance's claim queues in workflow order. move_claim_to_queue and find_claims take a queue's `name`. Requires the run's revenue capability.

**Arguments:** none.

**Returns:** Array of objects with `name`, `display_name`, and `description`.

#### `find_claim_labels`

**Category:** `@claims_reads`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

List the active labels configured for claims. add_claim_labels accepts only these names. Requires the run's revenue capability.

**Arguments:** none.

**Returns:** Array of objects with `name` and `color`.

#### `find_claim_assignees`

**Category:** `@claims_reads`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Find active staff members and teams a claim can be assigned to, by name. assign_claim takes a staff member's or a team's `id`. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive substring of the staff member's or team's name. |

**Returns:** Object with `staff` (array of `id`, `name`) and `teams` (array of `id`, `name`), each capped at 25.

#### `find_clinical_codes`

**Category:** `@config_reads`

Look up the codes a history or order command needs, by name, from Canvas's own vocabularies, as the chart's pickers do. `kind` is what to look up: `medical_history` (past conditions, for `originate_medical_history`), `condition` (ICD-10 diagnoses), `medication` (FDB, for `originate_medication_statement`), `allergen` (for `originate_allergy`), `family_history` and `surgical_history` (SNOMED, for the history tools), `immunization` (CVX and CPT, for `originate_immunization_statement`), or `imaging_study` (for `originate_imaging_order`). Use the codes it returns exactly; never write a code from memory. When several candidates fit, ask the clinician which one they mean.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `kind` | string (enum) | yes |  One of: `condition`, `medical_history`, `medication`, `allergen`, `family_history`, `surgical_history`, `immunization`, `imaging_study`. |
| `query` | string | yes | The name to search for, e.g. 'penicillin' or 'appendectomy'. |

**Returns:** Array of up to 10 candidates, each with `display` and its codes: `icd10_code` (condition, medical_history), `snomed_code` (condition, family_history, surgical_history), `fdb_code` and `rxnorm_rxcui` (medication), `concept_id` and `concept_type` (allergen), `cvx_code` and `cpt_code` (immunization), or `image_code` (imaging_study).

#### `read_incoming_document`

**Category:** `@intake_reads`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

Read the incoming document this run is about, such as a fax just received, and answer a question from it, with page numbers. Use it to find what the document says about who it is for (name, birth date, MRN), what kind of document it is, and the values it reports. Reads the whole file with a separate model call, so ask for everything you need in one or two questions.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `question` | string | yes | What to find in the document, in one focused question. |

**Returns:** Object with `ok`, `document_id`, `title`, `channel` (e.g. fax), `answer` (with page numbers), and `note`; or `{ok: false, error}` when the file cannot be read.

#### `match_patient`

**Category:** `@intake_reads`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

Check whether the identifiers on the document match exactly one Canvas patient, without suggesting anything. Pass the last name and birth date, plus the first name and MRN when the document gives them, exactly as the document shows them. Returns the patient's id only when exactly one matches; otherwise it says none or several did and names no one. Never guess or loosen identifiers to get a match: a document no one patient matches is for a person to file. On a scan or fax, also pass each identifier `as_printed` and the `legibility`: the code checks the values against the print and tries common fax misreads itself.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `first_name` | string | no | First name as the document gives it. |
| `last_name` | string | no | Last name as the document gives it. |
| `birth_date` | string (date) | no | Birth date as the document gives it, YYYY-MM-DD. |
| `mrn` | string | no | The MRN the document shows, whether Canvas's or the sending organization's. |
| `as_printed` | object | no | For a scanned or faxed document: each identifier exactly as printed, character for character, misprints and all (for example 'DOE, J0HN' or 'DOB: 03/O9/1971'). With it, the identifiers read are checked against the print, and a common fax misread is tried when they match no one. |
| `legibility` | string (enum) | no | How readable the identifiers are: clear; readable_with_artifacts (scan noise, but every character can be made out); illegible (any character is a guess). One of: `clear`, `readable_with_artifacts`, `illegible`. |
| `handwritten` | boolean | no | True when an identifier is handwritten. |
| `pages_disagree` | boolean | no | True when pages show different patients' identifiers. |

**Returns:** `{match: {patient_id}, matched_on, confidence}` when exactly one patient matches (`confidence` is high when three identifiers agree, else medium), else `{match: null, reason}`.

#### `find_document_types`

**Category:** `@intake_reads`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

List the types an incoming document can be filed as, for `categorize_document`. A clinical type with a `template_type` files with a report template (`find_report_templates`) whose values `prefill_document_fields` fills in.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `query` | string | no | Optional words in the type's name, e.g. 'lab' or 'referral'. |
| `report_type` | string (enum) | no |  One of: `CLINICAL`, `ADMINISTRATIVE`. |

**Returns:** Array of `{key, name, report_type, template_type}`; `template_type` is LabReportTemplate, ImagingReportTemplate, SpecialtyReportTemplate, or null.

#### `find_report_templates`

**Category:** `@intake_reads`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

Search the report templates a lab, imaging, or specialty document is filed with, for `prefill_document_fields`. Each template lists its fields: fill in values only for these fields, keyed by the field's `code` when it has one, else its `label`. When several templates fit, choose the one whose fields match the document's values.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `template_type` | string (enum) | yes |  One of: `lab`, `imaging`, `specialty`. |
| `query` | string | yes | Words in the template's name, e.g. 'lipid' or 'CBC'. |

**Returns:** Array of up to 10 `{template_id, name, code, fields: [{code, label, units, type, required}]}`.

#### `find_service_providers`

**Category:** `@config_reads`

Search the practice's directory of outside providers and facilities, the list the chart's Refer and Imaging Order commands pick from. Returns each with `id` (pass it as `service_provider_id` to `originate_refer` or `originate_imaging_order`), name, specialty, and practice. Practice-level config, not patient-scoped. When several fit, ask the clinician which one.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `specialty_contains` | string | no | Case-insensitive match on the specialty (e.g. 'cardiology', 'radiology'). |
| `name_contains` | string | no | Case-insensitive match on the provider's first or last name or practice. |
| `limit` | integer | no | Maximum results. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, `specialty`, `practice_name`, `business_phone`, `business_fax`, and `business_address`.

**Backing data model:** `ServiceProvider`.

#### `find_patient`

**Category:** `@patient_search`

**Offered only to runs with:** the `patient_search` capability. The platform hides it from other runs.

Find the one patient a person means, from the identifiers they give: the last name and birth date, plus the first name and MRN when known. Returns the patient's id only when exactly one patient matches; otherwise it says none or several did and names no one. Never loosen or guess identifiers to get a match: ask the person instead. The other tools still act on this run's patient, not the one found.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `first_name` | string | no | First name, or a nickname. |
| `last_name` | string | no | Last name. |
| `birth_date` | string (date) | no | YYYY-MM-DD. |
| `mrn` | string | no | The patient's MRN, when known. |

**Returns:** `{match: {patient_id}, matched_on}` when exactly one patient matches, else `{match: null, reason}`.

#### `find_providers`

**Category:** `@scheduling_reads`

List the practice's active staff a patient can be booked with, by name or primary location. Returns each with `id` (pass it as `provider_id` to the scheduling tools, or in `provider_ids` to `find_appointment_slots`), name, and primary location. Practice-level config, not patient-scoped.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `name_contains` | string | no | Case-insensitive match on the first or last name. |
| `practice_location_id` | string | no | Only staff whose primary location this is, from find_practice_locations. |
| `limit` | integer | no | Maximum results. Defaults to 25. |

**Returns:** Array of objects with `id`, `name`, and `primary_practice_location_id`.

**Backing data model:** `Staff`.

#### `find_appointment_slots`

**Category:** `@scheduling_reads`

Search the open appointment times the native booking screens offer at one practice location, between two times (at most 31 days apart), for a visit of the given length. Narrow it to providers from find_providers and a visit type from find_note_types. A slot is not held: book soon after finding it, and search again if the booking is refused.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `practice_location_id` | string | yes | The location, from find_practice_locations. |
| `start` | string | yes | Earliest start, ISO 8601 with a time zone. |
| `end` | string | yes | Latest start, ISO 8601 with a time zone. |
| `duration_minutes` | integer | yes |  |
| `provider_ids` | array of string | no |  |
| `visit_type_id` | string | no | The visit's note type, from find_note_types. |
| `reschedule_appointment_id` | string | no | When rescheduling, the appointment, so its own time shows as open. |

**Returns:** Array of up to 50 `{provider_id, start, end}`, earliest first.

#### `find_reason_for_visit_codes`

**Category:** `@config_reads`

Search the reasons for visit the practice configured, the list the chart's Reason for Visit command offers. Returns each with `id` (pass it as `coding_id` to `originate_reason_for_visit`) and `display`. Practice-level config, not patient-scoped. Use a configured reason when one matches what the visit is for.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `display_contains` | string | no | Case-insensitive match on the reason's name (e.g. 'follow', 'physical'). |
| `limit` | integer | no | Maximum results. Defaults to 25. |

**Returns:** Array of objects with `id`, `display`, `code`, and `system`.

**Backing data model:** `ReasonForVisitSettingCoding`.
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

**Offered only to runs with:** `api.change_task`. The platform hides it from a user's run without that permission.

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

**Offered only to runs with:** `api.change_task`. The platform hides it from a user's run without that permission.

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

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

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

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

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

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

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

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

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

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

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

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `AssessCommand`.

#### `originate_follow_up`

**Category:** `@clinical_writes`

Stage a draft Follow-Up command on the patient's current open note to schedule a return visit. NEVER commits. Use when the clinician wants to plan a follow-up appointment (e.g., 'recheck in 2 weeks').

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `requested_date` | string (date) | no | ISO 8601 target date for the follow-up. |
| `comment` | string | no | Free-text reason for the follow-up (visible to scheduling). E.g., 'recheck BP after med adjustment'. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `FollowUpCommand`.

#### `originate_stop_medication`

**Category:** `@clinical_writes`

Stage a draft Stop-Medication command on the patient's current open note to discontinue an active medication. NEVER commits. Requires medication_id from a prior `find_medications` call. Use when the clinician decides to stop a med (side effects, ineffective, completed course).

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `medication_id` | string | yes | UUID of the medication to stop — from a prior find_medications call (the row's `id` field). |
| `rationale` | string | no | Reason for stopping (e.g., 'side effects', 'completed course', 'ineffective'). Visible to anyone reviewing the chart. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

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

#### `originate_review_note`

**Category:** `@clinical_writes`

**Offered only to runs with:** `api.add_note`. The platform hides it from a user's run without that permission.

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

#### `move_claim_to_queue`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Move a claim to another queue, such as from coding review to queued for submission. Takes a queue `name` or `display_name` from find_claim_queues. Trashing a claim is left to a person. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `queue` | string | yes | Target queue `name` or `display_name`. |
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id, queue}` with the queue's `name`.

#### `assign_claim`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Assign a claim to a staff member or a team, given exactly one `id` from find_claim_assignees. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `staff_id` | string | no | The staff member's `id`. |
| `team_id` | string | no | The team's `id`. |
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id, assignee}` with the staff member's or team's name.

#### `unassign_claim`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Clear a claim's assignee or team. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id}`.

#### `add_claim_labels`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Add labels to a claim. Only labels find_claim_labels lists are accepted; creating a new label is left to a person. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `labels` | array of string | yes | Label names, from find_claim_labels. |
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id, labels}`.

#### `remove_claim_labels`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Remove labels from a claim. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `labels` | array of string | yes | Label names, from find_claim_labels. |
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id, labels}`.

#### `add_claim_comment`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Add a comment to a claim's comment thread, visible to everyone working the claim. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `comment` | string | yes | The comment text. |
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id}`.

#### `add_claim_banner`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Show a banner on a claim, such as a reminder that a prior authorization is pending. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `key` | string | yes | Identifier for the banner; remove_claim_banner takes it. |
| `narrative` | string | yes | Banner text, at most 90 characters. |
| `intent` | string (enum) | yes | Severity: info, warning, or alert. One of: `info`, `warning`, `alert`. |
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id, key}`.

#### `remove_claim_banner`

**Category:** `@claims_writes`

**Offered only to runs with:** the `revenue` capability. The platform hides it from other runs.

Remove a claim banner by its `key`, from get_claim's `banners`. Requires the run's revenue capability.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `key` | string | yes | The banner's `key`. |
| `claim_id` | string | no | The claim's `id`, from find_claims. Omit to act on the claim the agent was opened from. |

**Returns:** `{ok, claim_id, key}`.

#### `originate_medical_history`

**Category:** `@clinical_writes`

Stage a draft Medical History command recording a past or ongoing condition on the patient's open note. NEVER commits. Look the condition up first with `find_clinical_codes` (kind 'medical_history') and pass its `icd10_code` and `display`; the tool refuses a code whose entry would not resolve.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `icd10_code` | string | yes | ICD-10 code from find_clinical_codes (kind 'medical_history'). |
| `display` | string | no | The `display` that came with the code. |
| `approximate_start_date` | string (date) | no | ISO 8601 date it began, if known. |
| `approximate_end_date` | string (date) | no | ISO 8601 date it ended, if it has. |
| `show_on_condition_list` | boolean | no | Whether it appears on the conditions list. Defaults to true. |
| `comments` | string | no | Optional comment, up to 1000 chars. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `MedicalHistoryCommand`.

#### `originate_medication_statement`

**Category:** `@clinical_writes`

Stage a draft Medication Statement recording a medication the patient takes (prescribed elsewhere, or over the counter) on the patient's open note. NEVER commits, and never prescribes. Look the medication up with `find_clinical_codes` (kind 'medication') and pass its `fdb_code` and `display`. Refuses a medication already on the list, and a controlled substance, which the clinician records themselves.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `fdb_code` | string | yes | FDB code from find_clinical_codes (kind 'medication'). |
| `display` | string | no | The `display` that came with the code. |
| `sig` | string | no | How the patient takes it, e.g. '1 tablet daily'. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `MedicationStatementCommand`.

#### `originate_allergy`

**Category:** `@clinical_writes`

Stage a draft Allergy command on the patient's open note. NEVER commits. Look the allergen up with `find_clinical_codes` (kind 'allergen') and pass its `concept_id` and `concept_type`. Refuses an allergen already on the list.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `concept_id` | integer | yes | Allergen concept id from find_clinical_codes (kind 'allergen'). |
| `concept_type` | integer | yes | The `concept_type` that came with it. |
| `severity` | string (enum) | no | Severity, if known. One of: `mild`, `moderate`, `severe`. |
| `narrative` | string | no | The reaction, in words, up to 512 chars. |
| `approximate_date` | string (date) | no | ISO 8601 date of onset, if known. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `AllergyCommand`.

#### `originate_family_history`

**Category:** `@clinical_writes`

Stage a draft Family History command on the patient's open note. NEVER commits. Look the condition up with `find_clinical_codes` (kind 'family_history') and pass its `snomed_code` and `display`, with the relative.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `snomed_code` | string | yes | SNOMED code from find_clinical_codes (kind 'family_history'). |
| `display` | string | no | The `display` that came with it. |
| `relative` | string | yes | The relative, e.g. 'mother'. |
| `note` | string | no | Optional note, up to 512 chars. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `FamilyHistoryCommand`.

#### `originate_surgical_history`

**Category:** `@clinical_writes`

Stage a draft Past Surgical History command on the patient's open note. NEVER commits. Look the procedure up with `find_clinical_codes` (kind 'surgical_history') and pass its `snomed_code` and `display`.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `snomed_code` | string | yes | SNOMED code from find_clinical_codes (kind 'surgical_history'). |
| `display` | string | no | The `display` that came with it. |
| `approximate_date` | string (date) | no | ISO 8601 date of the surgery, if known. |
| `comment` | string | no | Optional comment, up to 1000 chars. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `PastSurgicalHistoryCommand`.

#### `originate_immunization_statement`

**Category:** `@clinical_writes`

Stage a draft Immunization Statement recording a vaccine given elsewhere on the patient's open note. NEVER commits. Look the vaccine up with `find_clinical_codes` (kind 'immunization') and pass its `cvx_code`, `cpt_code`, and `display`.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `cvx_code` | string | yes | CVX code from find_clinical_codes (kind 'immunization'). |
| `cpt_code` | string | yes | The `cpt_code` that came with it. |
| `display` | string | no | The `display` that came with it. |
| `approximate_date` | string (date) | no | ISO 8601 date it was given, if known. |
| `comments` | string | no | Optional comment, up to 255 chars. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `ImmunizationStatementCommand`.

#### `originate_vitals`

**Category:** `@clinical_writes`

Stage a draft Vitals command on the patient's open note. NEVER commits. A Vitals command records its readings as taken now, so use it only for readings taken today; never for older readings. Pass at least one reading, in US units.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `height` | integer | no | Inches. |
| `weight_lbs` | integer | no | Pounds. |
| `body_temperature` | number | no | Degrees Fahrenheit. |
| `blood_pressure_systole` | integer | no | Systolic mmHg. |
| `blood_pressure_diastole` | integer | no | Diastolic mmHg. |
| `pulse` | integer | no | Beats/min. |
| `respiration_rate` | integer | no | Breaths/min. |
| `oxygen_saturation` | integer | no | SpO2 percent. |
| `note` | string | no | Optional note, up to 150 chars. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `VitalsCommand`.

#### `originate_resolve_condition`

**Category:** `@clinical_writes`

Stage a draft Resolve Condition command marking one of the patient's conditions resolved, on the patient's open note. NEVER commits. Requires `condition_id` from `find_conditions`.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `condition_id` | string | yes | The condition's `id` from find_conditions. |
| `rationale` | string | no | Why it is resolved, up to 1024 chars. |
| `show_in_condition_list` | boolean | no | Whether it stays on the conditions list as resolved. Defaults to false. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `ResolveConditionCommand`.

#### `originate_remove_allergy`

**Category:** `@clinical_writes`

Stage a draft Remove Allergy command taking an allergy off the patient's list, on the patient's open note. NEVER commits. Requires `allergy_id` from `find_allergies`.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `allergy_id` | string | yes | The allergy's `id` from find_allergies. |
| `narrative` | string | no | Why it is removed, up to 512 chars. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `RemoveAllergyCommand`.

#### `edit_staged_command`

**Category:** `@clinical_writes`

Change fields on a staged (uncommitted) draft command in the patient's open note. NEVER commits. `command_id` is the `command_id` an `originate_*` tool returned in an earlier run, or a command's `uuid` from `get_note_content`. Pass `fields` with the new values, named as the matching `originate_*` tool names its arguments. Only these fields can change, by command: plan: narrative; prescribe: sig, days_supply, refills; labOrder: comment, fasting_required; diagnose: today_assessment, background, approximate_date_of_onset; goal: goal_statement, priority, achievement_status, due_date, progress; assess: status, narrative, background; followUp: requested_date, comment; stopMedication: rationale; medicalHistory: approximate_start_date, approximate_end_date, show_on_condition_list, comments; medicationStatement: sig; allergy: severity, narrative, approximate_date; familyHistory: relative, note; surgicalHistory: approximate_date, comment; immunizationStatement: approximate_date, comments; vitals: height, weight_lbs, body_temperature, blood_pressure_systole, blood_pressure_diastole, pulse, respiration_rate, oxygen_saturation, note; resolveCondition: rationale, show_in_condition_list; removeAllergy: narrative. To change anything else (the medication, condition, code, or allergen itself), use `delete_staged_command` and stage a new draft. A draft this run staged cannot be edited; delete it and stage it again.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `command_id` | string | yes | The draft command's id. |
| `fields` | object | yes | The fields to change and their new values. |

**Returns:** `{ok: true, command_id: <uuid>, command: '<command_key>', changed: [<field>], committed: false}`.

#### `delete_staged_command`

**Category:** `@clinical_writes`

Delete a staged (uncommitted) draft command from the patient's open note. `command_id` is the `command_id` an `originate_*` tool returned, in this run or an earlier one, or a command's `uuid` from `get_note_content`. A committed command, or one on another note, cannot be deleted. Use it to replace a draft staged with the wrong item: delete it, then stage the right one.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `command_id` | string | yes | The draft command's id. |

**Returns:** `{ok: true, command_id: <uuid>, command: '<command_key>', deleted: true}`; `command` is null for a draft this run staged, which is dropped before it reaches the note.

#### `suggest_patient`

**Category:** `@intake_writes`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

Suggest, on the document's review form, the patient the document is for. Pass the identifiers exactly as the document shows them, as for `match_patient`: the patient is matched in code and suggested only when exactly one matches. Files nothing; a person confirms the patient. On a scan or fax, pass `as_printed` and `legibility` as for `match_patient`.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `first_name` | string | no | First name as the document gives it. |
| `last_name` | string | no | Last name as the document gives it. |
| `birth_date` | string (date) | no | Birth date as the document gives it, YYYY-MM-DD. |
| `mrn` | string | no | The MRN the document shows, whether Canvas's or the sending organization's. |
| `as_printed` | object | no | For a scanned or faxed document: each identifier exactly as printed, character for character, misprints and all (for example 'DOE, J0HN' or 'DOB: 03/O9/1971'). With it, the identifiers read are checked against the print, and a common fax misread is tried when they match no one. |
| `legibility` | string (enum) | no | How readable the identifiers are: clear; readable_with_artifacts (scan noise, but every character can be made out); illegible (any character is a guess). One of: `clear`, `readable_with_artifacts`, `illegible`. |
| `handwritten` | boolean | no | True when an identifier is handwritten. |
| `pages_disagree` | boolean | no | True when pages show different patients' identifiers. |
| `label` | string | no | Optional short label shown with the suggestion on the review form, up to 40 characters, e.g. 'From fax header'. |

**Returns:** `{ok: true, patient_id, matched_on, confidence}` when one patient matched and was suggested, else `{ok: false, reason}`.

#### `categorize_document`

**Category:** `@intake_writes`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

Suggest, on the document's review form, the type of document it is. `document_type_key` is a `key` from `find_document_types`. Files nothing; a person confirms the type.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `document_type_key` | string | yes | From find_document_types. |
| `confidence` | string (enum) | no | How sure you are, shown to the reviewer: high only when the document states it plainly. One of: `high`, `medium`, `low`. |
| `label` | string | no | Optional short label shown with the suggestion on the review form, up to 40 characters, e.g. 'From fax header'. |

**Returns:** `{ok: true, document_type: {key, name, template_type}}`.

#### `prefill_document_fields`

**Category:** `@intake_writes`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

Fill in, on the document's review form, the values a lab, imaging, or specialty report gives, for a template from `find_report_templates`. `fields` maps each template field's `code` (or `label`, when it has no code) to the value exactly as the document reports it. Leave out a value the document does not give; never estimate one. Files nothing; a person confirms the values.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `template_type` | string (enum) | yes |  One of: `lab`, `imaging`, `specialty`. |
| `template_id` | integer | yes | From find_report_templates. |
| `fields` | object | yes | Field code or label -> {value, unit?, reference_range?, abnormal?}. |
| `confidence` | string (enum) | no | How sure you are, shown to the reviewer: high only when the document states it plainly. One of: `high`, `medium`, `low`. |
| `label` | string | no | Optional short label shown with the suggestion on the review form, up to 40 characters, e.g. 'From fax header'. |

**Returns:** `{ok: true, template_id, template_name, filled: [<field>]}`.

#### `assign_document_reviewer`

**Category:** `@intake_writes`

**Offered only to runs with:** `api.access_dataintegration`. The platform hides it from a user's run without that permission.

Suggest who reviews the document: a staff member, a team, or both. The review stays required; a person confirms the assignment.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `staff_id` | string | no | The reviewer's staff id. |
| `team_id` | string | no | The reviewing team's id. |
| `label` | string | no | Optional short label shown with the suggestion on the review form, up to 40 characters, e.g. 'From fax header'. |

**Returns:** `{ok: true, staff_id, team_id}`.

#### `originate_imaging_order`

**Category:** `@clinical_writes`

Stage a draft Imaging Order on the patient's open note for the clinician to review and sign. NEVER commits. Look the study up first with `find_clinical_codes` (kind 'imaging_study') and pass its `image_code`; never write a study code from memory. Use when the clinician asks to order imaging.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `image_code` | string | yes | The study's `image_code` from find_clinical_codes (kind 'imaging_study'). |
| `diagnosis_codes` | array of string | no | ICD-10 codes for the problems the order is for, from find_conditions or find_clinical_codes (kind 'condition'). Signing requires at least one. |
| `priority` | string (enum) | no | How urgent the study is. Omit when the clinician did not say. One of: `Routine`, `Urgent`, `STAT`. |
| `service_provider_id` | string | no | Where the study is performed: an `id` from find_service_providers. Optional; the clinician can choose when reviewing. |
| `additional_details` | string | no | Details for whoever performs the study, such as side or contrast. |
| `comment` | string | no | A comment on the order. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `ImagingOrderCommand`.

#### `originate_refer`

**Category:** `@clinical_writes`

Stage a draft Referral on the patient's open note for the clinician to review and sign. NEVER commits. Look the provider up first with `find_service_providers` and pass its `id`. Use when the clinician asks to refer the patient.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `service_provider_id` | string | yes | Who the patient is referred to: an `id` from find_service_providers. |
| `diagnosis_codes` | array of string | no | ICD-10 codes for the problems the order is for, from find_conditions or find_clinical_codes (kind 'condition'). Signing requires at least one. |
| `clinical_question` | string (enum) | no | What the referral asks of the specialist. One of: `Cognitive Assistance (Advice/Guidance)`, `Assistance with Ongoing Management`, `Specialized intervention`, `Diagnostic Uncertainty`. |
| `priority` | string (enum) | no | How urgent the referral is. Omit when the clinician did not say. One of: `Routine`, `Urgent`, `STAT`. |
| `notes_to_specialist` | string | no | What the specialist should know, in the clinician's words. |
| `include_visit_note` | boolean | no | Whether to send this visit's note with the referral. |
| `comment` | string | no | An internal comment on the referral. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `ReferCommand`.

#### `book_appointment`

**Category:** `@scheduling_writes`

**Offered only to runs with:** `api.add_appointment`. The platform hides it from a user's run without that permission.

Book an appointment for this run's patient at a time find_appointment_slots offered. It takes effect when applied, not as a draft: confirm the time, provider, and visit type with the person first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `provider_id` | string | yes | From find_providers. |
| `practice_location_id` | string | yes | From find_practice_locations. |
| `visit_type_id` | string | yes | A schedulable encounter note type, from find_note_types. |
| `start_time` | string | yes | ISO 8601 with a time zone. |
| `duration_minutes` | integer | yes |  |

**Returns:** `{ok: true, booked: false, requested: {...}}`: applied after the run.

#### `reschedule_appointment`

**Category:** `@scheduling_writes`

**Offered only to runs with:** `api.add_appointment`. The platform hides it from a user's run without that permission.

Move one of this run's patient's appointments, from find_appointments, to a new time find_appointment_slots offered (pass reschedule_appointment_id there so the current time shows as open). Canvas cancels the appointment and books a new one with a new id, which find_appointments returns once applied. Takes effect when applied: confirm with the person first. A patient already checked in cannot be rescheduled.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `appointment_id` | string | yes | From find_appointments. |
| `start_time` | string | yes | ISO 8601 with a time zone. |
| `provider_id` | string | no | A new provider, if changing. |
| `practice_location_id` | string | no | A new location, if changing. |
| `duration_minutes` | integer | no |  |

**Returns:** `{ok: true, replaces_appointment_id, requested: {start_time}, note}`: applied after the run, as a new appointment.

#### `cancel_appointment`

**Category:** `@scheduling_writes`

**Offered only to runs with:** `api.add_notestatechangeevent`, `api.change_appointment`. The platform hides it from a user's run without those permissions.

Cancel one of this run's patient's appointments, from find_appointments. Takes effect when applied: confirm with the person first.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `appointment_id` | string | yes | From find_appointments. |

**Returns:** `{ok: true, appointment_id}`: applied after the run.

#### `originate_reason_for_visit`

**Category:** `@clinical_writes`

Stage a draft Reason for Visit on the patient's open note. NEVER commits. Pass the reason in the clinician's or patient's words as `comment`, and, when one of the practice's configured reasons fits, its `coding_id` from `find_reason_for_visit_codes`. Without a comment the reason's name is used.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `comment` | string | no | Why the patient is being seen, in plain words. |
| `coding_id` | string | no | A configured reason's `id` from find_reason_for_visit_codes. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `ReasonForVisitCommand`.

#### `originate_hpi`

**Category:** `@clinical_writes`

Stage a draft History of Present Illness on the patient's open note. NEVER commits. Write the narrative from what the clinician or the visit said; never add findings the source does not contain.

**Arguments:**

| Name | Type | Required | Description |
|---|---|---|---|
| `narrative` | string | yes | The history of present illness as plain text. |

**Returns:** `{ok: true, note_id: <uuid>, command_id: <uuid>, command: '<command_key>', committed: false}`. Never commits — the clinician reviews the draft in the chart and decides whether to commit. `command_id` names the draft for `edit_staged_command` or `delete_staged_command`.

**Backing Command:** `HistoryOfPresentIllnessCommand`.
<!-- AUTOGEN:writes END -->
