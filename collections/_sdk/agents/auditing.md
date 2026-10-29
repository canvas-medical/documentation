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

- **Run outcomes**: the platform logs each run's start (`agent_id`,
  `scope_key`, `run_id`), its completion with the number of effects
  emitted, runs that waited for their scope, and gateway failures by
  kind (`LLM_UNAVAILABLE`, `LLM_REFUSED`, `LLM_NOT_CONFIGURED`).
  Unexpected exceptions go to Sentry, tagged with the agent ID.
- **Run duration**: a timing metric for every run, tagged with the
  `agent_id`.
- **LLM usage**: Canvas's inference gateway records every call in its
  usage ledger: model, token counts by cache class, and cost, against
  your organization's inference account, along with the instance,
  plugin, agent, and `run_id` that made it. It retains no request or
  response bodies.
- **Effect audit**: each effect the agent returns is applied like any
  other plugin effect and recorded in Canvas's security audit trail.
  Those events name the clinician whose action started the run, your
  plugin, and the agent class, and carry the `run_id` as their
  correlation id, so one id joins a run's chart changes to its LLM
  calls.

Captured with V1:

- **Run records**: a durable record per run with `agent_id`,
  `scope_key`, `run_id`, status, how long it waited for its scope,
  start and end timestamps, and wall-clock duration.
- **Per-LLM-call latency**: wall-clock and time-to-first-token.
- **Tool-call envelope**: name, arguments shape/hash, latency,
  error type for every tool the agent dispatches. Note: the
  envelope is structural metadata; the tool's *result content* is
  plugin-owned (see below) because only you know what's worth
  keeping and what counts as PHI you don't want sitting in
  platform audit storage.

The skeleton is the safety net. Even if your plugin captured zero
domain audit data, the platform's records answer: how many times did
this agent run, what was the success rate, how long did it take, how
much did it cost. That's enough to investigate basic ops questions
or notice that an agent is misbehaving. It is *not* enough to answer
"why did the agent recommend X for this patient" — that's your job.

Retention for platform-captured data is platform-set (long enough
for billing reconciliation and compliance, with the same
de-identification and right-to-be-forgotten guarantees that apply to
other Canvas-held data).

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

The reference plugin demonstrates one shape: a Custom Data table
with one row per agent invocation, written by lifecycle hooks:

```python
from django.db.models import DateTimeField, IntegerField, JSONField, TextField

from canvas_sdk.v1.data.base import CustomModel


class AgentRunLog(CustomModel):
    """One row per AgentPlugin invocation. Plugin-owned semantic audit."""

    agent_class_name = TextField()
    scope_key = TextField()
    status = TextField()                       # "running" | "success" | "error"
    started_at = DateTimeField(auto_now_add=True)
    completed_at = DateTimeField(null=True)
    duration_ms = IntegerField(null=True)
    llm_turns = IntegerField(null=True)
    error_type = TextField(blank=True, default="")
    error_message = TextField(blank=True, default="")
    # Add the fields your agent's questions actually need:
    rationale = TextField(blank=True, default="")
    grounding_facts = JSONField(default=dict)
```

Hooked up via the lifecycle surface (see
[Lifecycle](/sdk/agents-lifecycle/)):

```python
from datetime import UTC, datetime

from canvas_sdk.agents import AgentPlugin

from my_plugin.models.run_log import AgentRunLog


class MyAgent(AgentPlugin):
    def on_run_start(self, scope_key):
        self._run_log = AgentRunLog.objects.create(
            agent_class_name=self.__class__.__name__,
            scope_key=scope_key,
            status="running",
        )

    def on_turn(self, turn_index):
        # run_tool_loop calls this before each model call, counting from 0.
        self._run_log.llm_turns = turn_index + 1

    def on_run_end(self, result):
        self._run_log.status = "success"
        self._run_log.completed_at = datetime.now(UTC)
        # ... other fields ...
        self._run_log.save()

    def on_run_error(self, exc):
        self._run_log.status = "error"
        self._run_log.error_type = type(exc).__name__
        self._run_log.error_message = str(exc)[:500]
        self._run_log.save()
```

Lifecycle hook failures are caught and logged by the platform — a
broken audit path can't crash the underlying run. See
[Lifecycle](/sdk/agents-lifecycle/#optional-hooks) for the full
contract.

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

When in doubt, capture the structural fact in your audit row even
if you think the platform does too. The platform's records are
optimized for billing and ops, not for your debugging — and your
table is closer to where your agent's logic lives.
