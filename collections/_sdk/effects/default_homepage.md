---
title: "Default Homepage"
slug: "default-homepage-effect"
excerpt: "Effect for setting a provider's default homepage in Canvas"
hidden: false
---

This allows developers to set a provider's default homepage in Canvas. The default homepage is the page that a provider sees when they log in to Canvas. This effect can be used to set the default homepage to a specific page or a plugin application. For more guidance, see "[How to set a default homepage for the provider application](/guides/set-default-homepage/)".

Build a `DefaultHomepageEffect` with a `page` or an `application_identifier`, then return its `apply()` from a `GET_HOMEPAGE_CONFIGURATION` handler.

## Methods

### apply() → Effect

Sets the default homepage for the user logging in.

- Either `page` or `application_identifier` is required. If both are set, `application_identifier` takes precedence and the homepage is that application.
- `application_identifier` must be the identifier of an installed application.

When no plugin returns this effect, the default homepage is the schedule.

## Attributes

| Attribute                | Type                   | Description                                                   | Required                                        |
|--------------------------|------------------------|---------------------------------------------------------------|-------------------------------------------------|
| `page`                   | [`Pages`](#pages) `\| None` | The Canvas page to open.                                | One of `page` or `application_identifier`       |
| `application_identifier` | `str \| None`          | The identifier of the plugin application to open.             | One of `page` or `application_identifier`       |

## Pages

An enumeration of pages that can be set as the default homepage, accessed as `DefaultHomepageEffect.Pages.<value>`:

| Value              |
|--------------------|
| `PATIENTS`         |
| `SCHEDULE`         |
| `REVENUE`          |
| `CAMPAIGNS`        |
| `DATA_INTEGRATION` |

## Example

```python
from canvas_sdk.effects.default_homepage import DefaultHomepageEffect

DefaultHomepageEffect(page=DefaultHomepageEffect.Pages.PATIENTS).apply()
```

```python
from canvas_sdk.effects.default_homepage import DefaultHomepageEffect

DefaultHomepageEffect(application_identifier="app_identifier").apply()
```
