---
title: "Application"
slug: "data-application"
excerpt: "Canvas SDK Application"
hidden: false
---

## Introduction

The `Application` model represents a plugin Application in Canvas. Applications are used to integrate third-party tools and services into the Canvas platform, allowing users to access external resources and functionalities directly from within Canvas. Each application has a unique identifier, name and description.

## Basic usage

To get an application by identifier, use the `get` method on the `Application` model manager:

```python
from canvas_sdk.v1.data import Application

application = Application.objects.get(identifier="123")
```

## Filtering

Applications can be filtered by any attribute that exists on the model.

Filtering for applications is done with the `filter` method on the `Application` model manager.

### By attribute

Specify an attribute with `filter` to filter by that attribute:

```python
from canvas_sdk.v1.data import Application

applications = Application.objects.filter(name="application name")
```

## Attributes

### Application

| Field Name          | Type                                                    |
| ------------------- | ------------------------------------------------------- |
| identifier          | str                                                     |
| name                | str                                                     |
| description         | str                                                     |
