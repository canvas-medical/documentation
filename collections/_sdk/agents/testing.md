---
title: "Testing"
slug: "agents-testing"
excerpt: "Patterns for testing AgentPlugin subclasses, tools, and the LLM loop without making real provider calls."
---

`AgentPlugin` is a regular Python class — `load_state`, `run`, and
`save_state` are testable directly, without spinning up the
plugin-runner. The only real friction is that `run()` typically calls
Anthropic, which you don't want firing in your unit tests. Stub the
LLM gateway and your agent becomes deterministically testable.

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

## Running an agent against a fake gateway

`canvas_sdk.test_utils.agents` runs an agent the way the platform does,
with a fake inference gateway in place of Anthropic:

- `FakeGateway(*replies)` answers each model call with the next reply,
  or raises it when it is an exception, such as an outage. It keeps a
  copy of each request on `gateway.requests`, so a test can check what
  the agent sent the model.
- `reply(*blocks)` builds a model reply from `text(...)` and
  `tool_use(name, input)` blocks. Its stop reason is `tool_use` when it
  calls a tool and `end_turn` otherwise; pass `stop_reason=` to test
  another.
- `prepare_agent(AgentClass, allowed=..., denied=..., subject=...)`
  sets up the agent as the platform does before a run: it applies the
  manifest's tool grant, sets `self.subject`, and gives the run an id.
- `run_agent(agent, gateway, trigger_payload)` calls the lifecycle
  methods and hooks in the platform's order and returns what the run
  did: the effects the platform would apply (`run.effects`), the ones
  the grant drops (`run.dropped`), the model calls, the tool calls, and
  how the last tool loop ended. Unlike the platform, an exception from
  the run reaches your test.

The blocks are real Anthropic types, so the tool loop behaves as it
does against the API.

```python?partial=true
import pytest

from canvas_sdk.agents import RunSubject
from canvas_sdk.effects import EffectType
from canvas_sdk.test_utils.agents import FakeGateway, prepare_agent, reply, run_agent, text, tool_use
from canvas_sdk.test_utils.factories import PatientFactory
from my_plugin.agents.advisor import LongitudinalCareAdvisor

# The advisor's grant in CANVAS_MANIFEST.json.
GRANT = ["@clinical_reads", "@clinical_alerts"]


@pytest.mark.django_db
def test_the_advisor_stages_a_card_for_new_follow_up():
    """The advisor reads the chart, then stages a card the platform applies."""
    agent = prepare_agent(
        LongitudinalCareAdvisor,
        allowed=GRANT,
        subject=RunSubject(patient_id=PatientFactory.create().id),
    )
    gateway = FakeGateway(
        reply(tool_use("find_conditions")),
        reply(
            tool_use(
                "add_or_update_protocol_card",
                {"title": "Recheck A1c", "narrative": "Last A1c was 9.2.", "status": "due"},
            )
        ),
        reply(text("Staged one card.")),
    )

    run = run_agent(agent, gateway)

    assert [effect.type for effect in run.effects] == [EffectType.ADD_OR_UPDATE_PROTOCOL_CARD]
    assert [call.name for call in run.tool_calls] == ["find_conditions", "add_or_update_protocol_card"]
```

Set `staff_id` on the `RunSubject` to test a run a staff member
started.

## Testing the tool grant

`prepare_agent` scopes `agent.tools` to the grant exactly as the
platform does, and `run_agent` drops returned effects no granted tool
stages. A test for "the agent can't do X" can check either:

```python?partial=true
def test_a_reads_only_grant_cannot_stage_cards():
    """Granted only chart reads, the advisor can neither call nor return card effects."""
    agent = prepare_agent(LongitudinalCareAdvisor, allowed=["@clinical_reads"])

    assert "add_or_update_protocol_card" not in {d["name"] for d in agent.tools.definitions()}
    with pytest.raises(ValueError, match="Unknown tool"):
        agent.tools.execute("add_or_update_protocol_card", {}, ctx={})
    assert agent.tools.effect_types() == frozenset()
```

The scoped registry doesn't contain ungranted tools at all, so a model
asking for one gets an `Unknown tool` error back, which `run.tool_calls`
records as a failed call.

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
    first = prepare_agent(
        ChatAgent, subject=RunSubject(patient_id=patient.id, staff_id=StaffFactory.create().id)
    )
    second = prepare_agent(
        ChatAgent, subject=RunSubject(patient_id=patient.id, staff_id=StaffFactory.create().id)
    )

    state = first.load_state("patient_and_staff")
    state.data["messages"] = [{"role": "user", "content": "How is her A1c trending?"}]
    first.save_state("patient_and_staff", state)

    assert second.load_state("patient_and_staff").data["messages"] == []
    assert len(first.load_state("patient_and_staff").data["messages"]) == 1
```

Tests that read or write your plugin's Custom Data need its tables in
the test database. `pytest-canvas` 0.2.0 and later, which the
`canvas[test-utils]` extra installs, creates them from the
`CustomModel` classes in your plugin's `models/` directory.

## Testing lifecycle hooks

If you've overridden `on_run_start` / `on_run_end` / `on_run_error`,
call them directly. The platform logs and swallows exceptions from
hooks, but that doesn't change their signatures. Set `run_id` the way
the platform would when your hook writes it, as the
[Auditing](/sdk/agents-auditing/#recommended-pattern) pattern does:

```python?partial=true
@pytest.mark.django_db
def test_on_run_end_records_the_decision():
    agent = MyAgent()
    agent.run_id = "6f1c2a8e-0d5b-4b9a-9a52-1c3f6a0e2b7d"
    agent._rationale = "Last A1c was 9.2 with no recheck since March."
    agent._grounding_facts = {}

    agent.on_run_end(AgentRunResult(state=AgentState(), effects=[]))

    row = AdvisorDecision.objects.get(run_id=agent.run_id)
    assert row.rationale.startswith("Last A1c")
```

## End-to-end runs

The unit and run-loop tests above cover your code. To see a real run —
the trigger firing, the run queued on the worker, the gateway call,
the effects landing in the chart — install the plugin on a development
instance with its `INFERENCE_GATEWAY_KEY` set and trigger it there.
Save that for a handful of golden-path scenarios per agent.

A useful split:

- **Unit** — individual tools, `load_state`/`save_state`, lifecycle
  hooks. Fast, no gateway needed.
- **Run-loop** — `run_agent` with a `FakeGateway`. Exercises the
  tool-use dispatch, the tool grant, and the effects it returns.
- **End-to-end** — a few runs per agent on a development instance,
  checking that effects land where they should.

## Don't pin to real provider responses

It's tempting to record real Anthropic responses and replay them.
That's a brittle test foundation — the model's tool-call sequence
varies run-to-run, the response shape evolves with API versions, and
the cost is borne by your CI. Hand-built canned replies (`reply`,
`tool_use`, and `text` above) give you tests
that exercise *your* loop logic, not the model's tendencies.

Real-provider tests belong in an evals harness — a small set of
representative `trigger_payload`s you run manually before releases.
See [Auditing](/sdk/agents-auditing/) for the evals/replay story.
