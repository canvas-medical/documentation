---
title: "Quick Start"
slug: "agents-quick-start"
excerpt: "Build an agent that tracks follow-up across visits with protocol cards."
---

This walks through a version of the reference plugin's
`LongitudinalCareAdvisor`. When a clinician locks a note, the agent
reviews the visit against the protocol cards it staged on earlier
visits, marks the ones the visit addressed as satisfied, and stages
cards for any new follow-up. It uses only the SDK's tools and keeps its
state in the chart itself, so it needs no Custom Data tables.

Agents reach Anthropic through Canvas's inference gateway. Your plugin
declares an `INFERENCE_GATEWAY_KEY` secret for its gateway key, and the
platform hands your agent a client built from it (see
[Credentials](/sdk/agents/#credentials)).

## 1. Register a tool catalog

Tools are declared at module-import time in a `ToolRegistry`. This
agent needs nothing beyond the SDK's `standard_tools`: patient-scoped
chart reads, plus `add_or_update_protocol_card` to stage and update
cards.

`my_plugin/agents/advisor_tools.py`:

```python
from canvas_sdk.agents import ToolRegistry, standard_tools

tools = ToolRegistry()
tools.extend(standard_tools)
```

Your manifest decides which of these tools the agent may use (step 4).
See [Tools](/sdk/agents-tools/) for writing your own.

## 2. Implement the agent

`my_plugin/agents/advisor.py`:

```python
import json
from typing import Any, cast

from anthropic.types import ToolUseBlock

from canvas_sdk.agents import AgentPlugin, AgentRunResult, AgentState, LLMGateway
from canvas_sdk.effects import Effect
from canvas_sdk.v1.data import ProtocolCurrent
from my_plugin.agents.advisor_tools import tools as _registered_tools

PLUGIN_NAME = "my_plugin"

SYSTEM_PROMPT = (
    "You are a longitudinal care advisor reviewing a patient's just-completed "
    "encounter. You maintain a small set of protocol cards on the patient that "
    "represent open clinical recommendations from prior visits.\n\n"
    "The user message lists the cards you staged before. For each one: if this "
    "visit addressed it, update it with the same `card_key` and "
    "`status='satisfied'`; if it no longer applies, use `status='not_relevant'`; "
    "otherwise leave it alone.\n\n"
    "Then call `add_or_update_protocol_card` for new follow-up this visit implies, "
    "with no `card_key`, `status='due'`, a short `title`, and a `narrative`. Stage "
    "three or fewer new cards. Check the chart with the read tools before you act, "
    "and end your turn when you are done."
)

MAX_TURNS = 10


def _existing_cards(patient_id: str) -> str:
    """List the cards this plugin staged on earlier visits, for the user message."""
    cards = ProtocolCurrent.objects.filter(
        patient__id=patient_id, plugin_name=PLUGIN_NAME
    ).order_by("-created")
    if not cards:
        return "No protocol cards from earlier visits."
    lines = ["Protocol cards from earlier visits:"]
    for card in cards:
        lines.append(f"- card_key={card.protocol_key!r} status={card.status!r} title={card.title!r}")
    return "\n".join(lines)


class LongitudinalCareAdvisor(AgentPlugin):
    """Reviews each locked note against the patient's open protocol cards."""

    # The platform replaces this with the tools your manifest grants before
    # run() fires. Always call self.tools, never the imported registry.
    tools = _registered_tools

    def load_state(self, scope_key: str) -> AgentState:
        """The cards are the state, and run() reads them from the chart."""
        return AgentState()

    def run(
        self,
        state: AgentState,
        gateway: LLMGateway,
        trigger_payload: dict[str, Any],
    ) -> AgentRunResult:
        patient_id = trigger_payload["patient_id"]
        effects: list[Effect] = []
        # The model never sees ctx. It scopes every tool to this patient and
        # collects the effects the tools stage.
        tool_ctx = {"patient_id": patient_id, "note_id": trigger_payload["note_id"], "effects": effects}

        client = gateway.client()
        messages: list[dict[str, Any]] = [
            {
                "role": "user",
                "content": (
                    "The patient just had a visit complete (note locked). Review the "
                    f"chart for follow-up needs.\n\n{_existing_cards(patient_id)}"
                ),
            }
        ]

        for _ in range(MAX_TURNS):
            response = client.messages.create(
                model=gateway.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=cast(Any, self.tools.definitions()),
                messages=cast(Any, messages),
            )
            messages.append({"role": "assistant", "content": response.content})

            tool_uses = [b for b in response.content if isinstance(b, ToolUseBlock)]
            if response.stop_reason not in ("tool_use", "max_tokens") or not tool_uses:
                break

            tool_results = []
            for block in tool_uses:
                try:
                    result = self.tools.execute(block.name, dict(block.input), ctx=tool_ctx)
                    content, is_error = json.dumps(result, default=str), False
                except Exception as exc:
                    content, is_error = f"Tool execution failed: {exc!s}", True
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": content,
                        "is_error": is_error,
                    }
                )
            messages.append({"role": "user", "content": tool_results})

        return AgentRunResult(state=state, effects=effects)

    def save_state(self, scope_key: str, state: AgentState) -> None:
        """Nothing to write: the protocol card effects are the state."""
        return None
```

The `AgentPlugin` contract is three methods: `load_state`, `run`, and
`save_state`. This agent's state is the protocol cards themselves, so
`load_state` and `save_state` do nothing and `run()` reads the cards
from the chart. A failed tool call goes back to the model as an
`is_error` result so it can try again, rather than ending the run.

The agent stages cards rather than draft commands because a locked note
can't take new commands. A card can still carry commands the clinician
runs in one click; see `add_or_update_protocol_card` in the
[catalog](/sdk/agents-tools/#the-sdk-standard_tools-catalog).

## 3. Trigger the agent

Agents don't subscribe to events. A regular handler does, and emits a
`RunAgentEffect` from `compute()`.

`my_plugin/handlers/advisor_trigger.py`:

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.agent import RunAgentEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from canvas_sdk.v1.data.note import CurrentNoteStateEvent, NoteStates


class LongitudinalCareAdvisorTrigger(BaseHandler):
    """Runs the advisor when a note is locked."""

    RESPONDS_TO = [EventType.Name(EventType.NOTE_STATE_CHANGE_EVENT_CREATED)]

    def compute(self) -> list[Effect]:
        state = CurrentNoteStateEvent.objects.values_list("state", flat=True).get(
            id=self.event.target.id
        )
        note_id = self.context.get("note_id")
        patient_id = self.context.get("patient_id")
        if state != NoteStates.LOCKED or not (note_id and patient_id):
            return []

        return [
            RunAgentEffect(
                agent_id="my_plugin.agents.advisor:LongitudinalCareAdvisor",
                scope_key=f"patient:{patient_id}",
                trigger_payload={"patient_id": patient_id, "note_id": note_id},
            ).apply()
        ]
```

`agent_id` is the agent's module path and class name, separated by a
colon; a plugin can only run its own agents. `scope_key` decides which
runs wait for each other. Runs of this agent on the same patient go one
at a time, and the next one starts only after the previous run's cards
have landed, so two notes locked in quick succession don't stage the
same card twice. See [Concurrency](/sdk/agents-lifecycle/#concurrency).

## 4. Wire it up in the manifest

```jsonc
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.handlers.advisor_trigger:LongitudinalCareAdvisorTrigger",
        "description": "Runs the longitudinal care advisor when a note is locked"
      }
    ],
    "agents": [
      {
        "class": "my_plugin.agents.advisor:LongitudinalCareAdvisor",
        "description": "Tracks follow-up across visits with protocol cards",
        "tools": {
          "allowed": ["@clinical_reads", "@clinical_alerts"]
        }
      }
    ]
  },
  "variables": [
    {"name": "INFERENCE_GATEWAY_KEY", "sensitive": true}
  ]
}
```

`tools.allowed` grants the chart reads and the alert tools (banner
alerts and protocol cards) by `@category`. It also bounds what the
agent can do: the platform drops any effect the agent returns that no
granted tool stages, so this agent can stage cards and banners but not
commands, tasks, or messages. An agent with no `tools.allowed` gets no
tools at all. See [Tools](/sdk/agents-tools/#manifest-driven-permissions).

## 5. Install and try it

```bash
canvas install my_plugin --host <your-instance> --secret INFERENCE_GATEWAY_KEY=<your-gateway-key>
```

Lock a note on a test patient. Within a few seconds the agent runs on
the worker, reads the chart, and stages protocol cards for the follow-up
it found. Lock another note on the same patient and it updates those
cards instead of repeating them.

## Next steps

- [Lifecycle](/sdk/agents-lifecycle/) — what the platform calls on
  your subclass and in what order.
- [Managing state](/sdk/agents-managing-state/) — when your agent needs
  to remember more than the chart records.
- [Tools](/sdk/agents-tools/) — designing your own read and effect tools.
- [Prompts](/sdk/agents-prompts/) — system-prompt patterns for clinical agents.
