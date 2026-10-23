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

> This framework is currently in preview. The shape of the SDK is
> stable, but some features described here are scheduled for upcoming
> releases — those are called out inline.

## When agents fit

Anything where the right next step depends on reasoning over multiple
parts of a chart, where the answer isn't deterministic, and where a
clinician will review what the agent staged.

Examples:

- **Note drafting** — read the chart on note creation, draft a Plan
  command on the new note for the clinician to edit and commit.
- **Longitudinal care surveillance** — at note lock, check whether
  recommendations from prior visits have been addressed, propose new
  follow-up Tasks.
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

An agent run is asynchronous and driven by the worker, even when the
trigger is user-initiated (e.g., a chat message). The agent's logic
runs on the plugin-runner pod, never on the web request thread.

```
plugin trigger handler        home-app web/worker            plugin-runner pod
─────────────────────         ──────────────────             ─────────────────
compute() →
  RunAgentEffect ─────────→  RunAgentEffectInterpreter
                               ↓
                             run_agent Celery task ────→  PluginRunner.RunAgent
                                                            ↓
                                                          AgentPlugin.load_state
                                                          AgentPlugin.run    ← LLM + tools
                                                          AgentPlugin.save_state
                                                            ↓
                             handle_effect ←────────  emitted effects
```

A trigger emits a `RunAgentEffect`. The home-app interpreter enqueues a
Celery task. The task makes a gRPC call to the plugin-runner, which
instantiates your `AgentPlugin` subclass, acquires a per-`scope_key`
lock, drives `load_state` → `run` → `save_state`, and streams emitted
effects back to the home-app worker. The worker dispatches each effect
through the existing `handle_effect` pipeline.

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
| Per-`scope_key` lock + retry on contention | State persistence (Custom Data tables you declare) |
| LLM credentials + (soon) gateway-mediated billing | Tool implementations |
| Cost / token / latency metrics | Run rationale and semantic audit (see [Auditing](/sdk/agents-auditing/)) |
| Effect dispatch | Effect choice + idempotency keying |
| Tool permission enforcement (manifest-driven) | Tool authorization policy (declared in your manifest) |

You declare an `AgentPlugin` subclass and its tool surface; the
platform makes sure it runs safely.

## Credentials

For preview, plugin authors configure an Anthropic API key as a plugin
secret (`ANTHROPIC_API_KEY`, declared in `CANVAS_MANIFEST.json`
`variables[]`). The customer's admin sets the value on the plugin's
configuration page. Your `run()` builds an `LLMGateway` from those
secrets:

```python?partial=true
from canvas_sdk.agents import LLMGateway
from anthropic import Anthropic

gateway = LLMGateway.from_plugin_secrets(self.secrets)
client = Anthropic(api_key=gateway.api_key)
```

> **Coming soon**: a Canvas-operated LLM gateway. Plugins will receive
> short-lived session tokens instead of provider keys; per-customer
> subaccount routing, cost accounting, and audit happen at the gateway
> boundary. Your `from_plugin_secrets(...)` call site stays unchanged —
> the gateway returns a session token in `api_key` and the gateway URL
> in `base_url`.

## Manifest declaration

Each agent goes under `components.agents[]` in your manifest, with the
tools you authorize it to use:

```jsonc
{
  "components": {
    "agents": [
      {
        "class": "my_plugin.agents.chart_summary:ChartSummary",
        "description": "Drafts a Plan command on the new note",
        "tools": {
          "allowed": [
            "find_medications",
            "find_conditions",
            "originate_plan"
          ]
        }
      }
    ]
  }
}
```

`tools.allowed` is the contract between you, the EHR administrator
reviewing your plugin, and the runtime. The platform reads it at load
time and scopes the agent's tool registry before `run()` fires — the
agent literally cannot see or invoke tools you didn't declare. See
[Tools](/sdk/agents-tools/) for the full pattern.

## Where to next

<ul>
  <li><a href="/sdk/agents-quick-start/"><strong>Quick start</strong></a> — minimal working agent in ~50 lines.</li>
  <li><a href="/sdk/agents-lifecycle/"><strong>Lifecycle</strong></a> — what your subclass implements; the order the runtime calls things.</li>
  <li><a href="/sdk/agents-managing-state/"><strong>Managing state</strong></a> — three persistence patterns: stateless, snapshot, event-sourced.</li>
  <li><a href="/sdk/agents-tools/"><strong>Tools</strong></a> — read tools, effect tools, and manifest-driven permissions.</li>
  <li><a href="/sdk/agents-prompts/"><strong>Prompts</strong></a> — system prompts in a clinical setting.</li>
  <li><a href="/sdk/agents-testing/"><strong>Testing</strong></a> — patterns for unit-testing agents and tools without real provider calls.</li>
  <li><a href="/sdk/agents-auditing/"><strong>Auditing</strong></a> — what the platform captures, what you should capture.</li>
</ul>

<br/>
<br/>
