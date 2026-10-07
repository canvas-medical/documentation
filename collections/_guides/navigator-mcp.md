---
title: "Drive Navigator from your coding agent (MCP)"
guide_for:
- /sdk/quickstart/
---

Navigator is Canvas's AI assistant for builders. It answers questions about the Canvas SDK and FHIR API, your own deployed plugins, and recent product updates, with read-only access and strict per-customer scope. You normally talk to Navigator in your Canvas Slack channel, but your developers can also drive it from a coding agent such as [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) or Cursor, so you can ask without leaving your editor.

This guide connects your coding agent to Navigator over a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) endpoint. It's the same assistant with the same scope and privacy rules; only the entry point changes.

{% include alert.html type="info" content="The MCP endpoint is opt-in per Canvas instance and off by default. If Navigator says it can't set up MCP access, ask your Canvas contact to enable it for your instance." %}

## Prerequisites

- A Canvas Navigator deployment for your organization, with the MCP endpoint enabled.
- A coding agent that supports streamable-HTTP MCP servers, such as [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) or Cursor.
- An email address on your Slack profile. Your key is delivered to that address, so Navigator can't issue one without it.

## 1. Get your API key

Keys are personal: each developer requests their own, from your Navigator Slack channel.

1. Ask Navigator for MCP access, for example: *"@Navigator can I get an MCP key?"* or *"@Navigator how do I use you from Claude Code?"*
2. Navigator confirms in the channel, then sends you a **direct message** with a 1Password link to your key and the `claude mcp add` command to run.
3. Open the link in any browser; you don't need a 1Password account. Only the email address on your Slack profile can open it, and 1Password emails you a verification code first. The link opens once and expires; the DM says when. Save the key to your own password manager while you're there.

The key itself never passes through Slack, and Canvas stores only a hash of it, so nobody can look it up for you later. If you miss the link's window or lose the key, ask Navigator for a new one.

A key that sits unused for 90 days, or that is never used within 14 days of being issued, is revoked automatically. If your key leaks, tell your Canvas contact and they'll revoke it.

## 2. Connect your coding agent

Run the command from Navigator's DM, pasting your key in place of the placeholder. It has this shape:

```shell
claude mcp add --transport http --scope user navigator https://<your-navigator-endpoint>/mcp \
  --header "Authorization: Bearer PASTE_YOUR_KEY_HERE"
```

Use the URL exactly as sent; the endpoint is specific to your Canvas instance.

Using a different MCP client, such as Cursor? Add an HTTP MCP server pointing at the same `/mcp` URL, with an `Authorization: Bearer <your-api-key>` header. A minimal config looks like:

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

Then restart your agent and confirm the connection. In Claude Code, run `/mcp` and check that `navigator` is listed and connected.

Navigator can take a minute or two per answer, since it consults several sources before replying. If your agent times out waiting, raise its MCP tool timeout. In Claude Code, set `MCP_TOOL_TIMEOUT=300000` (five minutes, in milliseconds).

## 3. Ask Navigator

Talk to your coding agent in plain language and mention Navigator, for example *"ask Navigator how FHIR group IDs work in Canvas"*. Your agent routes the question to Navigator and relays the answer. Behind the scenes it has two Navigator tools:

- **`ask`** sends a question to Navigator.
- **`feedback`** sends a 👍 or 👎, with an optional comment, on Navigator's answers.

Navigator sees only what your agent puts in the question. It has no access to your files, your terminal, or the rest of your conversation with your agent, so when a question depends on your code or an error message, your agent includes that context in the question. Follow-up questions in the same conversation continue the same Navigator session, so Navigator remembers its earlier answers.

Things to ask:

- *How do I add a plugin that listens for a new appointment?*
- *Which FHIR resource holds the medication list?*
- *Why isn't our scheduling plugin firing?* Navigator reads your own deployed plugin and compares it against the reference implementation.
- *What does "Create New From Existing Form" do in the Questionnaire Builder?* When the docs don't cover an on-screen feature, Navigator explains it from the Canvas source for the release your instance runs.
- *Write a SQL query for patients with an active prescription.* Navigator drafts the query and validates it against your instance's schema, without ever running it.
- *What shipped in the last two weeks?*

## Scope and privacy

Navigator over MCP has the same guardrails as Navigator in Slack:

- **Per-customer isolation**: Navigator only ever sees your own Canvas instance and plugins, never another customer's.
- **Read-only**: Navigator answers questions and drafts code and queries; it never writes to your instance or runs the SQL it drafts.
- **PHI handling**: every reply is screened before it reaches you, and PHI is redacted unless your organization has explicitly opted in under its BAA.
- **Attributable**: each request is tied to your personal API key.

<br/>
<br/>
<br/>
