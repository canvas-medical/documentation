---
title: "Lifecycle"
slug: "agents-lifecycle"
excerpt: "What your AgentPlugin subclass implements, and what the platform does around it."
---

`AgentPlugin` is the abstract base class for every agent. You implement
three methods (`load_state`, `run`, `save_state`); the platform handles
dispatch, serialization, hook invocation, and effect delivery around them.

```python
from canvas_sdk.agents import AgentPlugin, AgentRunResult, AgentState, LLMGateway


class MyAgent(AgentPlugin):

    def load_state(self, scope_key: str) -> AgentState:
        """Return this run's starting state, or AgentState() if none."""
        ...

    def run(
        self,
        state: AgentState,
        gateway: LLMGateway,
        trigger_payload: dict,
    ) -> AgentRunResult:
        """Drive the agent. Return updated state and the effects to emit."""
        ...

    def save_state(self, scope_key: str, state: AgentState) -> None:
        """Persist the updated state for the next run."""
        ...
```

## What the platform does, in order

When a handler returns a `RunAgentEffect`, the following happens. Each
step is platform-driven:

1. **Take the run's scope.** A background worker claims the scope for
   this agent and `scope_key`. If another run holds it, this run waits
   and retries with backoff. See [Concurrency](#concurrency) below.
2. **Check ownership.** The agent must belong to the plugin whose
   handler returned the effect; a plugin can't run another plugin's
   agents.
3. **Build the `LLMGateway`** from the instance's inference gateway URL
   and your plugin's `INFERENCE_GATEWAY_KEY` secret, attributed to your
   plugin, this agent, and this run. If either is unset, the run stops
   here with `error_kind="LLM_NOT_CONFIGURED"`.
4. **Instantiate your subclass** (`agent_class()` with no arguments).
5. **Apply the manifest tool grant.** The platform expands
   `tools.allowed` (tool names and `@category` groups) against
   `agent.tools`, subtracts `tools.denied`, sets `agent.tools_allowed`
   to the result, and replaces `agent.tools` with a scoped view
   containing only those tools. An agent entry with no `tools.allowed`
   gets no tools.
6. **Call `on_run_start(scope_key)`** (optional hook; default no-op).
7. **Call `load_state(scope_key)`** to get the run's starting state.
8. **Call `run(state, gateway, trigger_payload)`** — the body of your
   agent.
9. **Call `save_state(scope_key, result.state)`** with the updated
   state from your `AgentRunResult`.
10. **Call `on_run_end(result)`** (optional hook).
11. **Filter and stamp the emitted effects.** Any effect whose type no
    granted tool stages is dropped. The rest are stamped with
    provenance (`plugin_name`, `handler_name` set to the agent class,
    `actor`, `source`).
12. **Apply the effects** through the same pipeline as any plugin
    effect, recording them in the audit trail as requested by the user
    whose action started the run.
13. **Release the scope**, so the next run on it can start.

If any of steps 7–9 raises, `on_run_error(exc)` fires, the exception
is captured to Sentry, and the run returns `success=False`. Errors from
the inference gateway are classified rather than captured: an outage
(`error_kind="LLM_UNAVAILABLE"`) is retried, and a refusal
(`error_kind="LLM_REFUSED"`) fails the run without a retry.

A run gets 10 minutes. One still running after that is abandoned: its
state is not saved and its effects are not applied, and the scope
passes to the next run. When the instance is already running its share
of agents, a new run waits and retries rather than taking workers that
event handlers need.

## The three methods you implement

### `load_state(scope_key) -> AgentState`

Called once per run, before `run()`. Return the state this run should
start from — read from your Custom Data tables, deserialize a JSON
blob, query the chart, whatever makes sense. Return `AgentState()`
(empty) if your agent is stateless.

`scope_key` is the same string the trigger emitted; you control its
shape. Use it as the key into your storage.

### `run(state, gateway, trigger_payload) -> AgentRunResult`

The body of your agent. Drive the tool-use loop, accumulate effects,
update `state` in place. Return an `AgentRunResult(state=..., effects=[...])`.

```python?partial=true
from canvas_sdk.agents import AgentRunResult
from canvas_sdk.effects import Effect


def run(self, state, gateway, trigger_payload):
    effects: list[Effect] = []
    tool_ctx = {"patient_id": trigger_payload["patient_id"], "effects": effects}
    self.run_tool_loop(gateway, ctx=tool_ctx, system=SYSTEM_PROMPT, messages=messages)
    return AgentRunResult(state=state, effects=effects)
```

The `effects` list is what the platform will dispatch *after* `run()`
returns and `save_state()` commits — the platform owns *when* effects
emit; your agent owns *what*. Save and dispatch both happen while the
run holds its scope, so the next run on that scope starts from the
state and chart this run left behind.

### Running the model with `run_tool_loop`

Most agents spend `run()` in the same loop: call the model, run the
tools it asks for, send the results back, and repeat until it finishes.
`self.run_tool_loop` does that with the agent's granted tools:

```python?partial=true
result = self.run_tool_loop(
    gateway,
    ctx=tool_ctx,               # passed to every tool; the model never sees it
    system=SYSTEM_PROMPT,
    messages=messages,          # the conversation so far, ending with the turn to answer
    max_turns=8,                # optional; also max_tokens, model, history_chars, cache_system
)
result.text       # the model's last reply, stripped
result.messages   # messages plus every new turn, as JSON-safe dicts you can store
result.turns      # how many model calls it made
result.stopped    # "end_turn", "max_turns", or "unexpected"
```

Along the way it:

- runs each tool call through `self.tools` and sends a failure back to
  the model as an error result, so the model can recover;
- runs complete tool calls in a turn the token limit cut off;
- sends the model only the newest part of a long history that fits a
  size budget (`history_chars`, 300,000 characters by default), while
  returning all of it (`history_chars=None` sends everything);
- marks the system prompt for prompt caching (`cache_system=False` to
  turn that off);
- answers any tool call left open when the model stops unexpectedly,
  so a stored transcript is always valid to send again;
- calls `on_turn` before each model call;
- lets errors from the inference gateway propagate, so the platform can
  retry an outage and record a refusal.

`canvas_sdk.agents.run_tool_loop` is the same loop as a function that
takes `tools` explicitly, for code without an agent instance; sub-agents
use it.

### `save_state(scope_key, state) -> None`

Called once per run, after `run()` returns. Persist `state.data`
back to wherever you read it from. For stateless agents this is a
no-op.

`save_state` runs while the run holds its scope. A concurrent
`RunAgentEffect` for the same agent and `scope_key` waits until this
run's effects have been applied.

## Optional hooks

`AgentPlugin` declares four lifecycle hooks. Override them in your
subclass to capture observability data without polluting `run()`.

| Hook | When it fires | What it receives |
|---|---|---|
| `on_run_start(scope_key)` | After instantiation, before `load_state` | The scope_key for this run |
| `on_run_end(result)` | After `save_state` succeeds | The `AgentRunResult` |
| `on_run_error(exc)` | If any of `load_state` / `run` / `save_state` raises | The exception |
| `on_turn(turn_index)` | Before each model call `run_tool_loop` makes | The turn number, from 0 |

```python?partial=true
def on_run_start(self, scope_key):
    self._scope_key = scope_key
    self._started = time.perf_counter()

def on_run_end(self, result):
    duration_ms = int((time.perf_counter() - self._started) * 1000)
    MyAuditLog.objects.create(scope_key=self._scope_key, duration_ms=duration_ms, status="ok")

def on_run_error(self, exc):
    MyAuditLog.objects.create(scope_key=self._scope_key, status="error", error=type(exc).__name__)
```

Hook failures are caught and logged by the platform — a broken
observability path can't crash the underlying run.

See [Auditing](/sdk/agents-auditing/) for the recommended split
between platform-owned and plugin-owned audit data.

## Concurrency

The platform runs one invocation at a time per agent and `scope_key`.
A second `RunAgentEffect` for the same agent and `scope_key` waits,
retrying with backoff for up to about 10 minutes, until the first run's
effects have been applied.

This lets `load_state` / `run` / `save_state` treat the underlying
storage as if no one else is touching it during the run, including
state the previous run wrote through its effects, such as protocol
cards or tasks.

**Picking a `scope_key`**: encode whatever should serialize. The scope
already includes your plugin and agent, so two agents never wait on
each other. Common shapes:

```python
# Patient-scoped — two runs on the same patient serialize.
f"patient:{patient_id}"

# Encounter-scoped — runs on the same encounter serialize, but the same
# patient on different encounters can run concurrently.
f"encounter:{encounter_id}"

# One clinician's conversation about one patient.
f"patient:{patient_id}:staff:{staff_id}"

# Instance-wide — only one run of this agent at a time. Useful for cron
# jobs you want strictly serialized.
"nightly_review"
```

Each Canvas instance serializes its own runs, so you don't need to
namespace by customer.

## The `AgentRunResult` shape

```python
from dataclasses import dataclass, field

from canvas_sdk.agents import AgentState
from canvas_sdk.effects import Effect


@dataclass
class AgentRunResult:
    state: AgentState
    effects: list[Effect] = field(default_factory=list)
```

`state` is what `save_state` will persist. `effects` is what the
platform will dispatch.

## `LLMGateway` shape

```python?partial=true
class LLMGateway:
    model: str  # the run's default model, "claude-sonnet-4-6"

    def client(self, *, max_retries: int = 2) -> Anthropic:
        """An Anthropic client pointed at the inference gateway."""
```

Built by the platform before `run()` is called, from the instance's
inference gateway URL and your plugin's `INFERENCE_GATEWAY_KEY` secret.
`client()` returns an `anthropic.Anthropic` client pointed at the
gateway. It carries that key and headers that attribute each call to
your plugin, agent, and run. See
[Credentials](/sdk/agents/#credentials) for the errors the gateway
returns.
