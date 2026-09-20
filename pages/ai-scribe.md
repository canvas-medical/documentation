---
permalink: /product-updates/ai-scribe/
layout: betas
title: "Beta | AI Scribe"
date: 2026-09-20
---

{% include alert.html type="warning" content="<b>Beta participation:</b> AI Scribe is in private beta and is not enabled by default. Participation requires a signed beta agreement. Use the interest form at the bottom of this page, or email <a href='mailto:product@canvasmedical.com'>product@canvasmedical.com</a>." %}

## Overview

AI Scribe turns a recorded visit into a reviewable draft and a set of Canvas commands. It
records the room from a panel docked beside the chart, sends the audio to a transcription
engine, drafts the note from the transcript, and reads that draft back as commands the
provider reviews one at a time.

Nothing reaches the chart until a provider adds it. Every command Scribe proposes is staged
in the note as the provider, through the same path a typed command takes, so the resulting
note carries no marker distinguishing a Scribe-proposed command from a hand-entered one.

It ships as a set of Canvas plugins rather than as a feature of the platform, which is what
makes the pieces separable:

| Plugin | Role |
| --- | --- |
| The app | The provider-facing panel: the day's visits, the recording session, and the review screen. Served from the plugin itself and mounted in the right-hand dock. |
| The core | The clinical half. Owns the transcript and the draft note, and turns the draft into command proposals. Carries no vendor-specific code. |
| A vendor | One plugin per transcription engine. Two routes, no storage. |

The transcript and the draft belong to the core plugin, not to the engine. An instance can
change transcription engine without losing the visits it has already recorded: a swap
changes which engine drafts the next note and nothing else.

## How a visit flows

1. **Pick the visit.** The panel lists the provider's day. A visit is entered by pressing
   its card, or by the chart announcing the note the provider just expanded. The panel opens
   nothing on its own, a day holding a single visit included, because a panel that chose for
   the provider would record into a note nobody named.
2. **Record.** Audio streams to the active engine. Pause releases the microphone and Resume
   continues the same timeline, so a visit interrupted partway is still one recording.
3. **Read the transcript as it settles.** Lines are attributed to the person who spoke them.
   An utterance still resolving shows as unattributed, because the engine revises both the
   text and the speaker as it settles, and a name drawn too early is a name that changes
   under the provider.
4. **Finish.** Finishing finalizes the visit's recording, which is one-way, and triggers
   generation. The engine drafts a note from the transcript it holds; the core reads that
   draft and produces the command proposals.
5. **Review.** Each proposal shows what it would write, the section of the note it will land
   in, and the transcript's own words behind it where there are any.
6. **Add.** Adding stages the command in the note, where the provider finishes and signs it.

A recording survives navigating around the chart, which is the reason the panel is a dock
rather than a modal: a modal is destroyed by navigation and takes the recording with it.
Moving to a different patient's chart does end the recording, deliberately, because a
recording belongs to a visit and one still running on another patient's chart is a
transcript about to be filed against the wrong person.

## What the review screen knows

A proposal is not offered blind. Before the provider sees it, the core has checked it
against the note and against the chart:

- **Already on the note.** A proposal matched to a command the note already holds offers to
  **update** that command rather than adding a second copy of it. This is what lets Scribe
  work with a note type's template instead of around it: a template that stages a Reason for
  visit, an empty HPI and an unanswered questionnaire gets those filled, not duplicated.
- **Already on the chart.** A proposal whose content resembles something the chart already
  carries is labeled as such. It stays addable, because the chart carrying something
  similar is information rather than a decision.
- **Recommendations.** A proposal from a recommender, rather than one extracted from what was
  said, is marked as a recommendation and is never pre-selected.
- **Evidence.** Where a proposal came out of a specific moment, it carries the transcript's
  own words for that value.

Proposals are colored by the note section the command will land in, using the note's own
section palette, so a card wears the color the command will wear once it is in the note.

## Try the interface

The panel below is a live design preview of the beta interface. It is a front-end mock with
no back end: the visit, the transcript and the suggestions are fixed sample data, and no
patient data is involved. It walks the happy path end to end, with a guide in the corner.

<iframe src="/assets/static/ai-scribe-preview.html"
        title="AI Scribe interface preview"
        width="100%" height="900"
        style="border: 1px solid #ccc; background: #fff;"
        allow="clipboard-write"></iframe>

<p><a href="/assets/static/ai-scribe-preview.html" target="_blank" rel="noopener">Open the preview in its own tab</a></p>

