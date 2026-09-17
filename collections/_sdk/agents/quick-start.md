---
title: "Quick Start"
slug: "agents-quick-start"
excerpt: "Build a minimal agent that drafts a Plan command on note creation."
---

This walks through the smallest possible agent — a triggered, stateless
one that reads the chart on note creation and drafts a Plan command for
the clinician to edit and commit. ~50 lines of agent code, plus a
manifest entry and a trigger handler.

## 1. Configure the plugin secret

Your manifest declares the Anthropic API key as a plugin variable; the
customer's admin sets the value once the plugin is installed.

`CANVAS_MANIFEST.json`:

```jsonc
{
  "variables": [
    {"name": "ANTHROPIC_API_KEY", "sensitive": true},
    {"name": "ANTHROPIC_MODEL", "sensitive": false}
  ]
}
```

`ANTHROPIC_MODEL` is optional; the SDK defaults to `claude-sonnet-4-6`.

## 2. Register a tool catalog

Tools are pre-declared at module-import time and registered into a
`ToolRegistry`. Start with the SDK's `standard_tools` (clinical reads
with patient-scope built in) and layer your own.

`chart_summary_tools.py`:

```python
from canvas_sdk.agents import ToolRegistry, standard_tools
from canvas_sdk.commands import PlanCommand

tools = ToolRegistry()
tools.extend(standard_tools)  # find_medications, find_conditions, etc.


@tools.tool(
    name="originate_plan",
    description=(
        "Stage a Plan command on the patient's current note. Call this "
        "exactly once with the narrative as plain text — no preamble, "
        "no headings, no markdown, <= 3 sentences."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "narrative": {"type": "string"},
        },
        "required": ["narrative"],
    },
)
def _originate_plan(arguments, *, ctx):
    """Stage a draft Plan command into the agent's effects accumulator."""
    effects = ctx["effects"]
    note_id = ctx["note_id"]
    narrative = arguments["narrative"].strip()
    effects.append(PlanCommand(note_uuid=note_id, narrative=narrative).originate())
    return {"ok": True}
```

See [Tools](/sdk/agents-tools/) for the full registry / executor /
permission model.

## 3. Implement the agent

`chart_summary.py`:

```python
from typing import Any, cast

from anthropic import Anthropic
from anthropic.types import ToolUseBlock

from my_plugin.agents.chart_summary_tools import tools as _registered_tools
from canvas_sdk.agents import AgentPlugin, AgentRunResult, AgentState, LLMGateway
from canvas_sdk.effects import Effect
from canvas_sdk.v1.data import Patient

SYSTEM_PROMPT = (
    "You are a clinical documentation assistant drafting a follow-up "
    "Plan-section narrative for a newly-created encounter note. You "
    "have read tools to inspect the patient's chart. Read the chart, "
    "draft a concise Plan grounded in what you found, then call "
    "`originate_plan` exactly once with the narrative as plain text "
    "(<= 3 sentences, no preamble, no headings, no markdown)."
)

MAX_TURNS = 8


class ChartSummary(AgentPlugin):
    """Drafts a Plan command for a new note via tool-driven chart reads."""

    # The platform scopes this to the manifest's tools.allowed before
    # run() fires. Always use `self.tools`, not the imported `_registered_tools`.
    tools = _registered_tools

    def load_state(self, scope_key: str) -> AgentState:
        """Stateless agent — no prior state to load."""
        return AgentState()

    def run(
        self,
        state: AgentState,
        gateway: LLMGateway,
        trigger_payload: dict[str, Any],
    ) -> AgentRunResult:
        patient_id = trigger_payload["patient_id"]
        note_id = trigger_payload["note_id"]
        patient = Patient.objects.get(id=patient_id)

        # Effects accumulator + per-run context for tools.
        effects: list[Effect] = []
        tool_ctx = {"patient_id": patient_id, "note_id": note_id, "effects": effects}

        client = Anthropic(api_key=gateway.api_key)
        messages: list[dict[str, Any]] = [
            {
                "role": "user",
                "content": (
                    f"Draft a follow-up Plan for {patient.first_name} "
                    f"{patient.last_name}. Inspect the chart with the "
                    "read tools, then call `originate_plan` once."
                ),
            }
        ]

        for _ in range(MAX_TURNS):
            response = client.messages.create(
                model=gateway.model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=cast(Any, self.tools.definitions()),
                messages=cast(Any, messages),
            )
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                break

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if not isinstance(block, ToolUseBlock):
                        continue
                    try:
                        result = self.tools.execute(
                            block.name, dict(block.input), ctx=tool_ctx
                        )
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        })
                    except Exception as exc:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Tool failed: {exc}",
                            "is_error": True,
                        })
                messages.append({"role": "user", "content": tool_results})
                continue

            break

        return AgentRunResult(state=state, effects=effects)

    def save_state(self, scope_key: str, state: AgentState) -> None:
        """Stateless — nothing to persist."""
        return None
```

