---
title: Prevents Duplicate Reason For Visit Commands when Scheduling Follow Ups
tags: bugfix ui
layout: productupdates
date: 2024-09-16
---
After scheduling appointments via the `follow up` command workflow, the reason for visit would be duplicated in the note. We now only add two commands if the note is updated in the scheduling workflow.  