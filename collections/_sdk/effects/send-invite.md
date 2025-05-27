---
title: "Send Patient Portal Invitation"
slug: "send-invite-effect"
excerpt: "Effect used to send an invitation to the patient portal."
hidden: false
---

## Overview

This effect triggers a portal invitation that allows the patient to register or activate their account on the patient portal.

### Details

This effect includes a timeout that prevents the invitation from being sent if it has already been triggered within the last 24 hours.

## Structure

A Send Invite effect consists of the following properties:

- **user_dbid**: The unique identifier for the User.

### **Attributes**

| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `user_dbid`        | `str   | UUID`                                                        | The unique ID of the User. |
