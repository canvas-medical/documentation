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

```python?partial=true
class PlanDrafter(AgentPlugin):
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
writing it back is one round-trip each. The reference plugin's chat
agent keeps one conversation per patient and clinician, so one
clinician's questions never become another's context, and puts both
ids in the `scope_key`:

```python?partial=true
from django.db.models import DO_NOTHING, ForeignKey, JSONField

from canvas_sdk.v1.data.base import CustomModel


class Conversation(CustomModel):
    """One row per patient and clinician, holding the message history as JSON."""

    patient = ForeignKey(PatientProxy, to_field="dbid", on_delete=DO_NOTHING)
    staff = ForeignKey(StaffProxy, to_field="dbid", on_delete=DO_NOTHING)
    messages = JSONField(default=list)


def chat_scope_key(patient_id, staff_id):
    return f"patient:{patient_id}:staff:{staff_id}"


class ChatAgent(AgentPlugin):
    tools = _registered_tools

    def load_state(self, scope_key):
        _, patient_id, _, staff_id = scope_key.split(":")
        conversation = Conversation.objects.filter(
            patient__id=patient_id, staff__id=staff_id
        ).first()
        return AgentState(data={
            "patient_id": patient_id,
            "staff_id": staff_id,
            "messages": list(conversation.messages) if conversation else [],
        })

    def run(self, state, gateway, trigger_payload):
        messages = [*state.data["messages"], {"role": "user", "content": trigger_payload["user_message"]}]
        result = self.run_tool_loop(gateway, ctx=tool_ctx, system=SYSTEM_PROMPT, messages=messages)
        state.data["messages"] = result.messages  # the history plus this run's turns
        return AgentRunResult(state=state, effects=effects)

    def save_state(self, scope_key, state):
        conversation, _ = Conversation.objects.get_or_create(
            patient=PatientProxy.objects.get(id=state.data["patient_id"]),
            staff=StaffProxy.objects.get(id=state.data["staff_id"]),
        )
        conversation.messages = state.data["messages"]
        conversation.save()
```

Take the patient and clinician from the scope, as above, rather than
from `trigger_payload`, so the chart the run reads and the record it
saves always belong to the same patient.

Because runs on the same scope go one at a time, `load → run → save`
can't interleave with another run that read the same baseline.

**Keep the history within one model call.** A conversation that grows
without bound eventually exceeds the model's context window, and every
call after that is refused. `run_tool_loop` sends the model only the
newest turns that fit a size budget, starting on a plain user message
so a tool result is never sent without its tool call, and always
keeping the latest question; it still returns the full history for you
to store. If you call the model yourself, `window_messages(messages)`
does the same trimming.

The snapshot pattern is also where **prompt caching** pays off most
— the system prompt, tool definitions, and the prefix of the message
history are stable turn-to-turn. See [Prompts → Prompt caching for
cost control](/sdk/agents-prompts/#prompt-caching-for-cost-control).

## Pattern 3: State in the chart

The agent's state is records in the chart itself: the protocol cards,
tasks, or banner alerts it staged on earlier runs. `load_state` and
`save_state` do nothing; `run()` reads the records it needs, and the
effects it returns are the writes.

Best for agents whose state is "the recommendations we've made over
time." Each recommendation is its own record the clinician already
sees and acts on, and the agent can update each one independently on
later runs. The reference plugin's longitudinal advisor works this way
with protocol cards (see the [Quick Start](/sdk/agents-quick-start/)):

```python?partial=true
from canvas_sdk.v1.data import ProtocolCurrent


class LongitudinalCareAdvisor(AgentPlugin):
    tools = _registered_tools  # granted @clinical_reads and @clinical_alerts

    def load_state(self, scope_key):
        return AgentState()  # the cards are the state

    def run(self, state, gateway, trigger_payload):
        patient_id = trigger_payload["patient_id"]
        cards = ProtocolCurrent.objects.filter(patient__id=patient_id, plugin_name="my_plugin")
        # ... brief the model with the cards; it updates them by card_key and
        # stages new ones through add_or_update_protocol_card ...
        return AgentRunResult(state=state, effects=effects)

    def save_state(self, scope_key, state):
        return None  # the effects are the writes
```

The next run on the same scope starts only after this run's effects
have been applied, so it sees the cards this run staged.

**Trade-offs**: nothing is written if the run fails, since effects are
applied only after `run()` returns successfully; the next trigger
simply tries again. The agent is limited to what the chart can hold,
so reach for Custom Data when it needs to remember facts no chart
record captures.

This pattern works especially well because the records are useful on
their own: clinicians act on the cards, task queues pick up the tasks,
and nothing about the agent's memory is hidden in a plugin table.

## Picking a pattern

| Pattern | When |
|---|---|
| Stateless | Each run can stand alone; no learning across runs. |
| Snapshot | One coherent thing grows over time (a conversation, a session). |
| State in the chart | Discrete recommendations the clinician should see and act on, updated independently across runs. |

You can mix patterns within a plugin — different agents have different
needs.

## `AgentState` mechanics

```python
from dataclasses import dataclass, field
from typing import Any


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

State has to live somewhere the next run can find it. The options the
SDK supports:

- **The chart.** Protocol cards, tasks, and banner alerts your agent
  stages through its effects, read back on the next run. Pattern 3
  above uses this.
- **[Custom Data](/sdk/custom-data/) tables** (recommended for
  durable state the chart can't hold). Your plugin declares `CustomModel` subclasses in
  its manifest; rows persist across plugin reloads. Pattern 2 above
  uses this.
- **[Caching API](/sdk/caching/)** (TTL-bounded; up to 14 days). Best
  for ephemeral state that's recoverable if lost — partial
  computation results, recently-seen tokens, etc.
- **External services** (`canvas_sdk.clients`). Plugin secrets carry
  credentials; do your own I/O. Common for integrations that need
  cross-instance state.

Reach for Custom Data first when the chart itself can't hold the
state. It lives in your plugin's namespace, so it's easy to reason
about retention, and runs on the same scope never interleave their
reads and writes to it.
