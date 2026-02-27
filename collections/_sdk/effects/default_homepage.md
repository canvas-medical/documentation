---
title: "Default Homepage"
slug: "default-homepage-effect"
excerpt: "Effect for setting a provider's default homepage in Canvas"
hidden: false
---

## Overview

This allows developers to set a provider's default homepage in Canvas. The default homepage is the page that a provider sees when they log in to Canvas. This effect can be used to set the default homepage to a specific page or a plugin application. For more guidance please reference "[How to set a default homepage for the provider application](/guides/set-default-homepage/)"

```python
from canvas_sdk.effects.default_homepage import DefaultHomepageEffect

DefaultHomepageEffect(page=DefaultHomepageEffect.Pages.PATIENTS).apply()
```

```python
from canvas_sdk.effects.default_homepage import DefaultHomepageEffect

DefaultHomepageEffect(application_identifier="app_identifier").apply()
```

## Structure

### **Pages**

An enumeration of pages that can be set as the default homepage:

| Value             |
|-------------------|
| `PATIENTS`         
| `SCHEDULE`  |      
| `REVENUE`  |       
| `CAMPAIGNS`  |     
| `DATA_INTEGRATION`  |


### **DefaultHomepage**

A DefaultHomepage effect consists of the following properties:

#### Attributes

| Attribute     | Type                  | Description                                                                     |
|---------------|-----------------------|---------------------------------------------------------------------------------|
| `page`        | `Pages \| None`       | Optional page                                                                   |
| `application_identifier`    | `str \| None`         | Optional application identifier                                                 |  

<br/>

If both `page` and `application_identifier` are provided, `application_identifier` will take precedence and the default homepage will be set to the specified application. If neither is provided, the default homepage will be set to the Canvas default homepage.
