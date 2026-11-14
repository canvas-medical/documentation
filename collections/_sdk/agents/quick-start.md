---
title: "Quick Start"
slug: "agents-quick-start"
excerpt: "Build an agent that tracks follow-up across visits with protocol cards."
---

This walks through `LongitudinalCareAdvisor`, an agent that tracks
follow-up across visits. When a clinician locks a note, the agent
reviews the visit against the protocol cards it staged on earlier
visits, marks the ones the visit addressed as satisfied, and stages
cards for any new follow-up. It uses only the SDK's tools and keeps its
state in the chart itself, so it needs no Custom Data tables.

Agents reach Anthropic through Canvas's inference gateway. Your plugin
declares an `INFERENCE_GATEWAY_URL` variable for the gateway's address
and an `INFERENCE_GATEWAY_KEY` secret for its gateway key, and the
platform hands your agent a client built from them (see
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

```python?partial=true
import json
from typing import Any

from canvas_sdk.agents import AgentPlugin, AgentRunResult, AgentState, LLMGateway
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


def _cards_text(cards: list[dict[str, Any]]) -> str:
    """The cards this plugin staged on earlier visits, for the user message."""
    if not cards:
        return "No protocol cards from earlier visits."
    return f"Protocol cards from earlier visits:\n{json.dumps(cards, indent=1)}"


class LongitudinalCareAdvisor(AgentPlugin):
    """Reviews each locked note against the patient's open protocol cards."""

    # The platform replaces this with the tools your manifest grants before
    # run() fires. Always call self.tools, never the imported registry.
    tools = _registered_tools

    def load_state(self, scope_key: str) -> AgentState:
        """The cards this plugin staged on the patient: this agent's state.

        Read through find_protocol_cards, the same tool the model has, so the
        cards come from one query in one shape, within the run's patient.
        """
        cards = self.tools.execute(
            "find_protocol_cards",
            {"plugin_name": PLUGIN_NAME},
            ctx=self.tool_context(),
        )
        return AgentState(data={"cards": cards})

    def run(
        self,
        state: AgentState,
        gateway: LLMGateway,
        trigger_payload: dict[str, Any],
    ) -> AgentRunResult:
        cards = _cards_text(state.data["cards"])
        messages = [
            {
                "role": "user",
                "content": (
                    "The patient just had a visit complete (note locked). Review the "
                    f"chart for follow-up needs.\n\n{cards}"
                ),
            }
        ]
        # Calls the model with this agent's granted tools until it ends its turn.
        # Every tool acts on self.subject's patient.
        result = self.run_tool_loop(
            gateway, system=SYSTEM_PROMPT, messages=messages, max_turns=MAX_TURNS
        )

        return AgentRunResult(state=state, effects=result.effects)

    def save_state(self, scope_key: str, state: AgentState) -> None:
        """Nothing to write: the cards change only through the run's effects."""
        return None
```

The `AgentPlugin` contract is three methods: `load_state`, `run`, and
`save_state`. This agent's state is the protocol cards themselves:
`load_state` reads them through the agent's own `find_protocol_cards`
tool, and `save_state` does nothing, because the cards change only
through the effects the run returns. Runs on the same patient happen one
at a time, so `load_state` sees the cards the previous run staged.
`self.tool_context()` builds the context a tool call gets from the run's
subject; outside the tool loop it has no gateway, which only the tools
that make model calls of their own need.

`run_tool_loop` does the back-and-forth with the model: it calls the
model with the agent's granted tools, runs each tool call through
`self.tools`, sends the results back, and repeats until the model ends
its turn or `max_turns` is reached. A failed tool call goes back to the
model as an error so it can try again, rather than ending the run. See
[Lifecycle](/sdk/agents-lifecycle/#running-the-model-with-run_tool_loop)
for everything it handles.

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
                scope=RunAgentEffect.Scope.PATIENT,
                patient_id=patient_id,
                note_id=note_id,
            ).apply()
        ]
```

`agent_id` is the agent's module path and class name, separated by a
colon; a plugin can only run its own agents. `patient_id` and `note_id`
are the run's subject: the platform checks them and hands them to the
agent as `self.subject`. `scope` decides which runs wait for each
other. Runs of this agent on the same patient go one at a time, and the
next one starts only after the previous run's cards have landed, so
when two notes are locked in quick succession, the second run sees the
first run's cards. Whether it updates a card rather than staging a
second one depends on the model reusing the card's `card_key`. See
[Concurrency](/sdk/agents-lifecycle/#concurrency).

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
          "allowed": ["@clinical_reads", "add_or_update_protocol_card"]
        }
      }
    ]
  },
  "variables": [
    {"name": "INFERENCE_GATEWAY_URL"},
    {"name": "INFERENCE_GATEWAY_KEY", "sensitive": true}
  ]
}
```

`tools.allowed` grants the chart reads by `@category` and
`add_or_update_protocol_card` by name. It also bounds what the agent
can do: the platform drops any effect the agent returns that no
granted tool stages, so this agent can stage protocol cards but not
banners, commands, tasks, or messages. An agent with no `tools.allowed` gets no
tools at all. See [Tools](/sdk/agents-tools/#manifest-driven-permissions).

## 5. Install and try it

```bash
canvas install my_plugin --host <your-instance> \
  --variable INFERENCE_GATEWAY_URL=<your-gateway-url> \
  --secret INFERENCE_GATEWAY_KEY=<your-gateway-key>
```

Set `INFERENCE_GATEWAY_URL` to the address of the gateway that issued
your key. When Canvas Platform deploys the plugin instead, it sets the
URL for you.

Agent runs are off on an instance until Canvas turns them on for it, so
ask your Canvas team to turn them on for your test instance. Until then
each run is recorded as refused, with the reason "Agent runs are off on
this instance."

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
