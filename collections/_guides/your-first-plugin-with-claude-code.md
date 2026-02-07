---
title: "Your First Plugin (with Claude Code)"
guide_for:
- /sdk/quickstart/
- /sdk/canvas_cli/
- /sdk/events/
- /sdk/effects/
---

Canvas plugins let you customize the EHR — reacting to events, reading patient data, and returning effects that alter workflows. This guide uses an AI-assisted approach powered by Claude Code and the Canvas Plugin Assistant (CPA), getting you from idea to deployed plugin in minutes.

{% include alert.html type="info" content="Haven't yet advanced to AI-assisted coding? See <a href='/guides/your-first-plugin/'>Your First Plugin (Manual)</a> to build your plugin by hand." %}

## Background: AI-Assisted Plugin Development

[Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) is Anthropic's agentic coding tool — it can read, write, and execute code autonomously in your terminal. Rather than copying and pasting snippets from documentation or typing code by hand, you can describe what you want in plain English and Claude Code does the programming with your supervision.

Claude Code supports a plugin marketplace. We built the Canvas Plugin Assistant (CPA) Claude Code plugin (yes, a plugin to make plugins!) with deep knowledge of the Canvas SDK, common plugin patterns, and best-practice workflows in plugin development. 

CPA accelerates the entire plugin development lifecycle — from brainstorming requirements and scaffolding code, to running tests and deploying to your instance and rapidly cycling through user acceptance testing and enhancements.

Together, Claude Code with CPA lets developers (and non-developers comfortable with the command line) go from an idea to a working, deployed plugin through natural conversation at warp speed.

## Prerequisites

- Python 3.12+ installed
- A Canvas instance with admin access
- [OAuth credentials configured](/api/customer-authentication/) and saved locally in `~/.canvas/credentials.ini` (register an application with `confidential` client type and `client-credentials` grant type)
- [Claude Code installed](https://docs.anthropic.com/en/docs/claude-code/overview)

## 1. Install the Canvas Plugin Assistant and Set Up Your Environment

Follow the installation and setup instructions in the [Canvas Plugin Assistant README](https://github.com/canvas-medical/coding-agents/tree/main/canvas-plugin-assistant). Once complete, run `/cpa:check-setup` to verify everything is ready.

## 2. Describe Your First Plugin

Run `/cpa:new-plugin` to start building. CPA will ask clarifying questions via an interactive chip interface. Describe what you want in plain English. For example:

> I want a plugin that adds a button to the note header. When clicked, the button should inject a Reason for Visit command into the note with the text "hello world".

Here's what happens next:

1. **Brainstorm** — CPA asks follow-up questions to refine your requirements
2. **Specification** — CPA generates a `plugin-spec.md` for your review. Read through it and approve or request changes
3. **Scaffold** — CPA creates the plugin project structure, manifest, and handler files
4. **Implement** — CPA writes the protocol/handler code based on the spec
5. **Test** — CPA generates and runs tests to verify the plugin works correctly

At any point, if you have more detail and direction to give, in any format (other markdown files, PDF files, images), you can simply instruct Claude to read those files and use them in formulating the plan.

## 3. Deploy and Test

When you're at the point of completion where you need to try the plugin yourself, run:

```
/cpa:deploy
```

CPA validates the plugin, bumps the version, deploys it to your Canvas instance, and starts log monitoring so you can see output in real time.

To test our example first plugin, open a patient chart in your Canvas instance, create a new note, and click the button in the note header. You should see a Reason for Visit command appear with the text "hello world".

## 4. Next Steps: Keep Iterating in Conversation with Claude

The real power of AI-assisted development is iterating. Now that your plugin is deployed, enhance it with follow-up prompts:

### Make it dynamic and patient-specific

Ask CPA to update the plugin so the RFV text follows the classic clinical one-liner format, pulling patient data dynamically from the Canvas data module:

> Update the plugin so instead of "hello world", the RFV text is a clinical one-liner: "{patient first and last name} is a {age} year old {sex} presenting with ___". Pull the patient data dynamically.

### Handle existing RFV

Ask CPA to handle the case where the note already has a Reason for Visit command — editing the existing one instead of creating a duplicate:

> Update the plugin to check if the note already has a Reason for Visit command. If it does, edit the existing one instead of creating a new one.

### Ask Claude to check logs and troubleshoot

The `/cpa:deploy` command will start a subagent called `deploy-uat`, which runs a background task to access the `canvas logs` stream. Ask Claude to look at them anytime you need help troubleshooting. You can also of course view logs in the shell manually with:

```
uv run canvas logs <your-instance>
```

### Keep going

Continue exploring the [SDK documentation](/sdk/) and browse other [guides](/guides/) to see what's possible with Canvas plugins. When you're ready to harden your plugin for production, run `/cpa:coverage` to check test coverage and improve tests, `/cpa:security-review` to audit for common security issues, and `/cpa:database-performance-review` to ensure efficient data retrieval. When you feel everything is ready to finalize, use the `/cpa:wrap-up` command.

<br/>
<br/>
<br/>
