---
title: Templating
---

# Templating

The Templating API is responsible for providing a simple interface to
define templates (e.g., HTML templates) and render them at runtime.

## Basic Usage

The interface for the `templating` module is minimal.

``` python
>>> from canvas_core import templating

>>> template_body = "<h1>{{ message }}</h1>"
>>> render_context = {"message": "Hello, world"}

# Render a template string.
>>> templating.render_template_string(template_body, render_context)
'<h1>Hello, world</h1>'

# Create a reusable Template object (stored in the database with a unique key).
>>> template = templating.create_template("my-template", template_body)

# Render a Template object.
>>> templating.render_template(template, render_context)
'<h1>Hello, world</h1>'

# Retrieve a Template object by its key.
>>> template = templating.get_template("my-template")
<Template: my-template>

# Update a Template object by its key.
>>> updated_template = templating.update_template("my-template", '<h1 class="fancy">{{ message }}</h1>')

# Delete a Template by its key.
>>> deleted_template = templating.delete_template("my-template")
>>> templating.get_template("my-template")
LookupError: Unable to find a template with key 'my-template'. Is it correct?
```

## API Reference

::: {.automodule members=""}
canvas_core.templating
:::