{% include alert.html type="info" content="The preview shows the interface as it is being designed for the beta, which is ahead of what is deployed today. The table below says which is which." %}

## What is in the beta today

| Capability | State |
| --- | --- |
| Record, pause, resume, finish a visit from a docked panel | Available |
| Live speaker-attributed transcript, recovered after a page reload | Available |
| Draft note generated from the transcript, with per-step progress | Available |
| Command proposals reviewed and added one at a time | Available |
| Proposals matched to commands already on the note, offering an update | Available |
| Proposals labeled when the chart already carries something similar | Available |
| Recommendations told apart from what the visit said | Available |
| Transcription engine selected per instance, swappable | Available |
| Scribe restricted to chosen note types | Available |
| Free-text fields edited in the panel before they are written | In design |
| Dismissed suggestions recoverable rather than discarded | In design |
| Day list ranked by what Scribe still owes on each visit | In design |
| Recording that continues while the provider works on another page | In design |
| Per-provider custom drafting instructions | In design |
| Transport controls on the collapsed panel | In design |
| Evidence linked to its moment in the transcript | In design |
| Per-visit audit trail of accepts and dismissals | In design |

## Limits worth knowing before you enroll

These are properties of the current design rather than open defects, and each one is a
question beta participants have asked:

- **One generation per visit.** Finishing the recording is what asks for the note; there is
  no regenerate. A second pass would produce a different set of suggestions over the first,
  which leaves a provider mid-review to reconcile two.
- **A suggestion is edited in the note, not in the panel, today.** Editing free text in the
  panel is in design; until then a proposal is added and then finished in the note.
- **No level meter and no prolonged-silence warning.** Neither is expressible over the
  interface between the app and the engine, so both are absent rather than shown as controls
  that do nothing. The elapsed timer is the browser's clock, not a signal from the engine.
- **Finalizing is one-way.** A visit's recording cannot be reopened after it is finished.
- **The panel is not a second chart.** Signing, billing and everything else about the note
  stays in the note.

## Configuration

Set per instance when the plugins are installed:

| Setting | What it decides |
| --- | --- |
| Active vendor plugin | Which transcription engine drafts the note |
| Note types | Which note types Scribe is offered on. A visit of any other type is listed and shown as unavailable rather than silently missing |
| Vendor credentials | The engine's API key |
| Namespace read key | Lets the vendor plugin read the core's transcript, read-only |

The sharing between plugins runs one way and read-only. A vendor plugin declares read access
on the core's namespace and mirrors the one model it needs; the core declares nothing about
the vendor and never calls it. That direction is deliberate: namespace access is granted per
plugin rather than per table, so a grant the other way would hand a transcription vendor
write access across everything the core stores.

## Joining the beta

Participation is by agreement, and enrolllment is per instance rather than per user. Two steps:

1. Tell us you are interested, using the form below.
2. Sign the AI Scribe beta agreement. Your Canvas team will send it, and it covers what the
   beta includes, how recordings and transcripts are handled, and what either side can
   expect while the feature is in beta.

<!-- TODO before merge: create the Google Form and paste its embed URL below.

     Google Forms embed pattern:
       Form -> Send -> the < > (embed) tab gives the src, which looks like
       https://docs.google.com/forms/d/e/<LONG_FORM_ID>/viewform?embedded=true

     Then replace the placeholder block below with:
       <iframe src="https://docs.google.com/forms/d/e/<LONG_FORM_ID>/viewform?embedded=true"
               title="AI Scribe beta interest form"
               width="100%" height="900" frameborder="0"
               marginheight="0" marginwidth="0"
               style="border: 1px solid #ccc; background: #fff;">Loading form...</iframe>

     Fields the form should collect, matching what enrolllment needs:
       - Instance name / slug
       - Your name and email
       - Roughly how many providers would use it
       - Which note types you would want it on
       - Which transcription engine you already have a contract with, if any
       - Anything about your care model that would change how a note is drafted

     This page should not ship with the placeholder: the email fallback works, but the
     form is the route the page promises. -->

<div style="border: 1px solid #ccc; padding: 24px; text-align: center; background: #fafafa;">
  <p><b>Interest form</b></p>
  <p>The form is not embedded yet. In the meantime, email
  <a href="mailto:product@canvasmedical.com?subject=AI%20Scribe%20beta%20interest">product@canvasmedical.com</a>
  with your instance name, roughly how many providers would use it, and the note types you
  would want it on.</p>
</div>

## Questions

Email [product@canvasmedical.com](mailto:product@canvasmedical.com), or raise it with your
Canvas team in your Slack channel.
