---
title: "Reason For Visit Setting Coding"
slug: "data-reason-for-visit-setting-coding"
excerpt: "Canvas SDK Reason For Visit Setting Coding"
hidden: false
---

## Introduction

The `ReasonForVisitSettingCoding` model represents the coding information used to populate the coding field within a
Reason For Visit in Canvas.

## Basic Usage

To retrieve a specific coding record by its identifier, use the model manager's `get` method:

```python
from canvas_sdk.v1.data import ReasonForVisitSettingCoding

rfv_coding = ReasonForVisitSettingCoding.objects.get(id="e2b1e1e3-3f52-4a0a-bb3a-123456789abc")
```

You can also filter records by attributes. For example, to get all codings from a specific coding system:

```python
codings = ReasonForVisitSettingCoding.objects.filter(system="http://snomed.info/sct")
```

## Attributes

### ReasonForVisitSettingCoding

| Field Name | Type              | Description                                                                       |
|------------|-------------------|-----------------------------------------------------------------------------------|
| id         | UUID              | The universally unique identifier for this coding record.                         |
| dbid       | Integer           | The database identifier for this coding record.                                   |
| code       | String            | The code representing the concept.                                                |
| display    | String            | The human-readable display name for the concept.                                  |
| system     | String            | The coding system (e.g., `http://snomed.info/sct`).                               |
| version    | String            | The version of the coding system.                                                 |
| duration   | Array of Duration | An array of durations (as Python `timedelta` objects) associated with the coding. |

<br/>
<br/>
<br/>
