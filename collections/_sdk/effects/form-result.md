---
title: "Form Result"
slug: "form-result-effect"
excerpt: "Effect for dynamically displaying forms in the Patient Portal"
hidden: false
---

## Overview

Forms are a key part of the Patient Portal experience.
They allow developers to dynamically display questionnaires to patients based on various criteria
and optionally create a Questionnaire Command within a Note.
Since these effects are evaluated on every page load, it’s essential to ensure that only the appropriate forms are
shown.

## Structure

A Form Result effect consists of the following properties:

- **questionnaire_id**: The unique identifier for the Questionnaire.
- **create_command**: A boolean flag that, when set to `True`, creates a Questionnaire Command within a Note.
- **note_id**: Optionally associates the effect with an existing Note.

These properties ensure that the effect integrates seamlessly with the rest of the Canvas SDK.

### **Attributes**

| Attribute          | Type   | Description                                                  |
|--------------------|--------|--------------------------------------------------------------|
| `questionnaire_id` | `str   | UUID`                                                        | The unique ID of the Questionnaire. |
| `create_command`   | `bool` | If `True`, a Questionnaire Command is created inside a Note. |
| `note_id`          | `str   | UUID                                                         | None` | Associates the response with an existing Note if applicable. |
