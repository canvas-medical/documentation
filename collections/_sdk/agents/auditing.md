---
title: "Auditing"
slug: "agents-auditing"
excerpt: "What the platform captures automatically, and what you should capture yourself."
---

Agent runs need an audit trail for two distinct purposes — billing
and operations on one side, "what did the agent do, and why" on the
other. Those two needs have different shapes, different schemas,
different retention requirements, and different owners. The Agent
Runner Framework splits the responsibility along that line.

## Platform-owned audit (skeleton)

The platform captures structural facts about every run: things that
have a stable schema, are needed for billing or abuse detection
regardless of what the agent author wrote, and have predictable
retention. You don't need to do anything to enable these — they
happen automatically for every run.

Captured today:

- **Run records**: one `AgentRun` record per run, which your plugin
  can read (see [Reading run records](#reading-run-records) below).
  It holds the agent, the triggering handler, the scope, the run's
  subject by id, and the run's status: `queued`, `running`,
  `succeeded`, `failed`, `refused`, `abandoned`, or `gave_up`; a run
  whose worker stopped reads as `abandoned` as soon as its hold on the
  scope expires. It also holds why a run failed or was refused, when
  it was queued, started, and finished, how many times it waited for
  its scope or a free worker, how many model calls it made, how its
  last tool loop ended, and how many effects it returned, had dropped
  by its tool grant, and applied.
  Runs that never reach your agent are recorded too: a subject that
  fails the platform's checks, a run that gave up waiting for its
  scope, and one whose worker died.
- **Tool-call envelope**: for every tool call `run_tool_loop` makes,
  sub-agents included, the tool's name, whether it succeeded, the
  exception type when it did not, and how long it took. Arguments and
  results are left out: they carry chart content, and only you know
  what is worth keeping (see below). An agent that calls the model
  without `run_tool_loop` gets a record without these, and without
  its model-call count or how its tool loop ended.
- **LLM usage**: Canvas's inference gateway records every call in its
  usage ledger: model, token counts by cache class, and cost, against
  your organization's inference account. It retains no request or
  response bodies.
- **Effect audit**: each effect the agent returns is applied like any
  other plugin effect and recorded in Canvas's security audit trail.
  Those events name the clinician whose action started the run, your
  plugin, and the agent class, and carry the `run_id` as their
  correlation id, so one id joins a run's record and its chart changes.
- **Logs and errors**: the platform logs each run's start and finish,
  and unexpected exceptions go to Sentry, tagged with the agent ID.

The platform records these itself, around and inside the tool loop,
so agent code can neither skip nor alter them.

Coming soon:

- **Per-LLM-call latency**: wall-clock and time-to-first-token.
- **LLM call attribution**: the gateway's usage ledger records the
  instance, plugin, agent, and `run_id` behind each call, so the
  `run_id` also joins a run to its LLM calls.

The skeleton is the safety net. Even if your plugin captured zero
domain audit data, the platform's records answer: how many times did
this agent run, what was the success rate, how long did it take, how
much did it cost. That's enough to investigate basic ops questions
or notice that an agent is misbehaving. It is *not* enough to answer
"why did the agent recommend X for this patient" — that's your job.

Run records are kept for 90 days. The platform stores them by day
and drops each day once all of it is older than that.

### Reading run records

`AgentRun` and `AgentRunToolCall` are data models in
`canvas_sdk.v1.data`. A run's record has the `run_id` its
`RunAgentEffect` generated, so a handler can return that id to a UI and
the UI can follow the run:

```python?partial=true
from canvas_sdk.effects.agent import RunAgentEffect
from canvas_sdk.v1.data import AgentRun

run = RunAgentEffect(
    agent_id="my_plugin.agents.chat:ChatAgent",
    scope=RunAgentEffect.Scope.PATIENT_AND_STAFF,
    patient_id=patient_id,
    trigger_payload={"user_message": message},
)
# Return str(run.run_id) with the 202, then, when the UI asks:
record = AgentRun.objects.filter(id=run_id, plugin_name="my_plugin").first()
record.status       # "queued" until the run starts, then "running", then final
record.error_kind   # for a failed run, such as "LLM_REFUSED"
record.tool_calls.values_list("name", "ok")
```

Inside a run, the agent has its record's id as `self.run_id`.

## Plugin-owned audit (semantic)

Why an agent did what it did — and what specifically it looked at to
decide — is content only you can reason about. Canvas doesn't know
your agent's intent; the platform can capture the structural facts
of a run but it can't tell whether the recommendation was a *good*
recommendation, or whether the agent's tool calls actually informed
the decision.

You own this layer. Typical things to capture:

- The agent's stated rationale (a natural-language explanation of
  why it did what it did).
- The specific chart facts the agent grounded its decision in
  ("recommended an A1c recheck because last value was 9.2 in March,
  no recheck since").
- Tool results that informed the decision, when they're not
  reconstructable from the patient's current chart state.
- Inputs from the clinician, for user-initiated agents.
- The model's final response text, for conversational agents.

These don't have a one-size-fits-all schema — they're agent-specific
and you should design them around the questions you expect to need
to answer.

### Recommended pattern

Keep a Custom Data table of what only your agent knows, one row per
run, keyed by `self.run_id` so it joins the platform's record. The
status, timing, and counts are already on that record, so your row
holds the meaning:

```python
from django.db.models import JSONField, TextField

from canvas_sdk.v1.data.base import CustomModel


class AdvisorDecision(CustomModel):
    """Why one run of the advisor did what it did. Plugin-owned semantic audit."""

    run_id = TextField()
    rationale = TextField(blank=True, default="")
    grounding_facts = JSONField(default=dict)
```

Write it from `run()`, where the reasoning is, or from a lifecycle hook
(see [Lifecycle](/sdk/agents-lifecycle/#optional-hooks)):

```python?partial=true
def on_run_end(self, result):
    AdvisorDecision.objects.create(
        run_id=self.run_id,
        rationale=self._rationale,
        grounding_facts=self._grounding_facts,
    )
```

Lifecycle hook failures are caught and logged by the platform — a
broken audit path can't crash the underlying run.

## Retention is your decision, with a ceiling

Default retention for Custom Data tables is "as long as the plugin
is installed." For audit tables, that default is wrong — clinical
data accumulates indefinitely, your storage bill follows, and
de-identification / right-to-be-forgotten obligations become
expensive to honor on data you didn't need to keep.

> **Coming soon**: per-table retention policy declared in
> `CANVAS_MANIFEST.json`. The platform will run a daily prune job that
> drops rows older than the declared cutoff. The platform sets a maximum cap by data class
> (e.g., 2 years for clinical-data-bearing tables, 90 days for purely
> operational); you choose any duration up to that.

Until then, plan your own retention. Two pragmatic approaches:

1. **Compact aggressively.** Store enough to answer "what happened
   on this run" for, say, 30 days; compact older runs into per-day
   aggregates (count, error rate, average duration, p95 cost) and
   drop the originals.
2. **Project, then prune.** For "what did the agent decide for this
   patient" queries, the answer often lives in *clinical state*
   (a Task, a recommendation, a draft command) not in the audit
   log itself. Audit-log rows are scaffolding; once their
   information is reflected in chart state, the audit row can be
   dropped without losing the decision.

The shape that's almost always wrong: retaining everything forever
because nobody decided otherwise.

## Evals and replay

> **Coming soon**: SDK helpers for running an agent against captured
> inputs (the same `trigger_payload` plus the chart state at that
> moment) to evaluate prompt changes against historical runs.

The minimum you need today for replay is: the agent's
`trigger_payload`, the patient's chart state at run time (which
Canvas already retains), and either the prompt + tool definitions
the agent used or — better — a deterministic pin on the agent class
+ tool registry so you can rebuild them.

The audit-log row + chart state usually gets you there.

## Splitting platform vs plugin in practice

A useful test: if you removed your agent and replaced it with a
different agent at the same trigger, which audit data would still
be useful?

- Cost, token counts, run durations, error rates, scope contention
  — useful regardless of the agent. **Platform-owned.**
- "The agent saw an A1c of 9.2 and proposed a recheck in 3 months"
  — only meaningful in the context of this specific agent and its
  decision logic. **Plugin-owned.**

Your audit row can leave out what the run record already holds and
join it on `run_id` instead. Keep a structural fact in your row when
you need it beyond the run record's 90 days, or alongside the
reasoning it explains.
