---
title: "Testing"
slug: "agents-testing"
excerpt: "Patterns for testing AgentPlugin subclasses, tools, and the LLM loop without making real provider calls."
---

`AgentPlugin` is a regular Python class — `load_state`, `run`, and
`save_state` are testable directly, without spinning up the
plugin-runner. The only real friction is that `run()` typically calls
Anthropic, which you don't want firing in your unit tests. Stub the
LLM client and your agent becomes deterministically testable.

This page assumes the general SDK testing setup from
[Testing Utilities](/sdk/testing-utils/): `pytest` with the
`canvas[test-utils]` extra, and the model factories in
`canvas_sdk.test_utils.factories`. The examples test the agent from the
[Quick Start](/sdk/agents-quick-start/) and the tools defined on the
[Tools](/sdk/agents-tools/) page.

## Test each tool you write

A tool runs through its registry with `tools.execute(name, arguments,
ctx=...)`, so you can test it without the model. Tools are where your
business logic lives, which makes them the most worth testing.

```python
import pytest

from canvas_sdk.test_utils.factories import PatientFactory, TaskFactory
from my_plugin.agents.tools import tools


def test_create_followup_task_stages_one_labeled_task():
    """The tool stages an AddTask effect and returns its id to the model."""
    effects = []

    result = tools.execute(
        "create_followup_task",
        {"title": "Call patient about the A1c"},
        ctx={"patient_id": "b80b1cdc2e6a4aca90ccebc02e683f35", "effects": effects},
    )

    assert result["ok"] is True
    assert len(effects) == 1


@pytest.mark.django_db
def test_update_task_refuses_another_patients_task():
    """A task id the model supplies must belong to the run's patient."""
    other_patients_task = TaskFactory.create()
    effects = []

    with pytest.raises(ValueError, match="not found for this patient"):
        tools.execute(
            "update_task",
            {"task_id": str(other_patients_task.id), "status": "CLOSED"},
            ctx={"patient_id": PatientFactory.create().id, "effects": effects},
        )
    assert effects == []
```

Tests against real rows (the second test) catch ORM-level bugs, such as
a wrong filter or relation, that tests with mocked data miss.

## Stubbing the `LLMGateway`

Inside `run()`, your agent gets its Anthropic client from
`gateway.client()`. Pass `run()` a stand-in gateway whose `client()`
returns a mock, so no network call happens.

```python
from unittest.mock import MagicMock

import pytest
from anthropic.types import TextBlock, ToolUseBlock

from canvas_sdk.agents import LLMGateway


@pytest.fixture
def mock_client():
    """The client the agent receives from gateway.client(); queue responses on it."""
    return MagicMock()


@pytest.fixture
def gateway(mock_client):
    """A stand-in gateway whose client() returns mock_client."""
    gateway = MagicMock(spec=LLMGateway)
    gateway.model = "claude-sonnet-4-6"
    gateway.client.return_value = mock_client
    return gateway


def _response(*, content, stop_reason):
    """A minimal Anthropic-shaped response for the loop to consume."""
    response = MagicMock()
    response.content = content
    response.stop_reason = stop_reason
    return response


def _tool_use(name, input_dict, *, block_id="tu_1"):
    return ToolUseBlock(id=block_id, name=name, input=input_dict, type="tool_use")


def _text(text):
    return TextBlock(text=text, type="text")
```

These helpers are typically the only LLM-mocking infrastructure you
need. `_tool_use` and `_text` build real Anthropic blocks, so the
agent's `isinstance` checks behave as they do against the API.

## Driving the run loop in tests

