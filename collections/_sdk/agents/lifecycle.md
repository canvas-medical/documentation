---
title: "Lifecycle"
slug: "agents-lifecycle"
excerpt: "What your AgentPlugin subclass implements, and what the platform does around it."
---

`AgentPlugin` is the abstract base class for every agent. You implement
three methods (`load_state`, `run`, `save_state`); the platform handles
dispatch, locking, hook invocation, and effect delivery around them.

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

When a `RunAgentEffect` reaches the plugin-runner's `RunAgent` RPC, the
following happens. Each step is platform-driven, and steps 4 through
10 run inside the per-`scope_key` lock:

1. **Resolve the agent class** from `LOADED_PLUGINS` by `agent_id`.
2. **Build the `LLMGateway`** from the instance's inference gateway
   configuration, attributed to your plugin, this agent, and this run.
   If the instance has no gateway configured, the run stops here with
   `error_kind="LLM_NOT_CONFIGURED"`.
3. **Acquire the per-`scope_key` lock**. If another invocation holds
   it, the run returns `success=False` with `error_kind="AGENT_LOCKED"`;
   the Celery task auto-retries with exponential backoff. See
   [Concurrency](#concurrency) below.
4. **Instantiate your subclass** (`agent_class()` with no arguments).
5. **Apply the manifest tool allowlist.** The platform expands
   `tools.allowed` (tool names and `@category` groups) against
   `agent.tools`, subtracts `tools.denied`, sets `agent.tools_allowed`
   to the result, and replaces `agent.tools` with a scoped view
   containing only those tools. An agent entry with no `tools.allowed`
   keeps its full registry.
6. **Call `on_run_start(scope_key)`** (optional hook; default no-op).
7. **Call `load_state(scope_key)`** to get the run's starting state.
8. **Call `run(state, gateway, trigger_payload)`** — the body of your
   agent.
9. **Call `save_state(scope_key, result.state)`** with the updated
   state from your `AgentRunResult`.
10. **Call `on_run_end(result)`** (optional hook).
11. **Release the lock.**
12. **Stamp provenance on each emitted effect** (`plugin_name`,
    `handler_name`, `actor`, `source`) and stream them
    back to the home-app worker for dispatch through
    `handle_effect`.

If any of steps 7–9 raises, `on_run_error(exc)` fires, the exception
is captured to Sentry, and the run returns `success=False`. Errors from
the inference gateway are classified rather than captured: an outage
(`error_kind="LLM_UNAVAILABLE"`) is retried, and a refusal
(`error_kind="LLM_REFUSED"`) fails the run without a retry.

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

```python
def run(self, state, gateway, trigger_payload):
    effects: list[Effect] = []
    tool_ctx = {"patient_id": trigger_payload["patient_id"], "effects": effects}
    # ... LLM loop using self.tools ...
    return AgentRunResult(state=state, effects=effects)
```

The `effects` list is what the platform will dispatch *after* `run()`
returns and `save_state()` commits — the platform owns *when* effects
emit; your agent owns *what*. This split keeps idempotency clean:
because save and dispatch are both bracketed by the lock, a retry
sees the same starting state, decides the same effects, and the
platform can apply dedup if it's seen the run before.

### `save_state(scope_key, state) -> None`

Called once per run, after `run()` returns. Persist `state.data`
back to wherever you read it from. For stateless agents this is a
no-op.

`save_state` runs **inside the lock**. A concurrent `RunAgentEffect`
for the same `scope_key` is held off until you return.

## Optional hooks

`AgentPlugin` declares four lifecycle hooks. Override them in your
subclass to capture observability data without polluting `run()`.

| Hook | When it fires | What it receives |
|---|---|---|
| `on_run_start(scope_key)` | After instantiation, before `load_state` | The scope_key for this run |
| `on_run_end(result)` | After `save_state` succeeds | The `AgentRunResult` |
| `on_run_error(exc)` | If any of `load_state` / `run` / `save_state` raises | The exception |
| `on_turn(turn_index)` | Per-turn (not wired in preview — coming soon) | The turn number |

```python
def on_run_start(self, scope_key):
    self._started = time.perf_counter()

def on_run_end(self, result):
    duration_ms = int((time.perf_counter() - self._started) * 1000)
    MyAuditLog.objects.create(scope_key=scope_key, duration_ms=duration_ms, status="ok")

def on_run_error(self, exc):
    MyAuditLog.objects.create(scope_key=scope_key, status="error", error=type(exc).__name__)
```

Hook failures are caught and logged by the platform — a broken
observability path can't crash the underlying run.

See [Auditing](/sdk/agents-auditing/) for the recommended split
between platform-owned and plugin-owned audit data.

## Concurrency

The platform serializes invocations per-`scope_key`. Two
`RunAgentEffect`s with the same `scope_key` cannot run at the same
time; the second is held off until the first completes (lock + retry
with exponential backoff).

This lets `load_state` / `run` / `save_state` treat the underlying
storage as if no one else is touching it during the run.

**Picking a `scope_key`**: encode whatever should serialize. Common
shapes:

```python
# Patient-scoped — two runs on the same patient serialize.
f"my_plugin:chart_summary:patient:{patient_id}"

# Patient-and-encounter-scoped — runs on the same encounter serialize,
# but the same patient on different encounters can run concurrently.
f"my_plugin:visit_summary:encounter:{encounter_id}"

# Tenant-wide — only one run anywhere at a time. Useful for cron jobs
# you want strictly serialized.
"my_plugin:nightly_review"
```

Tenant isolation is automatic (the lock storage prefixes keys with
the customer identifier), so you don't need to namespace by customer.

## The `AgentRunResult` shape

```python
@dataclass
class AgentRunResult:
    state: AgentState
    effects: list[Effect]
```

`state` is what `save_state` will persist. `effects` is what the
platform will dispatch.

## `LLMGateway` shape

```python?partial=true
class LLMGateway:
    model: str  # the run's default model, "claude-sonnet-4-6"

    def client(self, *, max_retries: int = 2) -> Anthropic:
        """An Anthropic client that reaches only the inference gateway."""
```

Built by the platform from the instance's inference gateway
configuration before `run()` is called. It exposes no key: `client()`
returns an `anthropic.Anthropic` client whose own key is a placeholder,
and the real key and attribution headers are added beneath it on each
request. The client refuses requests to any other host and to any
endpoint besides the Messages API and token counting. See
[Credentials](/sdk/agents/#credentials) for the errors the gateway
returns.
