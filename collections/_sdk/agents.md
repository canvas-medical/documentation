---
title: "Agent Runner Framework"
disable_anchorlist: true
---

The Agent Runner Framework lets you deploy LLM-driven agents as Canvas
plugins. An agent has read access to a patient's chart, can call tools you
define (and tools the SDK ships), and emits Canvas [Effects](/sdk/effects/)
that the platform dispatches — drafting commands on a note, creating
tasks, surfacing recommendations to clinicians, and so on. Unlike a
[BaseHandler](/sdk/handlers-basehandler/), an agent's `run()` is allowed to
take seconds (or minutes, for tool-heavy workflows) — it runs on a
worker, not on the request thread.

{% include alert.html type="warning" content="This framework is currently in preview. The shape of the SDK is stable, but some features described here are scheduled for upcoming releases. Those are called out inline." %}

## When agents fit

Anything where the right next step depends on reasoning over multiple
parts of a chart, where the answer isn't deterministic, and where a
clinician will review what the agent staged.

Examples:

- **Note drafting** — read the chart on note creation, draft a Plan
  command on the new note for the clinician to edit and commit.
- **Longitudinal care surveillance** — at note lock, check whether
  recommendations from prior visits have been addressed and stage
  protocol cards for new follow-up.
- **In-chart chat** — a clinician asks "what's this patient's A1c
  history?"; the agent reads the chart and answers, optionally staging
  prescriptions or lab orders the clinician then commits.
- **Background risk stratification** — periodic CronTask emits a
  `RunAgentEffect`; the agent reviews open patients and creates Tasks
  for those who match a clinical pattern.

Agents are distinct from handlers because they reason; handlers do
fixed transformations. Reach for an agent when "what should happen
next" depends on chart context the rules engine can't enumerate.

## How a run executes

An agent run is asynchronous, even when the trigger is user-initiated
(e.g., a chat message):

1. A handler in your plugin returns a `RunAgentEffect` naming one of
   your plugin's agents, the patient and note the run is about, a
   `scope`, and a small `trigger_payload`.
2. Canvas checks the run's subject, adds the staff member whose action
   started it, and queues the run on a background worker. Runs of the
   same agent on the same scope go one at a time.
3. The worker calls your agent's `load_state` → `run` → `save_state`,
   with the subject on `self.subject`.
4. Each effect your agent returns is applied like any other plugin
   effect. The next run on that scope starts only after these
   effects have been applied, so it sees what this run did.

Two invocation patterns share that path:

- **Event-triggered** — a `BaseHandler` in your plugin emits the
  effect from `compute()` (e.g., on note creation, lab arrival, cron
  tick).
- **User-initiated** — a `SimpleAPI` POST handler emits the effect
  and returns `202 Accepted`; the UI polls a history endpoint until
  the agent's output lands. Don't run agents synchronously inside a
  request handler — the plugin-runner iterates handlers sequentially,
  and a multi-second LLM round-trip blocks every other plugin on the
  instance.

See [Lifecycle](/sdk/agents-lifecycle/) for what your subclass needs to
implement and what the platform does around it.

## What the platform owns vs what you own

| Platform owns | You own |
|---|---|
| Triggering, dispatch, lifecycle orchestration | Agent business logic (`run()`) |
| The run's subject: checking the patient and note, identifying the requesting staff member | Which patient and note a run is about |
| One run at a time per agent and scope, with retry | State persistence (see [Managing State](/sdk/agents-managing-state/)) |
| LLM access: gateway credentials, metering, budgets | Tool implementations |
| A record of every run, its tool calls, and its outcome, kept 90 days; per-call tokens and cost at the gateway, by run | Run rationale and semantic audit (see [Auditing](/sdk/agents-auditing/)) |
| Effect dispatch | Effect choice + idempotency keying |
| Tool grant enforcement: the agent sees only granted tools and can return only the effects they stage | Tool grant (declared in your manifest) |

You declare an `AgentPlugin` subclass and its tool surface; the
platform makes sure it runs safely.

## Credentials

