---
title: "Syncing Provider Google Calendars"
guide_for:
- /api/slot/
- /api/appointment/
---

Each provider can connect their own Google account to Canvas, whether it is a Google Workspace account or a personal Gmail account. Once connected, Canvas copies the provider's appointments to their Google Calendar, and busy time on their Google calendars blocks their availability in Canvas. This guide explains what syncs in each direction and what changes for integrations and plugins that read the schedule.

{% include alert.html type="info" content="Google Calendar sync is off by default. <a href='https://canvas-medical.help.usepylon.com/'>Contact Support</a> to turn it on for your instance." %}

## Connecting a calendar

A provider opens **Google Calendar** from the account menu, connects their Google account, and chooses which of their Google calendars Canvas should read. Every provider connects separately, so each one controls their own account.

Canvas syncs about every 15 minutes. A provider's appointments appear in Google within about a minute of connecting.

## Canvas appointments in Google

Canvas creates a calendar named **Canvas (Busy)** in the provider's Google account and keeps their Canvas appointments on it.

- Each event shows the visit type and time only. Events carry no patient information and no meeting link.
- Canvas is the source of truth. If someone moves, edits, or deletes one of these events in Google, Canvas puts it back on the next sync.
- When an appointment is cancelled, rescheduled, or moved to another provider in Canvas, its event is removed from this calendar.
- Events added by hand to **Canvas (Busy)** stay in Google and are not sent to Canvas.

## Google busy time in Canvas

Busy events on the calendars a provider selects become busy blocks in Canvas. They show as "Busy" on the provider's day and week schedule, with no title or details from Google.

- Canvas reads events from 31 days ago through 183 days ahead.
- Events marked "Free" in Google, cancelled events, and events the provider declined do not block time.
- An event that spans several days, or a recurring event, blocks each day it covers.
- A meeting that appears on more than one selected calendar blocks time once.

## What this means for integrations and plugins

- **Slot search reflects Google busy time.** The [Slot](/api/slot/) endpoint leaves out times that a connected provider's busy blocks cover, so a self-scheduling app built on it does not offer those times.
- **Busy blocks are not appointments.** They do not appear in [Appointment](/api/appointment/) search, and they do not emit appointment events such as `APPOINTMENT_CREATED` to plugins.

## Disconnecting

A provider can disconnect from the same page. Canvas deletes the **Canvas (Busy)** calendar from their Google account, removes the busy blocks it imported, and revokes its access to the account.

If Google access stops working, for example because the provider removed Canvas from their Google account settings, sync pauses for that provider and the page asks them to reconnect.
