---
title: Add Commands to All Unlocked Notes
tags: beta bugfix
date: 2024-08-13
layout: productupdates
---
When using the Commands API, there is validation to ensure that commands are only added to unlocked notes. We fixed a bug that caused the incorrect state to be returned when multiple note state change events had occured (locking & unlocking).
