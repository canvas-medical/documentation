---
title: "ProtocolCurrent"
slug: "data-protocol-current"
excerpt: "Canvas SDK ProtocolCurrent"
hidden: false
---

## Introduction

The `ProtocolCurrent` object represents the current state of clinical protocols applied to patients within Canvas. Protocols are structured plans or guidelines that outline specific medical interventions, treatments, or care pathways for managing various health conditions. The `ProtocolCurrent` object contains essential information about the protocol's status, associated patient, and relevant clinical details.

## Basic Usage

To get a protocol by identifier, use the `get` method on the `ProtocolCurrent` model manager:

```python
from canvas_sdk.v1.data.protocol_current import ProtocolCurrent

protocol = ProtocolCurrent.objects.get(id="12345678-1234-1234-1234-123456789012")
```

## Filtering

```python
from canvas_sdk.v1.data.protocol_current import ProtocolCurrent

protocols = ProtocolCurrent.objects.filter(status="active", patient_id="b80b1cdc2e6a4aca90ccebc02e683f35")

## Attributes

### ProtocolResult

| Field Name             | Type          |
| ---------------------- | ------------- |
| id                     | UUID          |
| dbid                   | Integer       |
| created                | DateTime      |
| modified               | DateTime      |
| title                  | String        |
| narrative              | String        |
| result_identifiers     | Array[String] |
| types                  | Array[String] |
| protocol_key           | String        |
| plugin_name            | String        |
| status                 | String        |
| due_in                 | DateTime      |
| days_of_notice         | Integer       |
| snoozed                | Boolean       |
| sources                | Array[String] |
| recommendations        | Array[String] |
| top_recommendation_key | String        |
| next_review            | DateTime      |
| feedback_enabled       | Boolean       |
| plugin_can_be_snoozed  | Boolean       |
| patient_id             | UUID          |
| result_hash            | String        |
| snooze_date            | DateTime      |
```
