---
title: "Update User"
slug: "update-user-effect"
excerpt: "Effect for updating a user"
hidden: false
---

## Overview

This effect is intended for updating a user’s phone number or email. In the future, we may expand its capabilities to support additional attributes, but for now, only these two are supported.

## Structure

An Update User effect consists of the following properties:

- **user_dbid**: The unique identifier for the User.
- **phone_number**: The user’s phone number to be saved.
- **email**: The user’s email to be saved.

### **Attributes**

| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `user_dbid`        | `str   | UUID`                                                        | The unique ID of the User. |
| `phone_number`     | `str`                                                                 | Specifies the phone number to be stored. |
| `email`            | `str`                                                                 | Specifies the email to be stored. |
