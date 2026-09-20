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

1. **Pick the visit.** The panel lists the provider's day in time order. A visit is entered
   by pressing its card, or by the chart announcing the note the provider just expanded. The
   panel opens nothing on its own, a day holding a single visit included, because a panel
   that chose for the provider would record into a note nobody named.
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

The panel is a dock rather than a modal because a recording has to survive navigation: a
modal is destroyed by it and takes the recording with it. The recording is held to the visit
the provider started it on, not to whatever page they are looking at, so they can go to
another chart, the schedule, or their inbox while it runs. The panel names the patient it is
recording, and keeps naming them when it is collapsed to a rail, because a live microphone
whose chart is nowhere on screen has to say whose visit it is filing against.

## Try the interface

The panel below is the beta interface, running on sample data. There is no back end behind
it and no patient data in it: the visit, the transcript and the suggestions are fixed. It
walks a visit end to end, with a guide in the corner saying what to press.

<style>
/* The docs content column is capped at 800px (_scss/_pagelayout.scss), which is not
   enough room for a two-pane EHR: at 1:1 the app gets 800px total, the 420px panel
   takes half of it, and the chart beside it is unreadable.

   So the frame is given a viewport 1/scale wider than the column and drawn at `scale`.
   `width: calc(100% / var(--embed-scale))` is what makes that responsive: the frame is
   1.43x the column, scaled to 0.7, which lands at exactly 100% again. At an 800px
   column the app sees about 1140px, which is enough for the panel and the chart both.

   To change how much is shown, change --embed-scale and nothing else. Lower shows more
   and reads smaller. Clicks map correctly through a transform, so the frame stays
   interactive. */
.scribe-embed {
  --embed-scale: 0.7;
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
          title="AI Scribe interface preview"
          allow="clipboard-write"></iframe>
</div>

<p>It is shown at 70% so the whole workspace fits the column.
<a href="/assets/static/ai-scribe-preview.html" target="_blank" rel="noopener">Open it in its own tab</a>
for it at full size.</p>

## What it does

### Recording

- Record, pause and resume a visit from a panel docked beside the chart. Pause releases the
  microphone and Resume continues the same timeline, so a visit interrupted partway is still
  one recording.
- The recording is held to the visit rather than to the page, so a provider can keep working
  elsewhere in Canvas while it runs.
- Transport controls stay reachable when the panel is collapsed to a rail, along with the
  name and date of birth of the patient being recorded.
- A live transcript, attributed to the person who spoke each line, and read back intact
  after a page reload.

### Drafting

- The active transcription engine drafts the note from the transcript it holds. The core
  reads that draft and produces the command proposals.
- Progress is reported step by step while it drafts.
- Per-provider custom instructions, written in plain language, are carried into every draft
  that provider's Scribe makes. They change how the draft is written, not what the recording
  captures.

### Review

- Proposals are grouped the way a visit is worked through: History, Exam, and Assessment and
  Plan. Assessment and Plan are one group because they are decided together.
- A proposal matched to a command the note already holds offers to **update** it rather than
  adding a second copy. This is what lets Scribe fill a note type's template instead of
  working around it.
- A proposal is labeled when the chart already carries something similar. It stays addable,
  because the chart carrying something similar is information rather than a decision.
- A proposal from a recommender, rather than one extracted from what was said, is marked as
  a recommendation and is never pre-selected.
- Where a proposal came out of a specific moment, it carries the transcript's own words for
  that value, and pressing them goes to that point in the transcript.
- **Free text is editable in the panel.** A field the command takes as free text can be
  fixed before it is written. A field backed by a code system, an option set, a date or a
  constrained number is shown and left to the note, because changing it needs the chart's
  own autocomplete.
- Add one proposal, add a selection, or add all. A dismissed proposal drops to a section at
  the bottom of the list and can be restored, rather than disappearing.

### Fit with the chart

- Every command is staged in the note as the provider, so the finished note carries no
  marker distinguishing a Scribe-proposed command from a hand-entered one.
- A proposal is colored by the note section its command will land in, using the note's own
  section palette.
- Scribe is offered only on the note types the instance chooses. A visit of any other type
  is listed and shown as unavailable rather than silently missing.

### The day

- The panel lists the provider's day in the order the calendar shows it, by time, with what
  Scribe still owes on each visit in the status line.
- A signed visit says whether Scribe was part of it. One Scribe recorded offers a way back
  into the transcript and what was suggested; one signed without it has nothing for the
  panel to show and says so.

## Getting good audio

Suggestions rather than requirements. Scribe records through the browser using your
computer's **default microphone**, so it works with whatever you already have and there is
nothing to install. That also means it does not know or care which microphone that is, and
it has no device picker of its own yet: if you plug something in, make it the default in
your operating system's sound settings, or set it for the Canvas site in your browser's
site settings.

Audio reaches the transcription engine as 16 kHz mono, which is the band speech lives in.
That matters for what to spend money on. A more expensive microphone mostly buys fidelity
above that band, and that fidelity is discarded. What is not discarded is how far the
microphone is from each person, how much of the room it hears, and how much the room echoes,
and those are what a transcript's accuracy actually turns on.

So, in rough order of how much difference each makes:

- **Move the microphone off the laptop and into the middle of the room.** A tabletop
  microphone roughly equidistant from both people hears them about equally. A laptop
  microphone is close to whoever is typing and far from whoever is on the exam table, and
  many laptops steer their microphone array toward the person at the keyboard, which is the
  wrong person.
- **Prefer an omnidirectional tabletop microphone** over anything aimed in one direction. A
  USB conference speakerphone is the usual shape of this. Canvas has not benchmarked
  specific models, so treat any particular product as a starting point rather than a
  recommendation from us, and tell us what worked.
- **Wired USB over Bluetooth.** Bluetooth drops and renegotiates over a long session, and
  often switches to a low-quality profile when the microphone opens.
- **Smaller, softer rooms transcribe better.** Echo off hard walls arrives at the microphone
  as a smeared copy of what was just said, and the engine has to sort one from the other.
- **Close anything else using the microphone.** A video call, another recorder, or a
  note-taking app can hold the device, and the browser may then get nothing.

### Telehealth

Scribe captures a microphone, not your computer's audio output and not a video call's
stream. On a video visit the patient's voice reaches the microphone only by coming out of
your speakers into the room, and the browser's echo cancellation is designed to remove
exactly that, so it will work against you. On headphones it never reaches the microphone
at all.

Treat telehealth as unsupported for now rather than as something to work around. If it is
important to your practice, tell us, because it changes what we build next.

## Limits worth knowing before you enroll

These are deliberate properties rather than open defects, and each one is a question a
beta participant will ask:

- **One generation per visit.** Finishing the recording is what asks for the note; there is
  no regenerate. A second pass would produce a different set of suggestions over the first,
  which leaves a provider mid-review to reconcile two.
- **No level meter and no prolonged-silence warning.** Neither is expressible over the
  interface between the app and the engine, so both are absent rather than shown as controls
  that do nothing. The elapsed timer is the browser's clock, not a signal from the engine.
- **Finalizing is one-way.** A visit's recording cannot be reopened after it is finished.
- **Scribe records a microphone, not a video call.** There is no capture of your
  computer's audio output or of a call's stream, so telehealth is not supported today. See
  Getting good audio.
- **No microphone picker in Scribe.** It records through whatever your operating system or
  browser has set as the default input. Changing microphones is done there, not here.
- **Coded fields are not editable in the panel.** A code, an option set, a date or a
  constrained number needs the chart's own autocomplete, so Scribe shows it and leaves it to
  the note. Free text is the part the panel can fix.
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