Agents reach Anthropic through Canvas's inference gateway. Each agent
plugin holds its own gateway key: declare an `INFERENCE_GATEWAY_KEY`
variable with `"sensitive": true` in your manifest (see
[Manifest declaration](#manifest-declaration)), and set its value when
you install the plugin, as with any other
[plugin secret](/sdk/secrets/). Gateway keys are issued per organization
in Canvas Platform, each with its own spending limit; your Canvas team
can issue one for your plugin.

Before each run, the platform builds the `LLMGateway` it passes to
`run()` from the instance's gateway URL and your plugin's
`INFERENCE_GATEWAY_KEY`. `gateway.client()` returns an
`anthropic.Anthropic` client pointed at the gateway:

```python?partial=true
client = gateway.client()
response = client.messages.create(
    model=gateway.model,
    max_tokens=1024,
    messages=messages,
)
```

The client sends your plugin's key, along with headers naming your
plugin, agent, and run.

> **Coming soon**: the gateway records those names on each call in its
> usage ledger.

The gateway meters every call against your organization's inference
account and enforces its budget and model allowlist. `gateway.model`
defaults to `claude-sonnet-4-6`; pass any model your organization has
enabled. Refusals come back as Anthropic's own error types, so the SDK's
exception handling works unchanged:

| Status | Cause |
|---|---|
| 401 `authentication_error` | The key is missing, revoked, or not enabled for inference |
| 402 `billing_error` | The organization's budget or a key's monthly limit is reached |
| 404 `not_found_error` | The model is not available to the organization |
| 400 `invalid_request_error` | A feature the gateway does not serve (code execution, containers, skills, the Files API, the MCP connector, the priority service tier) or a malformed request |

Let these errors propagate out of `run()`. The platform retries a run
when the gateway is unreachable, rate-limited (429), or returns a
server error, and records a refusal (any status above) as a failed run
without retrying it. If the instance has no gateway URL configured, or your plugin's
`INFERENCE_GATEWAY_KEY` isn't set, the run fails before your agent is
instantiated.

## Manifest declaration

Each agent goes under `components.agents[]` in your manifest, with the
tools you authorize it to use. Declare the gateway key under the
top-level `variables`:

```jsonc
{
  "components": {
    "agents": [
      {
        "class": "my_plugin.agents.advisor:LongitudinalCareAdvisor",
        "description": "Tracks follow-up across visits with protocol cards",
        "tools": {
          "allowed": ["@clinical_reads", "@clinical_alerts"],
          "denied": ["remove_banner_alert"]
        }
      }
    ]
  },
  "variables": [
    {"name": "INFERENCE_GATEWAY_KEY", "sensitive": true}
  ]
}
```

`tools` is the contract between you, the EHR administrator reviewing
your plugin, and the runtime. Before `run()` fires, the platform scopes
the agent's tool registry to the tools granted here (names and
`@category` groups, minus anything in `denied`). After the run, it
drops any effect the agent returns that no granted tool stages, even
one the agent built directly. An agent with no `tools.allowed` gets no
tools and can return no effects. See [Tools](/sdk/agents-tools/) for
the full pattern.

## Where to next

<ul>
  <li><a href="/sdk/agents-quick-start/"><strong>Quick start</strong></a> — an agent that tracks follow-up across visits with protocol cards.</li>
  <li><a href="/sdk/agents-lifecycle/"><strong>Lifecycle</strong></a> — what your subclass implements; the order the runtime calls things.</li>
  <li><a href="/sdk/agents-managing-state/"><strong>Managing state</strong></a> — three persistence patterns: stateless, snapshot, and state kept in the chart.</li>
  <li><a href="/sdk/agents-tools/"><strong>Tools</strong></a> — read tools, effect tools, and manifest-driven permissions.</li>
  <li><a href="/sdk/agents-prompts/"><strong>Prompts</strong></a> — system prompts in a clinical setting.</li>
  <li><a href="/sdk/agents-testing/"><strong>Testing</strong></a> — patterns for unit-testing agents and tools without real provider calls.</li>
  <li><a href="/sdk/agents-auditing/"><strong>Auditing</strong></a> — what the platform captures, what you should capture.</li>
</ul>

<br/>
<br/>
