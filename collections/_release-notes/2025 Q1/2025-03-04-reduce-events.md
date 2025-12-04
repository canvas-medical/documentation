---
title: Reduces Emission of Unecessary Model Update Events
layout: productupdates
tags: plugins sdk
date: 2025-03-04
---

We've reduced unnecessary model update events by suppressing cases where the only detected change is a modified timestamp. This prevents updates from being triggered when no meaningful data has changed