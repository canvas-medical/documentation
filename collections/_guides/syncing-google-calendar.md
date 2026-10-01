---
title: "Syncing Your Schedule with Google Calendar"
---

Connect your own Google account to Canvas to keep your Canvas schedule and your Google Calendar in step. Once you connect, your Canvas appointments appear on a calendar in your Google account. Busy time on the Google calendars you choose blocks the same times on your Canvas schedule. Patients and staff can't book you into a meeting that's already on your Google Calendar.

Each provider connects their own account, and both Google Workspace accounts and personal Gmail accounts work. This page covers connecting, choosing calendars, what syncs in each direction, and disconnecting.

{% include alert.html type="info" content="Google Calendar sync is turned on per instance. If <b>Google Calendar</b> doesn't appear in your Canvas menu, contact <a href='https://canvas-medical.help.usepylon.com/'>Canvas Support</a> to ask about enabling it." %}

## How the sync works

The sync runs in two directions:

- **Canvas to Google.** Canvas creates a calendar named **Canvas (Busy)** in your Google account and copies your Canvas appointments onto it. Canvas owns this calendar and keeps it matched to your Canvas schedule.
- **Google to Canvas.** Canvas reads the calendars you select and adds a **Busy** block to your Canvas schedule for each event that shows you as busy. Those times are no longer available for booking.

Canvas checks for changes in both directions every 15 minutes. Appointments you book, reschedule, or cancel in Canvas usually reach Google shortly after you save them, without waiting for the next check.

## Connect your Google account

Connect your account once to start syncing.

1. In the Canvas menu, select **Google Calendar**. The Google Calendar page opens in a new tab.
2. Select **Connect Google Calendar**.
3. Sign in to the Google account whose calendar you want to sync.
4. On Google's consent screen, leave every requested permission selected, then continue. Canvas needs all of them, and the connection fails if you clear any.

Google returns you to the Google Calendar page, which shows that your account is connected. Canvas creates the **Canvas (Busy)** calendar and copies your appointments to it, usually within about a minute.

Canvas asks Google for permission to:

- Create and manage the **Canvas (Busy)** calendar. Canvas doesn't change your other calendars.
- See your list of calendars, so you can choose which ones to sync.
- Read the events on your calendars, so Canvas can block the times you're busy.

## Choose which calendars block your Canvas schedule

Choose the Google calendars whose busy time should block your availability in Canvas. Until you select at least one, Google events don't affect your Canvas schedule.

1. On the Google Calendar page, select each calendar you want to sync. If the list is empty, wait a few minutes and refresh the page.
2. Select **Save selection**.

Canvas imports busy time from the selected calendars right away and checks them every 15 minutes after that. To stop a calendar from blocking your schedule, clear it and select **Save selection** again. Canvas removes the **Busy** blocks that came from that calendar.

## What appears in Canvas

Busy time from Google appears on the day and week views of your Canvas schedule as a block labeled **Busy**. Canvas doesn't copy the event's title, attendees, or other details. Appointments can't be booked into a **Busy** block.

An event blocks your schedule when it shows you as busy. Canvas skips these events:

- Events marked as free in Google.
- Events you've declined.
- Cancelled events.

All-day, multi-day, and recurring busy events block each day they cover.

## What appears in Google

Each Canvas appointment appears on the **Canvas (Busy)** calendar as a private event titled with the appointment's visit type, such as "Office Visit." The event doesn't include the patient's name or any other patient information, and it doesn't include a telehealth meeting link. Open the appointment in Canvas to see those details.

When an appointment is cancelled, rescheduled, or moved to another provider in Canvas, Canvas removes its event from your **Canvas (Busy)** calendar.

### Make changes in Canvas, not Google

Canvas overwrites changes made to its events in Google. If you move, resize, rename, or delete an event on the **Canvas (Busy)** calendar, Canvas puts it back within about 15 minutes. Reschedule or cancel the appointment in Canvas instead.

Events you add to the **Canvas (Busy)** calendar yourself aren't sent to Canvas, and Canvas leaves them alone. To block time in Canvas, add the event to one of your selected calendars instead.

## Reconnect when the connection expires

The sync stops for your account if your Google access expires or is revoked. For example, removing Canvas's access in your Google account settings revokes it. The Google Calendar page then shows a message that your connection has expired or was revoked. To resume syncing:

- On the Google Calendar page, select **Reconnect Google Calendar** and sign in again.

You can reconnect with a different Google account. Canvas first removes the previous account's **Canvas (Busy)** calendar and **Busy** blocks, then starts syncing the new account.

## Disconnect Google Calendar

Disconnect when you no longer want your Canvas schedule synced with Google.

1. In the Canvas menu, select **Google Calendar**.
2. Select **Disconnect**.

Canvas stops syncing and deletes the **Canvas (Busy)** calendar from your Google account. It also removes the **Busy** blocks that came from Google, so those times become available for booking again. Your other Google calendars and their events don't change.

<br/>
<br/>
<br/>