The `AgentPlugin` contract is three methods: `load_state`, `run`, and
`save_state`. For this stateless agent both `load_state` and
`save_state` are no-ops. The `run()` method drives the tool-use loop
and accumulates effects.

## 4. Trigger the agent

Agents don't subscribe to events directly. A regular handler does, and
emits a `RunAgentEffect` from `compute()`.

`triggers.py`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.agent import RunAgentEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.note import CurrentNoteStateEvent, NoteStates


class ChartSummaryTrigger(BaseHandler):
    """Fires the ChartSummary agent when a note is created."""

    RESPONDS_TO = [EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)]

    def compute(self) -> list[Effect]:
        # Only fire on note creation (NEW state).
        state = CurrentNoteStateEvent.objects.values_list("state", flat=True).get(
            id=self.event.target.id
        )
        if state != NoteStates.NEW:
            return []

        note_id = self.context.get("note_id")
        patient_id = self.context.get("patient_id")
        if not (note_id and patient_id):
            return []

        return [
            RunAgentEffect(
                agent_id="my_plugin.agents.chart_summary:ChartSummary",
                scope_key=f"my_plugin:chart_summary:patient:{patient_id}",
                trigger_payload={"patient_id": patient_id, "note_id": note_id},
            ).apply()
        ]
```

`agent_id` is the colon-separated module path + class name.
`scope_key` is yours to shape — by convention, prefix with plugin name
and agent identity so two agents on the same patient don't serialize
against each other. The platform uses it as the lock key.

## 5. Wire it up in the manifest

```jsonc
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.triggers:ChartSummaryTrigger",
        "description": "Emits RunAgentEffect on note creation"
      }
    ],
    "agents": [
      {
        "class": "my_plugin.agents.chart_summary:ChartSummary",
        "description": "Drafts a Plan command on the new note",
        "tools": {
          "allowed": [
            "find_medications",
            "find_conditions",
            "find_lab_results",
            "get_patient_demographics",
            "originate_plan"
          ]
        }
      }
    ]
  }
}
```

The `tools.allowed` list authorizes specific tools by name. The
platform reads this and scopes `self.tools` at run time — see
[Tools](/sdk/agents-tools/).

## 6. Install + test

```bash
canvas install my_plugin --host <your-instance>
```

Configure `ANTHROPIC_API_KEY` on the plugin's admin page, then create a
new note in the chart. Within a few seconds the agent should run on
the worker, call the chart-read tools, and stage a draft Plan command
on the new note.

## Next steps

- [Lifecycle](/sdk/agents-lifecycle/) — what the platform calls on
  your subclass and in what order.
- [Managing state](/sdk/agents-managing-state/) — for agents that
  need to remember things across runs.
- [Tools](/sdk/agents-tools/) — designing your own read and effect tools.
- [Prompts](/sdk/agents-prompts/) — system-prompt patterns for clinical agents.
