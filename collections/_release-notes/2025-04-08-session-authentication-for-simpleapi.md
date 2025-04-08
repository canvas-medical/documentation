---
title: SimpleAPI Session Authentication
tags: sdk
layout: productupdates
date: 2025-04-08
---

When serving HTTP requests from your SimpleAPI handler, you can now use Canvas
session information to authenticate your endpoints.

This allows you to restrict requests to only logged in users, or be even more
specific in your authorization by limiting certain requests to just patients,
just staff, or based on any information specific to that logged in user.

Using this will allow you to create and serve responses that are aware of who
the logged in user is.

See [SimpleAPI Authentication Options](/sdk/handlers-simpleapi/#session) for more details.


