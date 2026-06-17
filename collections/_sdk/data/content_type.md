---
title: "ContentType"
slug: "data-content-type"
excerpt: "Canvas SDK ContentType"
hidden: false
---

## Introduction

The `ContentType` model provides read-only access to Django content types. Use it to look up the content type id for a given model, which is required when working with generic relations (such as [document references](/sdk/data-document-reference)) and when generating permalinks.

## Basic usage

To get a content type by its database id, use the `get` method on the `ContentType` model manager:

```python
from canvas_sdk.v1.data import ContentType

content_type = ContentType.objects.get(dbid=42)
```

## Filtering

Content types can be filtered by any attribute that exists on the model.

Filtering for content types is done with the `filter` method on the `ContentType` model manager.

### By model

To find the content type for a specific model, filter by `app_label` and `model`:

```python
from canvas_sdk.v1.data import ContentType

content_type = ContentType.objects.filter(app_label="api", model="note").first()
if content_type:
    print(f"Content type id: {content_type.dbid}")
```

## Attributes

### ContentType

| Field Name | Type    |
|------------|---------|
| dbid       | Integer |
| app_label  | String  |
| model      | String  |

- **dbid**: The internal database primary key, which is the content type id used for generic relations and permalinks.
- **app_label**: The label of the application the model belongs to (e.g., `api`).
- **model**: The lowercased name of the model (e.g., `note`).

<br/>
<br/>
<br/>
