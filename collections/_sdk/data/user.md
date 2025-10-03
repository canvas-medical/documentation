---
title: "User"
slug: "data-user"
excerpt: "Canvas SDK User"
hidden: false
---

## Introduction

The `CanvasUser` model represents a Canvas User.

## Basic usage

To get a user by identifier, use the `get` method on the `CanvasUser` model manager:

```python
from canvas_sdk.v1.data import CanvasUser

user = CanvasUser.objects.get(dbid=123)
```

## Filtering

Users can be filtered by any attribute that exists on the model.

Filtering for users is done with the `filter` method on the `CanvasUser` model manager.

### By attribute

Specify attributes with `filter` to filter by those attributes:

```python
from canvas_sdk.v1.data import CanvasUser

users = CanvasUser.objects.filter(phone_number="1111111111", email="test@canvasmedical.com")
```

## Attributes

### User

| Field Name               | Type                                                                      |
|--------------------------|---------------------------------------------------------------------------|
| dbid                     | Integer                                                                   |
| email                    | String                                                                    |
| phone_number             | String                                                                    |
| last_invite_date_time    | DateTime                                                                  |

<br/>
<br/>
<br/>