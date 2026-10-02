---
title: "Managing State"
slug: "agents-managing-state"
excerpt: "Three patterns for persisting agent state across runs."
---

`AgentState` itself is intentionally thin — it's a dataclass holding a
`data: dict[str, Any]` that the framework hands to `run()` and
collects back from it. The interesting decision is *what* you store
and *where*, and the answer depends on what your agent actually needs
to remember.

Three patterns cover the common cases. They share the same
`load_state` / `run` / `save_state` contract — only what those methods
do differs.

## Pattern 1: Stateless

The agent has no memory of prior runs. Every invocation reads the
patient's current chart fresh, makes a decision, emits effects. This
is the simplest pattern and the right starting point.

```python
class ChartSummary(AgentPlugin):
    """Drafts a Plan command on a new note. No state between runs."""

    def load_state(self, scope_key):
        return AgentState()

    def run(self, state, gateway, trigger_payload):
        # ... LLM loop, accumulate effects ...
        return AgentRunResult(state=state, effects=effects)

    def save_state(self, scope_key, state):
        return None
```

Use it when each run can stand on its own — the trigger fires, the
agent reads the chart, the agent emits effects, done.

## Pattern 2: Snapshot

The whole state lives in one record. `load_state` reads it,
`run()` mutates it in memory, `save_state` writes it back. Best for
agents whose state grows roughly linearly in time and is always read
as a unit — chat conversations being the canonical example.

The full message history (user turns + assistant turns + tool calls +
tool results) lives in a single JSON column. Reading the row and
writing it back is one round-trip each.

```python
from django.db.models import DO_NOTHING, ForeignKey, JSONField
from canvas_sdk.v1.data.base import CustomModel


class Conversation(CustomModel):
    """One row per patient, holds the full message history as JSON."""

    patient = ForeignKey(PatientProxy, to_field="dbid", on_delete=DO_NOTHING)
    messages = JSONField(default=list)


class ChatAgent(AgentPlugin):
    tools = _registered_tools

    def load_state(self, scope_key):
        patient_id = scope_key.rsplit(":", 1)[-1]
        conversation = Conversation.objects.filter(patient__id=patient_id).first()
        return AgentState(data={
            "patient_id": patient_id,
            "messages": list(conversation.messages) if conversation else [],
        })

    def run(self, state, gateway, trigger_payload):
        messages = state.data["messages"]
        messages.append({"role": "user", "content": trigger_payload["user_message"]})
        # ... LLM loop appends assistant turns + tool blocks to messages ...
        state.data["messages"] = messages
        return AgentRunResult(state=state, effects=[])

    def save_state(self, scope_key, state):
        patient = PatientProxy.objects.get(id=state.data["patient_id"])
        conversation, _ = Conversation.objects.get_or_create(patient=patient)
        conversation.messages = state.data["messages"]
        conversation.save()
```

The platform's per-`scope_key` lock guarantees that `load → run →
save` is atomic — no race between two concurrent runs reading the
same baseline and clobbering each other.

**Trade-offs**: read and write cost grow with history length. At some
point (typically dozens-of-turns) you'll want to either trim the
in-memory list before sending it to the LLM (to control prompt
tokens) or compact it into a summary. For chat in particular, plan
for that compaction before the conversation grows unbounded.

The snapshot pattern is also where **prompt caching** pays off most
— the system prompt, tool definitions, and the prefix of the message
history are stable turn-to-turn. See [Prompts → Prompt caching for
cost control](/sdk/agents-prompts/#prompt-caching-for-cost-control).

> **Coming soon**: the SDK will ship `AllTurnsState`,
> `SlidingWindowState`, and `SummarizingState` helpers that handle
> the load/save plumbing for the common snapshot shapes (full
> history, last-N turns only, periodically summarized). Until then,
> the snapshot pattern is something you implement yourself per agent
> — the example above is the typical shape.

## Pattern 3: Event-sourced

State is a set of rows, each a discrete fact. `load_state` rarely
reads them (the agent queries them inside `run()` instead);
`save_state` is often a no-op because writes happen as a side
effect of tool calls during the run.

Best for agents whose state is "a list of things we've recommended
over time" or "a log of decisions, indexed for later lookup." Each
recommendation is its own row; you can mark them resolved
independently, query just the open ones, count them, etc. — all
things that are awkward with the snapshot pattern.

```python
class Recommendation(CustomModel):
    """One row per recommendation the agent has proposed."""

    patient = ForeignKey(PatientProxy, to_field="dbid", on_delete=DO_NOTHING)
    narrative = TextField()
    category = TextField()         # "task" | "follow_up_lab" | "none"
    status = TextField(default="open")  # "open" | "addressed" | "obsolete"
    proxy_data = JSONField(default=dict)


