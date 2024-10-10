---
title: Manually Sync Google Calendars
tags: beta config
date: 2024-08-05
layout: productupdates
---

Historically, our integration with gCal required us to pull from Google,loading availability every time the page loaded. To improve reliablity and load times, we are transitioning to storing availability from Google directly in Canvas. The Google API does expect some failures with their notifications, resulting in events in Google not being represented in Canvas. When this occurs, Canvas Support can now manually sync calendars in admin to capture any missed events. 