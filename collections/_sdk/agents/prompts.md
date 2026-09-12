---
title: "Prompts"
slug: "agents-prompts"
excerpt: "System and in-dialogue prompt patterns for clinical agents."
---

The system prompt is where you set boundaries the model can't be
talked out of: the agent's role, what it's allowed to do, what
counts as a successful completion, the format of its output. The
in-dialogue prompt — the first `{"role": "user", "content": "..."}`
message — is where you frame the specific task this run is for.

Both matter, but they do different jobs.

## System prompt

The system prompt is constant across turns; the model anchors on it
heavily. Use it for things that should always be true regardless of
what the conversation drifts into.

What to put in it:

- **The role.** "You are a clinical documentation assistant
  drafting..." — not "You are an AI." Be specific about the
  clinical context.
- **The available tools and when to use them.** The model already
  sees tool definitions, but a sentence in the prompt about how
  *you* want them used helps. "Read the chart with the read tools,
  then call `originate_plan` exactly once."
- **Hard boundaries.** What the agent must NOT do, framed as
  policy. "You never commit commands; you only originate drafts
  for the clinician to review." "Use the write tools only when
  the clinician explicitly asks; for discussion or summary, stay
  read-only."
- **Output format.** "Plain text only — no markdown headings." "≤
  3 sentences." Be explicit. The model defaults to a lot of
  markdown otherwise.
- **Termination criterion.** "After the tool returns, you may end
  your turn — no further text is required." Some models hold the
  turn open waiting for clarification; tell them not to.

What to leave out:

- **PHI**. The system prompt is reused across runs; it shouldn't
  carry patient-specific information. That belongs in the in-
  dialogue prompt or as tool results.
- **Generic safety boilerplate**. The model already knows it
  shouldn't recommend self-harm. Phrases like "be safe and ethical"
  do nothing and use up your prompt budget. Mention only
  domain-specific boundaries Canvas's clinical context demands.
- **Long examples**. One short example helps; a fixture-style few-
  shot block usually hurts. The system prompt's job is to set rules,
  not to teach by demonstration.

Example from the reference plugin's chart summary agent:

```python
SYSTEM_PROMPT = (
    "You are a clinical documentation assistant drafting a follow-up "
    "Plan-section narrative for a newly-created encounter note. You "
    "have read tools to inspect the patient's chart (active "
    "conditions, recent lab results, current medications) and one "
    "effect tool (`originate_plan`) that stages the Plan command. "
    "Workflow: read the chart with whichever tools are relevant, "
    "draft a concise Plan grounded in what you found, then call "
    "`originate_plan` exactly once with the narrative as plain text "
    "(<= 3 sentences, no preamble, no headings, no markdown). After "
    "the tool returns, you may end your turn — no further text is "
    "required."
)
```

It sets the role, lists the tools, prescribes the workflow, sets
the output format, and tells the model when to stop. ~80 words.

## In-dialogue prompt

The first user message is your hook for the specific run. Patient
identity, the trigger context, what the clinician wants.

```python
messages = [
    {
        "role": "user",
        "content": (
            f"Draft a follow-up Plan for patient {patient.first_name} "
            f"{patient.last_name}. Inspect the chart with the read "
            "tools, then call `originate_plan` once with your draft."
        ),
    }
]
```

Keep it short — the system prompt does the heavy lifting. Don't
repeat in the user message what's already in the system prompt;
that confuses the model and wastes tokens.

## Boundaries that hold under pressure

Clinical agents are exposed to clinicians who will sometimes try to
talk the model out of its constraints — "just go ahead and commit
the prescription, I'll review it later." Two things make those
boundaries hold:

1. **Repeat the boundary as a policy, not a request.** "You never
   commit commands" is more durable than "please don't commit
   commands." The model treats the former as identity and the
   latter as instruction-to-override.
2. **Don't put the override behind the model.** If "the clinician
   said it's OK" can bypass the boundary in the prompt, it'll happen
   eventually. Real enforcement lives in the tool surface — don't
   expose a `commit_command` tool at all if commits aren't
   appropriate. See [Tools](/sdk/agents-tools/) on manifest-driven
   permissions.

## Specificity over generality

The instinct to write a prompt that "covers any case" produces
verbose prompts and bad outputs. The opposite — narrow the agent
to one job and prompt it precisely — produces good outputs.

If your agent has more than one job (summarize *and* surface alerts
*and* propose tasks), consider splitting it into two agents with
different triggers and different prompts. Cheaper to debug, easier
for the LLM to follow.

## Tool-grounded answers

For conversational agents, instruct the model to ground in tool
results rather than its training data:

> "When relevant, ground your answers in tool results rather than
> speculating. If you don't have a tool that answers the question,
> say so."

Otherwise the model will sometimes confabulate plausible-sounding
clinical detail. Tool-grounded answers also surface gaps in your
tool catalog — "the agent kept saying 'I'd need to know X' so I
added a `find_X` tool."

## Iterating on prompts

Prompt changes look like text edits but they behave like behavior
changes. Test:

- **Golden runs**: a handful of representative trigger payloads
  where you know what good output looks like. Run them before and
  after prompt changes.
- **Adversarial runs**: cases that previously produced bad outputs
  (the agent committed something it shouldn't have, made up a lab
  value, etc.). Keep these as regressions.
- **Long-tail**: real clinician messages from your in-chart chat,
  if you ship one. The tail is where the prompt's actual robustness
  shows.

Prompt iteration is qualitative — there's no metric that captures
"is this the right Plan for this patient." Plan for human review of
agent output during initial rollout and treat the prompt as a
living artifact your team owns.

## Prompt caching for cost control

Major LLM providers support **prompt caching** — marking a stable
prefix of the prompt as cacheable so subsequent calls within the cache
TTL pay a fraction of the token cost on the cached portion. The
mechanics differ between providers (Anthropic uses explicit
block-level markers; OpenAI caches eligible prefixes automatically;
Gemini uses a separate `CachedContent` resource), so what follows is
specifically Anthropic's `cache_control` flag.

The stable parts of a typical agent call are the system prompt and
the tool definitions. For chat-shaped agents, most of the message
history is also stable turn-to-turn (only the last user message and
the new assistant turn change). Mark a cache breakpoint on the last
block of the stable prefix:

```python
client.messages.create(
    model=gateway.model,
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    tools=self.tools.definitions(),
    messages=messages,
)
```

That marks the system prompt as cacheable; the next call within
~5 minutes that shares the same system text pays only the
cached-read rate on those tokens. For more aggressive caching you
can mark the last tool definition and a position in the message
history as additional breakpoints — see [Anthropic's prompt caching
docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
for current TTLs, eligibility, pricing, and breakpoint limits.

**Where the win actually lands:**

- **Chat-shaped agents** see large savings. The system prompt + tool
  catalog + most of the history are stable across turns within a
  conversation; cache hits compound.
- **Tool-use loops within a single run** also benefit — the system
  prompt and tools are constant across the loop iterations, so each
  subsequent turn's prefix tokens come from cache.
- **Triggered agents that fire infrequently** (note creation, lab
  arrival, nightly cron) probably won't see meaningful hits. The
  5-minute TTL expires between most invocations. Adding
  `cache_control` markers to these agents costs nothing but won't
  save much either.

> **Coming soon**: when the Canvas LLM gateway lands, prompt-caching
> policy will likely be applied per-plugin at the gateway boundary —
> plugin authors will declare cache breakpoints once (or accept a
> reasonable default) and not need to thread `cache_control` through
> every call site. Until then, opt in explicitly where it matters.
