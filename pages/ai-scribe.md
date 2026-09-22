---
permalink: /product-updates/ai-scribe/
layout: betas
title: "Beta | AI Scribe"
date: 2026-09-20
---

{% include alert.html type="warning" content="<b>Beta participation:</b> AI Scribe is in private beta and is not enabled by default. Participation requires a signed beta agreement. Use the interest form at the bottom of this page, or email <a href='mailto:product@canvasmedical.com'>product@canvasmedical.com</a>." %}

## Overview

AI Scribe turns a recorded visit into a reviewable draft and a set of Canvas commands. It
records the room from a panel docked beside the chart, drafts the note from the transcript,
and reads that draft back as commands the provider reviews one at a time.

Nothing reaches the chart until a provider adds it, and every command is staged in the note
as the provider, through the same path a typed command takes. A finished note carries no
marker distinguishing a Scribe-proposed command from a hand-entered one.

It records in the browser. There is nothing to install.

## Try it

The panel below is the beta interface on sample data, with no back end behind it and no
patient data in it. It walks a visit end to end, with a guide in the corner saying what to
press.

<style>
/* The docs content column is capped at 800px (_scss/_pagelayout.scss), which is not enough
   room for a two-pane EHR. The frame is given a viewport 1/scale wider than the column and
   drawn at `scale`, so the app sees about 1140px. `width: calc(100% / var(--embed-scale))`
   is what keeps it responsive. Change --embed-scale and nothing else. */
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

<p>Shown at 70% so the whole workspace fits the column.
<a href="/assets/static/ai-scribe-preview.html" target="_blank" rel="noopener">Open it in its own tab</a>
for it at full size.</p>

## What it does

- **Record, pause, resume and finish** a visit from the docked panel. The recording is held
  to the visit rather than to the page, so you can work elsewhere in Canvas while it runs.
- **A live transcript**, attributed to whoever spoke each line, read back intact after a
  page reload.
- **An Additional note context box** while you record, for anything you want the draft to
  know that was not said out loud. It feeds the draft and is not written to the chart.
- **Command proposals grouped** as History, Exam, and Assessment and Plan. Add one, add a
  selection, or add all. A dismissed proposal drops to a section at the bottom and can be
  restored.
- **A proposal matched to a command the note already holds offers to update it** rather
  than adding a second copy, which is what lets Scribe fill a note type's template instead
  of working around it.
- **Free text is editable in the panel** before it is written. A field backed by a code
  system, an option set, a date or a constrained number is shown and left to the note.
- **Evidence.** Where a proposal came out of a specific moment, it carries the transcript's
  own words and links back to that point.
- **Per-provider custom instructions**, in plain language, carried into every draft.

## Where its context comes from

Five sources doing two different jobs. Keeping them apart is the difference between Scribe
filling in a note and Scribe arguing with it.

**Shapes the draft:** the **recording**, the **note context box** you type during the visit,
and your **custom instructions**. The last two exist separately because they have different
lifespans: a standing preference belongs in instructions, a detail about this visit belongs
in the box.

**Checked against, after the draft exists:** the **note's existing commands**, so a matched
proposal offers an update, and the **patient's chart**, so a proposal resembling something
already documented is labeled as such. Neither writes the draft.

Scribe does not read other visits, and there is nothing it learns from your edits.

## Getting good audio

Suggestions, not requirements. Scribe records through your computer's default microphone,
so it works with what you have, and it has no device picker of its own yet: if you plug
something in, make it the default in your system sound settings.

Audio reaches the engine as 16 kHz mono, which is the band speech lives in. A more expensive
microphone mostly buys fidelity above that band, and that fidelity is discarded. Distance,
pickup pattern and room echo are not discarded, and those are what accuracy turns on. So, in
order of how much difference each makes:

- **Move the microphone off the laptop and into the middle of the room**, roughly
  equidistant from both people. Many laptops steer their microphone array toward whoever is
  at the keyboard, which is the wrong person.
- **Prefer an omnidirectional tabletop microphone.** A USB conference speakerphone is the
  usual shape. Canvas has not benchmarked specific models, so treat any product as a
  starting point rather than a recommendation, and tell us what worked.
- **Wired USB over Bluetooth**, which drops and renegotiates over a long session.
- **Smaller, softer rooms transcribe better.** Echo arrives as a smeared copy of what was
  just said.

**Telehealth is not supported yet.** Scribe captures a microphone, not your computer's audio
output or a call's stream. On a video visit the patient's voice reaches the microphone only
by coming out of your speakers, and the browser's echo cancellation is designed to remove
exactly that. On headphones it never arrives at all.

## Limits worth knowing

- **One generation per visit.** Finishing the recording is what asks for the note; there is
  no regenerate.
- **Finalizing is one-way.** A visit's recording cannot be reopened once finished.
- **No level meter and no silence warning.** Neither is expressible across the interface
  between the panel and the engine. The elapsed timer is the browser's clock.
- **The panel is not a second chart.** Signing, billing and everything else about the note
  stays in the note.

## Join the beta

Enrollment is per instance rather than per user. Tell us you are interested below, and your
Canvas team will send the beta agreement, which covers what the beta includes, how
recordings and transcripts are handled, and what either side can expect while it is in beta.

<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSf2wv-iKI2F8MJD1Sbtiaed8NnLkA3KEC0o_ItU5JV824pjkA/viewform?embedded=true"
        title="AI Scribe beta interest form"
        width="100%" height="771" frameborder="0" marginheight="0" marginwidth="0">Loading...</iframe>

Questions: [product@canvasmedical.com](mailto:product@canvasmedical.com), or your Canvas
team in your Slack channel.
