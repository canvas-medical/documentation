---
title: Addresses Errors when Using Automations that include the SDK Prescribe & Refill Commands
tags: beta bugfix sdk
date: 2024-10-29
layout: productupdates
---
We added validation to the quantity field in the new prescribe and refill commands to prevent trailing zeros. Automations created with trailing zeros were causing errors. This update ensures that these errors no longer occur.

