---
title: "Testing"
slug: "agents-testing"
excerpt: "Patterns for testing AgentPlugin subclasses, tools, and the LLM loop without making real provider calls."
---

`AgentPlugin` is a regular Python class — `load_state`, `run`, and
`save_state` are testable directly, without spinning up the
plugin-runner harness. The only real friction is that `run()`
typically calls Anthropic, which you don't want firing in your unit
tests. Stub the LLM client and your agent becomes deterministically
testable.

This page assumes you have the general SDK testing setup from
[Testing Utilities](/sdk/testing-utils/). The patterns below build on
that.

## Test the executor of each tool first

Tool executors are pure functions: `fn(arguments, *, ctx) -> Any`.
They're the easiest part of an agent to test, and the most worth
testing because the executor is where your business logic lives.

```python
from my_plugin.agents.chart_summary_tools import (
    _originate_plan,
    _list_active_conditions,
)


def test_originate_plan_appends_effect_to_accumulator():
    """The tool stages a Plan command effect and returns ok."""
    effects = []
    ctx = {"patient_id": "p1", "note_id": "n1", "effects": effects}

    result = _originate_plan({"narrative": "Recheck A1c in 3 months"}, ctx=ctx)

    assert result == {"ok": True}
    assert len(effects) == 1
    # The effect is what the platform will dispatch after run() returns.


def test_list_active_conditions_filters_to_patient(patient_factory, condition_factory):
    """Tool reads are patient-scoped via ctx — model arguments can't widen."""
    target = patient_factory()
    other = patient_factory()
    condition_factory(patient=target, code="E11.9", display="Type 2 diabetes")
    condition_factory(patient=other, code="I10", display="Hypertension")

    result = _list_active_conditions({}, ctx={"patient_id": target.id})

    codes = {c["code"] for c in result}
    assert codes == {"E11.9"}
```

The second test uses `factory_boy`-style fixtures from
`canvas[test-utils]` (see [Testing Utilities](/sdk/testing-utils/)).
Tool tests against real data are the most valuable layer — they
catch ORM-level bugs (wrong filter, wrong relation traversal) that
mocked-data tests miss.

## Stubbing the `LLMGateway`

Inside `run()`, your agent instantiates an Anthropic client from
`gateway.api_key`. Replace the client in tests so no real provider
call happens.

```python
from unittest.mock import patch, MagicMock

import pytest
from anthropic.types import TextBlock, ToolUseBlock

from canvas_sdk.agents import AgentState, LLMGateway
from my_plugin.agents.chart_summary import ChartSummary


@pytest.fixture
def gateway():
    """A fake gateway that satisfies the dataclass without exercising HTTP."""
    return LLMGateway(api_key="sk-fake", model="claude-sonnet-4-6")


def _response(*, content, stop_reason):
    """Build a minimal Anthropic-shaped response object for the loop to consume."""
    response = MagicMock()
    response.content = content
    response.stop_reason = stop_reason
    return response


def _tool_use(name, input_dict, *, block_id="tu_1"):
    block = MagicMock(spec=ToolUseBlock)
    block.type = "tool_use"
    block.id = block_id
    block.name = name
    block.input = input_dict
    return block


def _text(text):
    block = MagicMock(spec=TextBlock)
    block.type = "text"
    block.text = text
    return block
```

These three helpers (`_response`, `_tool_use`, `_text`) are typically
the only LLM-mocking infrastructure you need.

## Driving the run loop in tests

The pattern: queue the responses you want the mock Anthropic client
to return, then drive `run()` and assert on the result.

```python
@patch("my_plugin.agents.chart_summary.Anthropic")
def test_run_drafts_plan_from_tool_results(
    mock_anthropic_cls, gateway, patient_factory
):
    """Two-turn run: agent calls a read tool, then originates the Plan."""
    patient = patient_factory()
    mock_client = MagicMock()
    mock_anthropic_cls.return_value = mock_client

    # Turn 1: model calls find_conditions.
    # Turn 2: model calls originate_plan with a narrative, then ends.
    mock_client.messages.create.side_effect = [
        _response(
            content=[_tool_use("find_conditions", {}, block_id="tu_1")],
            stop_reason="tool_use",
        ),
        _response(
            content=[
                _tool_use(
                    "originate_plan",
                    {"narrative": "Recheck A1c in 3 months."},
                    block_id="tu_2",
                ),
            ],
            stop_reason="tool_use",
        ),
        _response(content=[_text("done")], stop_reason="end_turn"),
    ]

    agent = ChartSummary()
    result = agent.run(
        AgentState(),
        gateway,
        {"patient_id": patient.id, "note_id": "note-uuid"},
    )

    # The accumulator should have the originated Plan command.
    assert len(result.effects) == 1
    # Three turns happened: find_conditions, originate_plan, end_turn.
    assert mock_client.messages.create.call_count == 3
```

Walk-through:
- The `side_effect` is a list — each call to `messages.create()`
  pops the next response.
- `tool_use` responses cause the agent's loop to dispatch the named
  tool through `self.tools.execute(...)` and append the result on the
  next turn.
