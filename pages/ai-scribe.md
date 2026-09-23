---
permalink: /product-updates/ai-scribe/
layout: betas
title: "Beta | Hyperscribe V2"
date: 2026-09-20
---

{% include alert.html type="warning" content="<b>Beta participation:</b> Hyperscribe V2 is currently in a limited beta. Use the interest form at the bottom of this page to express interest and receive updates." %}

## Overview

Hyperscribe records a visit and turns the transcript into Canvas commands for the provider to review.

The scribe panel sits beside the chart while you record. When you finish, Scribe generates a set of proposed commands. You can review the proposals individually, select several, or add them all at once.

Nothing is added to the chart until you add it. Commands go through the same path as commands entered manually, so once they're in the note there is no distinction between a Scribe-generated command and one entered by hand.


## Try it

The panel below is the target beta interface using sample data. It walks through a visit from recording to finished note, with an in-app guide showing what to do next. The interface is still changing during the beta, so expect some differences between this preview and what you see in your instance.

<style>
/* The docs content column is capped at 800px (_scss/_pagelayout.scss), which is not enough
   room for a two-pane EHR. The frame is given a viewport 1/scale wider than the column and
   drawn at `scale`, so the app sees about 1140px. `width: calc(100% / var(--embed-scale))`
   is what keeps it responsive. Change --embed-scale and nothing else. */
.scribe-embed {
  --embed-scale: 0.65;
  --embed-height: 660px;
  width: 100%;
  height: var(--embed-height);
  overflow: hidden;
  border: 1px solid #ccc;
  background: #fff;
}
.scribe-embed iframe {
  width: calc(100% / var(--embed-scale));
  height: calc(var(--embed-height) / var(--embed-scale));
  transform: scale(var(--embed-scale));
  transform-origin: 0 0;
  border: 0;
  display: block;
}
</style>

<div class="scribe-embed">
  <iframe src="/assets/static/ai-scribe-preview.html"
          title="Hyperscribe interface preview"
          allow="clipboard-write"></iframe>
</div>

<a href="/assets/static/ai-scribe-preview.html" target="_blank" rel="noopener">Open in a new tab</a>
for the full-size version.

## What it does

- **Record a visit from the docked panel.** Pause, resume, and finish the recording while navigating Canvas freely. The recording stays with the visit, so you can move around Canvas while it runs.
- **Live transcript.** The transcript identifies who said each line and remains available
  after the visit
- **Additional note context.** Add information while you record that you want Hyperscribe to use
  when drafting the note. This context is used for the draft and is not written to the chart.
- **Command proposals.** Proposals are grouped into History, Exam, and Assessment and Plan.
  Add them individually, select several, or add everything at once. Dismissed proposals move
  to the bottom of the panel and can be restored.
- **Updates to existing commands.** If a proposal matches a command already in the note,
  Hyperscribe offers to update the existing command instead of creating a duplicate. This lets
  Hyperscribe fill the note type's existing template.
- **Editable free text.** Edit free-text values in the panel before adding them to the note.
  Fields backed by a code system, option set, date, or constrained number are shown but remain
  controlled by the note.
- **Evidence.** When a proposal comes from a specific part of the conversation, Hyperscribe shows
  the relevant transcript text and links back to it.
- **Custom instructions.** Each provider can set plain-language instructions that are used
  when generating drafts.

## Where Hyperscribe gets its context

- The **transcript**
- The **additional note context** you enter during the visit
- Your **custom instructions** set within each user's preferences
- The **note's existing commands**, letting you leverage already built templates and document as you are recording. 
- The **patient's chart**, to identify when a proposal resembles something previously documented


## Request to join the beta

Complete the form below and our team will reach out with next steps. We will enroll a limited set of customers in October, with a plan to open the beta to all in November. Participation will be gated on a beta agreement and up to date AI amendment. 

<div style="width: 100%; overflow: hidden;"> <iframe src="https://canvas-medical.portal.usepylon.com/forms/hyperscribe-interest" title="Hyperscribe Interest Form" width="100%" height="500" frameborder="0" allow="clipboard-write" style="display: block; border: 0; width: 100%; max-width: 100%;" ></iframe> </div>




