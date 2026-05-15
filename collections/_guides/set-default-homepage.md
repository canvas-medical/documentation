---
title: "How to set a default homepage for the provider application"
guide_for:
- /sdk/events/
- /sdk/effects/
---

This guide explains how to set a default homepage for the provider application. By setting a default homepage, you can control which page users see when they first log in to the provider application, ensuring they have quick access to the most relevant information or features.

## What you'll learn:

- Use the [`Application`](/sdk/data-application) model to get a specific application.
- Use the [`DefaultHomepageEffect`](/sdk/default-homepage-effect) to set the default homepage.

## Default homepage plugin

#### 1. Set an application as the homepage

```python

from canvas_sdk.effects import Effect
from canvas_sdk.effects.default_homepage import DefaultHomepageEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import Application


class Homepage(BaseHandler):
    """Handler for homepage configuration events."""

    RESPONDS_TO = EventType.Name(EventType.GET_HOMEPAGE_CONFIGURATION)

    def compute(self) -> list[Effect]:
        """Set an application as the default homepage."""
        application = Application.objects.filter(name="custom_homepage").first()

        return [DefaultHomepageEffect(application_identifier=application.identifier).apply()]
```

#### 2. Set a specific page as the homepage

```python

from canvas_sdk.effects import Effect
from canvas_sdk.effects.default_homepage import DefaultHomepageEffect
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class Homepage(BaseHandler):
    """Handler for homepage configuration events."""

    RESPONDS_TO = EventType.Name(EventType.GET_HOMEPAGE_CONFIGURATION)

    def compute(self) -> list[Effect]:
        """Set the Patients page as the default homepage."""

        return [DefaultHomepageEffect(page=DefaultHomepageEffect.Pages.PATIENTS).apply()]
```