- `end_turn` exits the loop.
- The accumulator (`result.effects`) holds whatever effect tools
  staged during the run.

## Simulating the platform's manifest-scoping

Recall that the platform replaces `agent.tools` with a scoped view
before `run()` fires. In tests you do this yourself if you want to
exercise the filter.

```python
def _make_agent(agent_cls, tools_allowed=None):
    """Instantiate an agent the way the platform would."""
    agent = agent_cls()
    if tools_allowed is not None:
        agent.tools_allowed = frozenset(tools_allowed)
        agent.tools = agent_cls.tools.scope(agent.tools_allowed)
    return agent
```

Use this anywhere `tools.allowed` matters to what you're testing:

```python
def test_run_cannot_use_disallowed_tool(gateway):
    """When the manifest withholds a tool, the agent can't call it."""
    agent = _make_agent(ChartSummary, tools_allowed={"find_conditions"})

    # find_conditions is in the scope, originate_plan is not.
    assert {"find_conditions"} == {
        d["name"] for d in agent.tools.definitions()
    }
    with pytest.raises(ValueError, match="Unknown tool"):
        agent.tools.execute("originate_plan", {"narrative": "..."}, ctx={})
```

The scoped registry doesn't contain disallowed entries at all — a
test for "the agent shouldn't be able to do X" can assert on
`Unknown tool` rather than checking permission state.

## State transitions

For agents that aren't stateless, test `load_state` and `save_state`
independently of `run()`. They're plain methods.

```python
def test_load_state_returns_existing_messages(patient_factory, conversation_factory):
    """load_state pulls the conversation snapshot for this patient."""
    patient = patient_factory()
    conversation_factory(
        patient=patient,
        messages=[{"role": "user", "content": "hi"}],
    )

    state = ChartChatAgent().load_state(
        f"my_plugin:chart_chat:patient:{patient.id}"
    )

    assert state.data["messages"] == [{"role": "user", "content": "hi"}]
    assert state.data["patient_id"] == patient.id


def test_save_state_writes_back_appended_messages(patient_factory):
    """save_state persists the (mutated) state.data['messages'] list."""
    patient = patient_factory()
    state = AgentState(
        data={
            "patient_id": patient.id,
            "messages": [
                {"role": "user", "content": "hi"},
                {"role": "assistant", "content": "hello"},
            ],
        }
    )

    ChartChatAgent().save_state(
        f"my_plugin:chart_chat:patient:{patient.id}",
        state,
    )

    from my_plugin.models import Conversation
    row = Conversation.objects.get(patient__id=patient.id)
    assert len(row.messages) == 2
```

End-to-end coverage of the snapshot pattern: write a `load_state →
run → save_state` test that mocks the Anthropic loop and asserts on
the final row in your CustomModel table.

## Testing lifecycle hooks

If you've overridden `on_run_start` / `on_run_end` / `on_run_error`
(for example, via a `RunLoggingMixin`), invoke them directly. The
platform's `_invoke_agent_hook` helper that swallows hook
exceptions doesn't change their signatures.

```python
def test_on_run_end_writes_audit_row(patient_factory):
    agent = MyAgent()
    agent.on_run_start("scope-key-1")

    agent.on_run_end(AgentRunResult(state=AgentState(), effects=[]))

    from my_plugin.models import AgentRunLog
    row = AgentRunLog.objects.get(scope_key="scope-key-1")
    assert row.status == "success"
    assert row.duration_ms is not None
```

If you want to verify the platform's "swallow hook exceptions"
behavior in your own code, raise from the hook and assert that
something downstream still works. (You usually don't need to — the
SDK's plugin-runner tests cover that path.)

## Integration tests through the plugin-runner

For end-to-end coverage — a real `RunAgentEffect` flowing from a
trigger through Celery and the gRPC RunAgent RPC — Canvas's
plugin test fixtures install your plugin into a test plugin-runner
and let you assert on emitted effects via `handle_effect`.
This is heavier than the unit patterns above and typically saved
for a handful of golden-path scenarios per agent. See
[Testing Utilities](/sdk/testing-utils/) for the full setup.

A useful split:

- **Unit** — individual tool executors, `load_state`/`save_state`,
  lifecycle hooks. Fast, no Anthropic mock needed.
- **Run-loop** — `run()` with a mocked Anthropic client. Exercises
  the tool-use dispatch and the effects accumulator.
- **Integration** — one or two end-to-end runs per agent, asserting
  that effects land where they should. Slow; uses the test
  plugin-runner.

## Don't pin to real provider responses

It's tempting to record real Anthropic responses and replay them.
That's a brittle test foundation — the model's tool-call sequence
varies run-to-run, the response shape evolves with API versions, and
the cost is borne by your CI. Hand-built canned responses (the
`_response` / `_tool_use` / `_text` helpers above) give you tests
that exercise *your* loop logic, not the model's tendencies.

Real-provider tests belong in an evals harness — a small set of
representative `trigger_payload`s you run manually before releases.
See [Auditing](/sdk/agents-auditing/) for the evals/replay story.