@tools.tool(name="propose_recommendation", description="...", input_schema={...})
def _propose_recommendation(arguments, *, ctx):
    """Write one Recommendation row + stage an AddTask effect to surface it."""
    patient = PatientProxy.objects.get(id=ctx["patient_id"])
    rec = Recommendation.objects.create(
        patient=patient,
        narrative=arguments["narrative"],
        category=arguments["category"],
        proxy_data=arguments.get("proxy_data") or {},
    )
    ctx["effects"].append(AddTask(patient_id=ctx["patient_id"], title=rec.narrative).apply())
    return {"ok": True, "recommendation_id": str(rec.id)}


class LongitudinalAdvisor(AgentPlugin):
    tools = _registered_tools

    def load_state(self, scope_key):
        # Don't materialize state here — run() queries the table directly.
        return AgentState()

    def run(self, state, gateway, trigger_payload):
        patient_id = trigger_payload["patient_id"]
        open_recs = Recommendation.objects.filter(patient__id=patient_id, status="open")
        # ... agent reasons over open recommendations + chart context ...
        return AgentRunResult(state=state, effects=effects)

    def save_state(self, scope_key, state):
        return None  # writes happen inside tool calls
```

**Trade-offs**: writes are scattered through `run()` (via tool calls)
rather than gathered in `save_state`. That means a crash mid-run can
leave partial state — some recommendations written, others not.
Acceptable for most cases because the "missing" recommendations
simply re-propose on the next trigger. Less acceptable if writes need
to be transactional with effect emission, in which case prefer the
snapshot pattern.

This pattern works especially well when **the rows are queryable for
their own purposes** — clinicians' task queues, admin reporting,
metrics dashboards. The agent's writes become first-class chart data,
not just agent-internal scaffolding.

## Picking a pattern

| Pattern | When |
|---|---|
| Stateless | Each run can stand alone; no learning across runs. |
| Snapshot | One coherent thing grows over time (a conversation, a session). |
| Event-sourced | A set of discrete facts that need to be queried, counted, or updated independently. |

You can mix patterns within a plugin — different agents have different
needs.

## `AgentState` mechanics

```python
@dataclass
class AgentState:
    data: dict[str, Any] = field(default_factory=dict)
```

The dict is yours to shape. Keep it JSON-serializable if you plan to
hand-roll storage that uses `JSONField`; otherwise any structure that
your `save_state` can persist is fine.

The state is held *only* across the boundary between `load_state` and
`save_state` — it's not implicit on `self`. (Hooks like
`on_run_start` and `on_run_end` see the agent instance but should
treat instance state as ephemeral; the run might be re-instantiated
on a different worker on retry.)

## Storage options

State has to live somewhere the next run can find it. Three durable
options the SDK supports:

- **[Custom Data](/sdk/custom-data/) tables** (recommended for
  durable state). Your plugin declares `CustomModel` subclasses in
  its manifest; rows persist across plugin reloads. Both
  patterns 2 and 3 above use this.
- **[Caching API](/sdk/caching/)** (TTL-bounded; up to 14 days). Best
  for ephemeral state that's recoverable if lost — partial
  computation results, recently-seen tokens, etc.
- **External services** (`canvas_sdk.clients`). Plugin secrets carry
  credentials; do your own I/O. Common for integrations that need
  cross-instance state.

Reach for Custom Data first. The platform indexes it the same way as
core models, plays nicely with the per-`scope_key` lock, and shows up
in your plugin's namespace so it's easy to reason about retention.