Queue the responses you want the mock client to return, then drive
`run()` and assert on the result. Grant the agent its tools the way the
platform does (see [the next section](#simulating-the-platforms-tool-grant)).

```python?partial=true
@pytest.mark.django_db
def test_run_stages_a_card_for_new_follow_up(mock_client, gateway):
    """Two tool turns: the advisor reads the chart, then stages a card."""
    patient = PatientFactory.create()
    mock_client.messages.create.side_effect = [
        _response(content=[_tool_use("find_conditions", {}, block_id="tu_1")], stop_reason="tool_use"),
        _response(
            content=[
                _tool_use(
                    "add_or_update_protocol_card",
                    {"title": "Recheck A1c", "narrative": "Last A1c was 9.2.", "status": "due"},
                    block_id="tu_2",
                )
            ],
            stop_reason="tool_use",
        ),
        _response(content=[_text("done")], stop_reason="end_turn"),
    ]
    agent = _granted(LongitudinalCareAdvisor, ["@clinical_reads", "@clinical_alerts"])
    # The subject the platform would set from the trigger's RunAgentEffect.
    agent.subject = RunSubject(patient_id=patient.id)

    result = agent.run(AgentState(), gateway, {})

    assert len(result.effects) == 1
    assert mock_client.messages.create.call_count == 3
```

Walk-through:
- The `side_effect` is a list — each call to `messages.create()`
  returns the next response.
- `tool_use` responses make the agent's loop dispatch the named tool
  through `self.tools.execute(...)` and send the result back on the
  next turn.
- `end_turn` exits the loop.
- `result.effects` holds whatever the tools staged during the run.
- `RunSubject` is in `canvas_sdk.agents`. Set `staff_id` on it to test a
  run a staff member started.

## Simulating the platform's tool grant

Before `run()` fires, the platform replaces `agent.tools` with the
tools the manifest grants. After `run()`, it drops any returned effect
whose type no granted tool stages. Do the same in tests to exercise the
grant:

```python?partial=true
def _granted(agent_cls, allowed, denied=None):
    """Instantiate an agent with the tools a manifest grant would give it."""
    agent = agent_cls()
    agent.tools_allowed = agent_cls.tools.resolve_allowed(allowed, denied=denied)
    agent.tools = agent_cls.tools.scope(agent.tools_allowed)
    return agent


def _kept_by_platform(agent, effects):
    """The effects the platform would apply from a run of this agent."""
    granted = agent.tools.effect_types()
    return [e for e in effects if EffectType.Name(e.type) in granted]


def test_reads_only_grant_cannot_stage_cards():
    """Granted only chart reads, the advisor can neither call nor return card effects."""
    agent = _granted(LongitudinalCareAdvisor, ["@clinical_reads"])

    assert "add_or_update_protocol_card" not in {d["name"] for d in agent.tools.definitions()}
    with pytest.raises(ValueError, match="Unknown tool"):
        agent.tools.execute("add_or_update_protocol_card", {}, ctx={})
    assert agent.tools.effect_types() == frozenset()
```

`EffectType` is in `canvas_sdk.effects`. The scoped registry doesn't
contain ungranted tools at all, so a test for "the agent shouldn't be
able to do X" can assert on `Unknown tool` rather than checking
permission state.

## State transitions

For agents that aren't stateless, test `load_state` and `save_state`
independently of `run()`. They're plain methods. This example uses the
per-clinician chat agent from
[Managing State](/sdk/agents-managing-state/#pattern-2-snapshot):

```python?partial=true
@pytest.mark.django_db
def test_each_clinician_has_their_own_conversation():
    """One clinician's chat never becomes another's context."""
    patient = PatientFactory.create()
    first, second = ChatAgent(), ChatAgent()
    first.subject = RunSubject(patient_id=patient.id, staff_id=StaffFactory.create().id)
    second.subject = RunSubject(patient_id=patient.id, staff_id=StaffFactory.create().id)

    state = first.load_state("patient_and_staff")
    state.data["messages"] = [{"role": "user", "content": "How is her A1c trending?"}]
    first.save_state("patient_and_staff", state)

    assert second.load_state("patient_and_staff").data["messages"] == []
    assert len(first.load_state("patient_and_staff").data["messages"]) == 1
```

Tests that read or write your plugin's Custom Data need its tables in
the test database. The reference plugin's
[`tests/conftest.py`](https://github.com/canvas-medical/canvas-plugins/blob/main/example-plugins/agent_runner_poc/tests/conftest.py)
has a session fixture that creates them from your `CustomModel`
classes.

## Testing lifecycle hooks

If you've overridden `on_run_start` / `on_run_end` / `on_run_error`,
call them directly. The platform logs and swallows exceptions from
hooks, but that doesn't change their signatures.

```python?partial=true
@pytest.mark.django_db
def test_on_run_end_writes_audit_row():
    agent = MyAgent()
    agent.on_run_start("scope-key-1")

    agent.on_run_end(AgentRunResult(state=AgentState(), effects=[]))

    row = AgentRunLog.objects.get(scope_key="scope-key-1")
    assert row.status == "success"
    assert row.duration_ms is not None
```

## End-to-end runs

The unit and run-loop tests above cover your code. To see a real run —
the trigger firing, the run queued on the worker, the gateway call,
the effects landing in the chart — install the plugin on a development
instance with its `INFERENCE_GATEWAY_KEY` set and trigger it there.
Save that for a handful of golden-path scenarios per agent.

A useful split:

- **Unit** — individual tools, `load_state`/`save_state`, lifecycle
  hooks. Fast, no Anthropic mock needed.
- **Run-loop** — `run()` with a mocked Anthropic client. Exercises the
  tool-use dispatch, the tool grant, and the effects it returns.
- **End-to-end** — a few runs per agent on a development instance,
  checking that effects land where they should.

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
