---
permalink: /product-updates/google-calendar-sync/
title: "Beta | Google Calendar Sync"
layout: betas
---

{% include alert.html type="warning" content="<b>Beta Participation:</b> Google Calendar sync is in limited beta and is turned on per instance. Reach out to Canvas support to be added to the waitlist." %}

## Overview

Each provider can connect their own Google account to Canvas and keep their calendars in sync both ways. Their Canvas appointments copy to a **Canvas (Busy)** calendar in Google, and busy events on the Google calendars they select block that time on their Canvas schedule. For setup steps and how each kind of Google event is handled, see [Connecting Your Google Calendar to Canvas](https://help.canvasmedical.com/articles/3718601633-connecting-google-calendar-to-canvas).

## Expected Benefits

**One calendar view for providers:** Canvas appointments appear in the provider's Google Calendar showing only the visit type and time, with no patient details.

**Fewer conflicting bookings:** Busy time from a provider's Google calendars is left out of available times everywhere Canvas offers them, including the schedule, patient self-scheduling and the FHIR Slot API.

## For developers

Google busy time is stored as busy blocks on the provider's schedule, separate from appointments.

- **[Slot](/api/slot/) search** leaves out times covered by a connected provider's busy blocks, the same way it leaves out booked appointments.
- **[Appointment](/api/appointment/) create and update** treat a busy block like a booked appointment when double booking is turned off: a request that overlaps one returns a `422` with `This appointment time is no longer available.` When double booking is allowed, busy blocks don't stop the request.
- **Busy blocks are not appointments or calendar events.** They aren't returned by FHIR [Appointment](/api/appointment/) search or by the SDK [Appointment](/sdk/data-appointment/), [Calendar, or Event](/sdk/data-calendar/) data models, and they don't send appointment events such as `APPOINTMENT_CREATED` to plugins. To find a provider's open times including Google busy time, use FHIR [Slot](/api/slot/) search.
- **Plugins read sync data through the [Google Calendar data models](/sdk/data-google-calendar/).**
  - [`GoogleCalendarBusyBlock`](/sdk/data-google-calendar/#googlecalendarbusyblock): a provider's busy time, through `google_calendar_busy_blocks` on [Staff](/sdk/data-staff/). Filter on `active=True` for current busy time.
  - [`GoogleCalendarConnection`](/sdk/data-google-calendar/#googlecalendarconnection): a provider's Google connection, through `google_calendar_connection` on Staff, including whether it needs reconnecting.
  - [`GoogleCalendar`](/sdk/data-google-calendar/#googlecalendar): the calendars on a connection, and which ones the provider selected.
- **Plugin [Appointment and ScheduleEvent effects](/sdk/effect-notes/#appointment-effect) don't check busy blocks.** Whatever the double booking setting, an appointment or schedule event a plugin creates, updates, or reschedules can overlap a provider's Google busy time.
- **The sidebar entry** for the sync page is the `GOOGLE_CALENDAR` item in the [layout effect](/sdk/layout-effect/), which renders only on instances in the beta.
