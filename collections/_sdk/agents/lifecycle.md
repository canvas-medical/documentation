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

1. **Check the run's subject.** The patient must exist, the note must
   belong to that patient, a user who is not staff, such as a patient
   acting in the portal, may only name their own patient record, and a
   staff member's patient groups must let them see the patient.
   The staff member whose action started the run becomes the run's
   requester, and the run [acts for them](#acting-for-the-requester). An effect with no Canvas user behind it, such as one from
   a SimpleAPI route with API-key authentication or a webhook, runs as
   Canvas Bot, and its `patient_id` is accepted once that patient exists:
   your plugin vouches for it, so check it before returning the effect.
   The platform grants the run its [capabilities](#capabilities) from
   the requester's permissions, and a `claim_id` must name an existing
   claim, which needs the `REVENUE` capability.
   The `trigger_payload` cannot carry `patient_id`, `staff_id`,
   `note_id`, or `claim_id` of its own. A subject that fails a check is refused and the
   run is never queued. Either way the run
   gets a record under its effect's `run_id`, which the platform keeps
   current through the steps below (see
   [Auditing](/sdk/agents-auditing/#reading-run-records)).
2. **Derive the scope key** from the effect's `scope` and the subject,
   or from its `scope_id` for a `KEY` scope. See
   [Concurrency](#concurrency) below.
3. **Take the run's scope.** A background worker claims the scope for
   this agent and scope key. If another run holds it, this run waits
   and retries with backoff.
4. **Check ownership.** The agent must belong to the plugin whose
   handler returned the effect; a plugin can't run another plugin's
   agents.
5. **Build the `LLMGateway`** from the instance's inference gateway URL
   and your plugin's `INFERENCE_GATEWAY_KEY` secret, attributed to your
   plugin, this agent, and this run. If either is unset, the run stops
   here with `error_kind="LLM_NOT_CONFIGURED"`.
6. **Instantiate your subclass** (`agent_class()` with no arguments).
7. **Set `agent.subject`, `agent.requester`, and `agent.capabilities`**
   to the checked subject, the requester with their permissions, and the
   granted capabilities, and `agent.run_id` to the run's id. See
   [The run's subject](#the-runs-subject) below.
8. **Apply the manifest tool grant.** The platform expands
   `tools.allowed` (tool names and `@category` groups) against
   `agent.tools`, subtracts `tools.denied`, removes the tools the
   requester [could not use](#acting-for-the-requester), sets
   `agent.tools_allowed` to the result, and replaces `agent.tools` with
   a scoped view containing only those tools. An agent entry with no
   `tools.allowed` gets no tools. Granted tools named in `tools.approve`
   [propose their changes](#approve-before-write) instead of making them.
9. **Call `on_run_start(scope_key)`** (optional hook; default no-op).
10. **Call `load_state(scope_key)`** to get the run's starting state.
11. **Call `run(state, gateway, trigger_payload)`** — the body of your
    agent.
12. **Call `save_state(scope_key, result.state)`** with the updated
    state from your `AgentRunResult`.
13. **Call `on_run_end(result)`** (optional hook).
14. **Filter and stamp the emitted effects.** Any effect whose type no
    granted tool stages is dropped. The rest are stamped with
    provenance (`plugin_name`, `handler_name` set to the agent class,
    `actor`, `source`).
15. **Check and apply the effects.** Every effect must be one the
    requester could make in the chart; if any is not, the run fails with
    `error_kind="PERMISSION_DENIED"` and none of its effects apply.
    Otherwise they apply through the same pipeline as any plugin
    effect, recorded in the audit trail as requested by the user whose
    action started the run. Proposed changes are held for the requester
    to [approve or deny](#approve-before-write).
16. **Release the scope**, so the next run on it can start.

If any of steps 10–12 raises, `on_run_error(exc)` fires, the exception
is captured to Sentry, and the run returns `success=False`. Errors from
the inference gateway are classified rather than captured: an outage
(`error_kind="LLM_UNAVAILABLE"`) is retried, and a refusal
(`error_kind="LLM_REFUSED"`) fails the run without a retry.

A run gets 10 minutes. The tool loop starts no model call in its last
30 seconds, and gives each call no more than the time left, split
across its retries. A run that reaches that point stops: its state is
not saved, its effects are not applied, and the scope passes to the
next run. Its record shows it as `failed`, and a run still going when
its time ends shows as `abandoned`.

An agent whose work takes longer, such as reconciling hundreds of
outside records, can ask for more time per run with `run_seconds` in
its manifest entry, up to 1,800 (30 minutes):

```json
{
  "class": "my_plugin.agents.reconcile:ReconcileAgent",
  "description": "Reconciles outside records against the chart",
  "run_seconds": 1200,
  "tools": {"allowed": ["@clinical_reads"]}
}
```

`canvas validate` rejects a value above 1,800, and the platform holds
every run to that ceiling whatever the manifest says. A run of an agent
that asks for more than the default 10 minutes is an extended run: the
plugin runner admits only a few at a time (one by default, and always
fewer than its agent runs in total), so long runs cannot take every
agent thread from the chats people are waiting on. An extended run that
finds them all taken waits and retries like any other run turned away
by a busy runner, and if it never gets one its record shows it gave up
with `error_kind="EXTENDED_RUNS_BUSY"`. Ask only for the time the work
needs: the run's scope stays held, and an agent thread busy, for as
long as it runs.

The tool loop makes at most `max_model_calls` model calls per run,
sub-agents included: 40 by default, set as a class attribute on your
`AgentPlugin` subclass. Reaching it ends the tool loop with
`stopped="call_limit"`, which the run's record shows as how its last
tool loop ended.

When the instance is already running its share of agents, a new run
waits and retries rather than taking workers that event handlers need.
Runs a person is waiting on go ahead of batch work; see
[Runs for many patients](#runs-for-many-patients).

## The run's subject

The platform sets three things on the agent before any hook fires:

| Attribute | Field | Where it comes from |
|---|---|---|
| `self.subject` (`RunSubject`) | `patient_id` | The effect's `patient_id`, checked to exist |
| | `note_id` | The effect's `note_id`, checked to belong to the patient |
| | `claim_id` | The effect's `claim_id`, checked to exist |
| `self.requester` (`RunRequester`) | `staff_id` | The staff member whose action emitted the effect; `None` for a run a patient, a schedule, or a system event started |
| | `permissions` | The staff member's permissions, such as `"api.change_task"`; empty for a run a patient started; `None` when permissions do not limit the run (see [Acting for the requester](#acting-for-the-requester)) |
| `self.capabilities` | | The [capabilities](#capabilities) the platform granted the requester |

Your agent reads these from the agent rather than from
`trigger_payload`, which rejects `patient_id`, `staff_id`, `note_id`,
and `claim_id` keys. `run_tool_loop` hands the subject to every tool, so the standard
tools read, write, and check ownership against the platform's patient.

A run doesn't have to be about a patient. An agent that works on a
clinician's inbox or the whole instance leaves `patient_id` unset and
picks the `STAFF`, `KEY`, or `AGENT` scope, and one opened from a claim
picks `CLAIM`. In such a run,
standard tools that only make sense on a patient return an error to the
model, so it never reads an empty chart as a patient with no records.
Your own patient tools can do the same with `require_patient_id(ctx)`
from `canvas_sdk.agents`.

```python?partial=true
def load_state(self, scope_key):
    messages = load_conversation(self.subject.patient_id, self.requester.staff_id)
    return AgentState(data={"messages": messages})
```

### Acting for the requester

A run a staff member started, whether from a chat or by an action that
triggered it, acts for them: it may do what they could do in the chart,
and nothing more. The platform enforces this in three places:

- **Patients:** the run's patient must be one their patient groups let
  them see, and every effect may touch only patients they can see.
- **Tools:** a tool declares the permission the chart checks for the
  same action with `required_permissions`, and the capability it needs
  with `required_capabilities`. The platform hides tools the requester
  could not use, so the model never offers them.
- **Effects:** before applying a run's effects, the platform checks each
  against the permission the chart checks for that action and the
  patients it touches. An effect type the chart has no counterpart for
  is refused, and committing a command applies only once the requester
  [approves it](#approve-before-write).

The standard tools need only what the chart needs. Updating a task or
commenting on one needs `api.change_task`, and drafting a review note
needs `api.add_note`. Creating a task, drafting a message or any
command, and adding a banner or protocol card need only access to the
patient. The [tools catalog](/sdk/agents-tools/) lists each tool's
requirements.

A run a patient started holds no staff permissions, so tools that need
one are hidden, and its effects may change only the patient's own
records. A run no user started, such as one from a webhook or an
API-key route, runs as Canvas Bot and acts with your plugin's authority,
as a handler's effects do; a superuser's run is not limited by
permissions.

Declare what your own tool needs the same way, so it is hidden from
requesters who could not use it:

```python?partial=true
@tools.tool(
    name="close_task",
    description="...",
    input_schema={...},
    effect_types=("UPDATE_TASK",),
    required_permissions=("api.change_task",),
)
def close_task(arguments, *, ctx):
    ...
```

### Capabilities

Some tools act beyond one patient's chart, so they work only for a run
the platform grants the matching `Capability`. The platform decides a
run's capabilities from the permissions of the staff member who started
it; a run a patient or Canvas Bot started has none.
`self.capabilities` holds the grant.

| `Capability` | Granted when the requester | Opens |
|---|---|---|
| `REVENUE` | holds the Revenue access permission, which the revenue pages require, and patient groups leave them able to see every patient | the claims tools, and runs with a `claim_id` |

A tool that needs a capability declares it, and the platform hides it
from runs without it:

```python?partial=true
from canvas_sdk.agents import Capability


@tools.tool(
    name="claims_for_payer",
    description="...",
    input_schema={...},
    required_capabilities=(Capability.REVENUE,),
)
def claims_for_payer(arguments, *, ctx):
    ...
```

A claims tool that takes a `claim_id` defaults to the run's claim, so a
chat opened from a claim acts on that claim unless the model names
another. `get_claim` returns the patient's name and sex from the claim
but never the SSN, date of birth, phone, or address the claim carries.

### Approve before write

A tool that commits a change, rather than drafting one for a clinician to
finish, can wait for the requester to approve each change it makes. List
it, or a `@category` of them, under `tools.approve` in the agent's
manifest entry. Here `commit_assessment` stands for a tool your plugin
registers, since no standard tool commits a command:

```json
"tools": {
  "allowed": ["@clinical_reads", "@task_writes", "commit_assessment"],
  "approve": ["@task_writes", "commit_assessment"]
}
```

The tool code does not change. When the model calls a listed tool, the
effects it stages become proposals, and the model receives
`{"status": "awaiting_approval", "proposal_ids": [...], "tool_result": ...}`,
with the tool's own result under `tool_result`, so it can tell the user
what is waiting. A tool
that stages nothing, such as one that refused its input, returns its own
result. Sub-agents scoped from the agent's tools propose the same way.

When the run ends, the platform checks each proposed change against the
requester's permissions, like any effect, and holds it as an
`AgentRunProposal` for one hour:

- **Who decides:** only the requester, the user the run acted for. A run
  that no user started, such as a Canvas Bot run, cannot propose.
- **How:** your plugin draws the change, such as a card in its chat, and
  returns a `DecideAgentProposal` effect from a SimpleAPI route, an
  application, or an action button when the requester approves or
  denies it. A decision from an event handler or another plugin is
  refused.
- **What applies:** an approval checks the requester's permissions and
  patient groups again and applies exactly the stored change, recorded
  in the audit trail as the requester's action correlated with the run.
  A second decision on the same proposal applies nothing.
- **Drafts apply at once:** a proposal of a draft, such as an originated
  command or a drafted message, applies without waiting, since a person
  still commits, signs, or sends it.
- **Commits need approval:** a committed command is the user attesting
  to it, so an agent's commit applies only through an approved proposal.

A proposal's `status` is `pending`, `approved`, `denied`, `failed` (the
change could not apply when approved), or `expired`. Approval is per
tool: the platform drops an effect a listed tool stages if the agent
returns it bare, unless a granted tool that doesn't need approval stages
the same effect type.

```python?partial=true
from http import HTTPStatus

from canvas_sdk.effects.agent import DecideAgentProposal
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.handlers.simple_api import SimpleAPI, StaffSessionAuthMixin, api
from canvas_sdk.v1.data import AgentRunProposal


class ProposalsAPI(StaffSessionAuthMixin, SimpleAPI):
    @api.get("/proposals")
    def proposals(self):
        staff_id = self.request.headers["canvas-logged-in-user-id"]
        pending = AgentRunProposal.objects.filter(
            run__id=self.request.query_params["run_id"],
            staff__id=staff_id,
            status="pending",
        )
        return [JSONResponse({"proposals": [
            {"id": str(p.id), "tool": p.tool, "arguments": p.arguments} for p in pending
        ]})]

    @api.post("/decide")
    def decide(self):
        body = self.request.json()
        return [
            JSONResponse({"status": "decided"}, status_code=HTTPStatus.ACCEPTED),
            DecideAgentProposal(
                proposal_id=body["proposal_id"],
                decision=body["decision"],  # "approve" or "deny"
                reason=body.get("reason", ""),
            ).apply(),
        ]
```

## The three methods you implement

### `load_state(scope_key) -> AgentState`

Called once per run, before `run()`. Return the state this run should
start from — read from your Custom Data tables, deserialize a JSON
blob, query the chart, whatever makes sense. Return `AgentState()`
(empty) if your agent is stateless.

`scope_key` is the key the platform derived from the effect's `scope`.
Most agents key their storage on `self.subject` instead.

### `run(state, gateway, trigger_payload) -> AgentRunResult`

The body of your agent. Drive the tool-use loop, accumulate effects,
update `state` in place. Return an `AgentRunResult(state=..., effects=[...])`.

```python?partial=true
from canvas_sdk.agents import AgentRunResult


def run(self, state, gateway, trigger_payload):
    result = self.run_tool_loop(gateway, system=SYSTEM_PROMPT, messages=messages)
    return AgentRunResult(state=state, effects=result.effects)
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
    system=SYSTEM_PROMPT,
    messages=messages,          # the conversation so far, ending with the turn to answer
    max_turns=8,                # optional; also max_tokens, model, history_chars, cache_system
)
result.text       # the model's last reply, stripped
result.messages   # messages plus every new turn, as JSON-safe dicts you can store
result.effects    # the effects the tools staged, to return from run()
result.turns      # how many model calls it made
result.stopped    # "end_turn", "max_turns", "call_limit", or "unexpected"
```

Every tool call gets a context the model never sees, which
`self.tool_context(gateway)` builds:

| Key | Value |
|---|---|
| `patient_id`, `claim_id` | From `self.subject` |
| `staff_id` | From `self.requester` |
| `note_id` | `self.subject.note_id`, or for a run a staff member started, that staff member's open note on the patient |
| `permissions` | `self.requester.permissions` |
| `capabilities` | `self.capabilities` |
| `effects` | A new list the tools append to; returned as `result.effects` |
| `gateway`, `parent_tools` | The run's gateway and the agent's granted tools, for tools that run sub-agents with `run_subagent` or make a model call of their own, as `read_document` does |

Pass `ctx={...}` to add agent-specific keys. Those keys cannot replace
any key in the table: passing one raises `ValueError`. A tool always
acts on the run's own patient.

Along the way it:

- runs each tool call through `self.tools` and sends a failure back to
  the model as an error result, so the model can recover;
- cuts a tool result longer than the tool's limit, telling the model
  so and how to narrow the request. The limit is 50,000 characters
  unless the tool registers its own with `max_result_chars` (see
  [Tools](/sdk/agents-tools/#result-size));
- in a platform run, cuts any tool result past the run's total of
  600,000 characters of tool output, sub-agents included, and tells the
  model to answer from what it has;
- runs complete tool calls in a turn the token limit cut off;
- sends the model only the newest part of a long history that fits a
  size budget (`history_chars`, 300,000 characters by default), while
  returning all of it (`history_chars=None` sends everything);
- marks the system prompt for prompt caching (`cache_system=False` to
  turn that off);
- answers any tool call left open when the model stops unexpectedly,
  so a stored transcript is always valid to send again;
- calls `on_turn` before each model call;
- lets errors from the inference gateway propagate, including those from
  a sub-agent a tool runs, so the platform can retry an outage and
  record a refusal.

`canvas_sdk.agents.run_tool_loop` is the same loop as a function that
takes `tools` and `ctx` explicitly, for code without an agent instance;
sub-agents use it with their parent's context.

### `save_state(scope_key, state) -> None`

Called once per run, after `run()` returns. Persist `state.data`
back to wherever you read it from. For stateless agents this is a
no-op.

`save_state` runs while the run holds its scope. A concurrent
`RunAgentEffect` for the same agent and scope waits until this run's
effects have been applied.

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

The platform runs one invocation at a time per agent and scope. A
second `RunAgentEffect` for the same agent and scope waits until the
first run's effects have been applied, retrying with randomized backoff,
about 5 minutes in total on average. If another run still holds the
scope when those retries run out, it waits once more, until that hold
expires, so a run whose worker stopped never blocks the scope for good;
after that it gives up.

This lets `load_state` / `run` / `save_state` treat the underlying
storage as if no one else is touching it during the run, including
state the previous run wrote through its effects, such as protocol
cards or tasks.

**Picking a `scope`**: choose what should serialize, and the platform
derives the key from the run's subject. Runs of two different agents
never wait on each other, whatever their scope.

| `RunAgentEffect.Scope` | Runs that wait on each other | Requires |
|---|---|---|
| `PATIENT` | Runs on the same patient | `patient_id` |
| `PATIENT_AND_STAFF` | Runs on the same patient started by the same staff member, such as one clinician's chat | `patient_id`, and a run a staff member started |
| `NOTE` | Runs on the same note; the same patient's other notes run concurrently | `patient_id` and `note_id` |
| `STAFF` | Runs started by the same staff member, such as an agent that works through one clinician's inbox | a run a staff member started |
| `CLAIM` | Runs on the same claim, such as one claim's chat | `claim_id`, and the [`REVENUE` capability](#capabilities) |
| `KEY` | Runs naming the same `scope_id`, for something none of the above covers, such as `f"appointment:{appointment_id}"` | `scope_id` |
| `AGENT` | Every run of this agent on the instance, such as a strictly serialized cron job | nothing |

A `RunAgentEffect` missing a field its scope requires, or carrying a
`scope_id` with any scope other than `KEY`, raises `ValueError` when you
build it. A `PATIENT_AND_STAFF` or `STAFF` run that
no staff member started is refused, and the run is never queued.

The scope decides only which runs wait on each other. `scope_id` gives
the agent's tools nothing, so a run's patient always comes from its
checked `patient_id`. Nor does the scope decide which state a run sees:
`load_state` receives the scope key and nothing else. `KEY` and `AGENT`
leave the patient out of the key, so an agent that keeps per-patient
state under those scopes must key that state by
`self.subject.patient_id`. An `AGENT`-scoped chat agent that stored its
history under the scope key alone would load one patient's conversation
into the next patient's run.

```python?partial=true
from canvas_sdk.effects.agent import RunAgentEffect

RunAgentEffect(
    agent_id="my_plugin.agents.advisor:Advisor",
    scope=RunAgentEffect.Scope.PATIENT,
    patient_id=patient_id,
    note_id=note_id,
)
```

Each Canvas instance serializes its own runs, so you don't need to
namespace by customer.

### Runs for many patients

A run is about one subject, so work across many patients, such as
reviewing every patient overdue for a screening, is many runs: return
one `RunAgentEffect` per patient, each with the `PATIENT` scope.

```python?partial=true
from canvas_sdk.effects.agent import RunAgentEffect

def compute(self):
    runs = [
        RunAgentEffect(
            agent_id="my_plugin.agents.gap_review:GapReview",
            scope=RunAgentEffect.Scope.PATIENT,
            patient_id=patient.id,
        )
        for patient in overdue_patients()
    ]
    return [run.apply() for run in runs]
```

Each run is checked, recorded, and run on its own. A staff member's
runs are refused for patients their patient groups hide, and the rest
proceed; each run's effects apply or not for its own patient only.
Runs on different patients don't wait on each other. Keep each
`run.run_id` to follow the runs through their `AgentRun` records.

Runs a person is waiting on go ahead of batch work. A run is
interactive when a signed-in user started it from a SimpleAPI route, an
application, or an action button, and they have no other run of the
same agent still waiting. Everything else waits behind interactive
runs: runs from event handlers, schedules, and webhooks; Canvas Bot runs,
such as those from an API-key SimpleAPI route; and every run
after the first when a user's request starts many. A chat's run doesn't
wait behind a large batch, though the batch takes longer to finish while
people are using the agents. A run already started isn't interrupted,
so a chat can still wait for a worker to free up.

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
