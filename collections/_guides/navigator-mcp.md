---
title: "Drive Navigator from your coding agent (MCP)"
guide_for:
- /sdk/quickstart/
---

Navigator is Canvas's AI assistant for builders. It answers questions about the Canvas SDK and FHIR API, your own deployed plugins, and recent product updates — with read-only access and strict per-customer scope. You normally talk to Navigator in your Canvas Slack channel, but your developers can also drive it from a coding agent such as [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) or Cursor over MCP, so you can ask without leaving your editor.

This guide connects your coding agent to Navigator over a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) endpoint. Same assistant, same scope and privacy rules — only the entry point changes.

{% include alert.html type="info" content="The MCP endpoint is opt-in per Canvas instance and off by default. If the setup below reports no access, ask your Canvas contact to enable it for your instance." %}

## Prerequisites

- A Canvas Navigator deployment for your organization, with the MCP endpoint enabled.
- A coding agent that supports streamable-HTTP MCP servers — e.g. [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) or Cursor.
- A personal Navigator API key (see the next step). Keys are per developer, not shared.

## 1. Get your API key

Navigator provisions keys on request, from your Canvas Slack channel:

1. In your Navigator channel, ask Navigator for an MCP key — for example: *"@Navigator provision me an MCP key."*
2. Navigator replies in-channel to confirm (with no secret), then sends you a **direct message** containing your API key and the exact `claude mcp add` command to run.

Your key is shown only once — Canvas stores only a hash of it. If you lose it, ask Navigator for a new one.

## 2. Connect your coding agent

Run the command Navigator DM'd you. It has this shape:

```shell
claude mcp add navigator \
  --scope user \
  --transport http \
  https://<your-navigator-endpoint>/mcp \
  -H 'Authorization: Bearer <your-api-key>'
```

Use the URL and key exactly as sent — the endpoint is specific to your Canvas instance.

Using a different MCP client (e.g. Cursor)? Add an HTTP MCP server pointing at the same `/mcp` URL, with an `Authorization: Bearer <your-api-key>` header. A minimal config looks like:

```json
{
  "mcpServers": {
    "navigator": {
      "url": "https://<your-navigator-endpoint>/mcp",
      "headers": {
        "Authorization": "Bearer <your-api-key>"
      }
    }
  }
}
```

Then restart your agent and confirm the connection — in Claude Code, run `/mcp` and check that `navigator` is listed and connected.

## 3. Ask Navigator

Once connected, your agent has two Navigator tools:

- **`ask`** — send a question to Navigator. Your agent forwards relevant context from your editor (such as the file you're in) with each follow-up, so answers stay grounded in what you're building.
- **`feedback`** — send a 👍 or 👎 on Navigator's last answer.

Navigator keeps a session per conversation, so follow-up questions build on the same context — just keep asking in the same session.

Things worth asking:

- *How do I add a plugin that listens for a new appointment?*
- *Which FHIR resource holds the medication list?*
- *Why isn't our scheduling plugin firing?* — Navigator reads your own deployed plugin and compares it against the reference implementation.
- *Write a SQL query for patients with an active prescription.* — Navigator drafts the query and validates its syntax against your instance, without ever running it.
- *What shipped in the last two weeks?*

## Scope and privacy

Navigator over MCP has the same guardrails as Navigator in Slack:

- **Per-customer isolation** — Navigator only ever sees your own Canvas instance and plugins, never another customer's.
- **Read-only** — Navigator answers questions and drafts code and queries; it never writes to your instance or runs the SQL it drafts.
- **PHI handling** — every reply is screened before it reaches you, and PHI is redacted unless your organization has explicitly opted in under its BAA.
- **Attributable** — each request is tied to your personal API key.

<br/>
<br/>
<br/>
