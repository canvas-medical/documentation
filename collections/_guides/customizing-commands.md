---
title: "Customizing Commands Beyond the Built-ins"
guide_for:
- /sdk/commands/
- /sdk/commands-custom-command/
- /sdk/command-metadata-create-form-effect/
- /sdk/handlers-simple-api-commands/
---

The built-in [commands](/sdk/commands/) cover most charting. When a workflow needs more, you can add fields to a built-in command, show your own content on it, add commands of your own, or write commands from outside Canvas.

## Adding fields to a built-in command

<!-- source: discussion #936 -->
To collect extra information on a built-in command, such as a few more fields on a Plan, add them with the [command metadata form](/sdk/command-metadata-create-form-effect/). The fields appear with the command in the note, and their values are saved as [command metadata](/sdk/data-command/#commandmetadata).

## Showing your own content on a built-in command

To display extra information with a built-in command, such as a summary or a reference link, attach HTML to it with [`set_custom_html`](/sdk/commands/#set_custom_html). The HTML renders alongside the command in the note. The command must still be staged, not committed.

## Adding your own command

<!-- source: discussion #923 -->
To add your own named command, such as a "Wound assessment" command, there are two routes.

**A [custom command](/sdk/commands-custom-command/).** You declare it in your plugin's manifest, and it shows HTML you supply in the note. The command itself is read-only, so the work is in deciding what goes into it and when your plugin inserts it:

- **From data your plugin already has:** build the HTML from the chart or your own records and originate the command, for example from an event handler.
- **From a form you build:** gather the data in any interface your plugin shows, then originate the command when the information is ready to submit officially.
  - [Action buttons](/sdk/handlers-action-buttons/) open your form in a [modal](/sdk/layout-effect/#modals) from the note header or footer, or the chart. Good for a short form the clinician fills in once.
  - [Note applications](/sdk/handlers-embedded-applications/#note-applications) add a tab next to the note body. Good for a longer form the clinician works through during the visit.
  - Other [applications](/sdk/handlers-applications/#application-scopes), in the patient chart, the app drawer, or the [patient portal](/sdk/patient-portal/), gather data outside the note, including answers from the patient.

  The form sends its data to a [SimpleAPI](/sdk/handlers-simple-api-http/) endpoint in your plugin, which can save it as it comes in, for example in [custom data](/sdk/custom-data/), so the user can come back to an unfinished form. The custom command you originate at the end is the record in the note.

See the [CustomCommand reference](/sdk/commands-custom-command/) for manifest setup, print content, and examples.

**A questionnaire-based command.** Build a questionnaire and use it with the [Questionnaire](/sdk/effect-questionnaires/), Review of Systems, Physical Exam, or Structured Assessment command. Canvas provides the form, so clinicians answer it directly in the note.

## Writing commands from outside Canvas

When another system needs to write commands to a chart, such as an intake form, a device, or an internal tool, use [`CommandAPI`](/sdk/handlers-simple-api-commands/). It turns a command into an HTTP endpoint in your plugin: it reads the request body onto the command, validates it, and writes the command to the note. [Writing Commands Over HTTP](/guides/writing-commands-over-http/) walks through building one, including checking that the caller may write to the note.
