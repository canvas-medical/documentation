---
title: Fix Assess Coding Gaps Entered in Error (EIE) workflow
tags: ui bugfix
layout: productupdates
date: 2025-04-07
---

Previously, when Assess Coding Gaps were EIE, the downstream actions were not rolled back. With this fix, when a Assess Coding Gap is EIE, the associated condition created from the coding gap will be removed from the patient summary and the billing footer as long as the associated condition itself has not been assessed.