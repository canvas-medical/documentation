---
title: "Custom Command"
slug: "commands-custom-command"
excerpt: "Canvas SDK Custom Command"
hidden: false
---

## Introduction

The `CustomCommand` class allows plugins to create custom commands with HTML-rendered content that can be inserted into patient charts. Custom commands are designed for displaying read-only content and do not support user input or interactive forms.

**Important**: Custom commands must be configured in the plugin's [`CANVAS_MANIFEST.json`](/sdk/canvas_manifest/#commands) file under the `commands` array before they can be used.

## Parameters

| Name            | Type     | Required | Description                                                                                    |
|:----------------|:---------|:---------|:-----------------------------------------------------------------------------------------------|
| `note_uuid`     | _string_ | `true`   | The externally exposable id of the note in which to insert the command.                        |
| `command_uuid`  | _string_ | `true`   | The externally exposable id of the command which is being referenced.                          |
| `schema_key`    | _string_ | `true`   | Identifier for data binding. Must match the `schema_key` in your manifest configuration and must be unique across every plugin installed on the instance. |
| `content`       | _string_ | `true`   | HTML content for display in the chart.                                                         |
| `print_content` | _string_ | `false`  | HTML content for print version (recommended for optimal print output).                         |

## Manifest Configuration

Custom commands must be declared in your `CANVAS_MANIFEST.json`:

```json
{
  "components": {
    "commands": [
      {
        "name": "RiskAssessment",
        "label": "Risk Assessment",
        "schema_key": "riskAssessment",
        "section": "assessment"
      }
    ]
  }
}
```

### Manifest Fields

- **name**: Unique name for the command
- **label**: User-friendly label displayed in Canvas UI
- **schema_key**: Identifier for the command. Must be unique across every plugin installed on the Canvas instance — if another installed plugin already declares the same `schema_key`, installation will be rejected. CustomCommand instances must use this value.
- **section**: Chart section where command appears: `subjective`, `objective`, `assessment`, `plan`, `procedures`, `history`, or `internal`

**Note**: `schema_key` values must be unique across **all plugins installed on the instance**, not just within a single plugin. If you install a plugin whose manifest declares a `schema_key` already owned by another installed plugin, the installation fails with a clear validation error instead of silently overwriting the existing command. Choose a distinctive `schema_key` — for example, prefixing it with your plugin's name — to avoid collisions.

## Basic Usage

### Step 1: Create HTML Templates

Create a template file for your command content (e.g., `templates/risk_assessment.html`):

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .risk-assessment {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 16px;
        }
        .risk-header {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
        }
        .risk-item {
            padding: 8px;
            margin-bottom: 8px;
            background: #f7fafc;
            border-radius: 4px;
        }
        .risk-level {
            font-weight: 600;
            color: #c53030;
        }
    </style>
</head>
<body>
    <div class="risk-assessment">
        <div class="risk-header">Risk Assessment</div>
        <div class="risk-item">
            <span class="risk-level">Cardiovascular Risk: High</span>
            <p>Hypertension, family history of heart disease</p>
        </div>
        <div class="risk-item">
            <span class="risk-level">Falls Risk: Moderate</span>
            <p>Age over 65, history of dizziness</p>
        </div>
    </div>
</body>
</html>
```

Create a simpler print version (e.g., `templates/risk_assessment_print.html`):

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .risk-assessment-print {
            font-family: Arial, sans-serif;
            font-size: 11px;

            .section {
                margin-bottom: 8px;
            }

            .label {
                font-weight: bold;
            }
        }
    </style>
</head>
<body class="risk-assessment-print">
    <h3>Risk Assessment</h3>
    <div class="section">
        <span class="label">Cardiovascular Risk:</span> High - Hypertension, family history
    </div>
    <div class="section">
        <span class="label">Falls Risk:</span> Moderate - Age over 65, history of dizziness
    </div>
</body>
</html>
```

### Step 2: Use Templates in Your Command

```python
from canvas_sdk.commands.commands.custom_command import CustomCommand
from canvas_sdk.templates import render_to_string
import uuid

command = CustomCommand(
    schema_key="riskAssessment",
    content=render_to_string("templates/risk_assessment.html"),
    print_content=render_to_string("templates/risk_assessment_print.html")
)
command.command_uuid = str(uuid.uuid4())
command.note_uuid = "rk786p"

effect = command.originate()
```

### Extended CustomCommand Class (For Reusability)

Create a subclass with a predefined `schema_key`:

```python
from canvas_sdk.commands.commands.custom_command import CustomCommand
from canvas_sdk.templates import render_to_string
import uuid

class RiskAssessmentCommand(CustomCommand):
    """Custom command for risk assessment."""

    class Meta:
        schema_key = "riskAssessment"

# Usage
command = RiskAssessmentCommand(
    content=render_to_string("templates/risk_assessment.html"),
    print_content=render_to_string("templates/risk_assessment_print.html")
)
command.command_uuid = str(uuid.uuid4())
command.note_uuid = "rk786p"

effect = command.originate()
```

## Methods

### originate()

Returns an Effect that originates a new command in the note body.

**Example:**
```python
from canvas_sdk.commands.commands.custom_command import CustomCommand
from canvas_sdk.templates import render_to_string
import uuid

command = CustomCommand(
    schema_key="riskAssessment",
    content=render_to_string("templates/risk_assessment.html"),
    print_content=render_to_string("templates/risk_assessment_print.html")
)
command.command_uuid = str(uuid.uuid4())
command.note_uuid = "rk786p"

effect = command.originate()
```

## Content vs Print Content

Custom commands support two versions of content:

### Display Content (content)
- Rendered in the Canvas UI when viewing the chart
- Can include rich styling and complex layouts

### Print Content (print_content)
- Rendered when printing the chart or generating PDFs
- Should be simpler and more compact
- Sanitized before it is added to the print page, as described in [Print content sanitization](#print-content-sanitization)

If you don't provide `print_content`, print pages use `content` instead, with the same sanitization.

**Best Practice**: Always provide both versions for the best user experience.

## Print content sanitization

The chart displays `content` in a sandboxed frame, but print pages inline the HTML into the page itself. Canvas sanitizes that HTML first, so script in a plugin's output can't run on the print page. Before sanitizing, Canvas prefixes your class names and IDs with the command's key and updates the selectors in your `<style>` blocks to match. It also removes the `<html>` wrapper and turns the `<body>` tag into a `<div>` with the same attributes. A full HTML document like the print template example keeps its top-level class.

Print pages keep:

- `<style>` blocks. The sanitizer doesn't change the CSS inside them.
- `class`, `id`, and `style` attributes.
- Common formatting and structure tags, such as headings, paragraphs, `<div>`, `<span>`, lists, tables, links, and images.

Print pages remove:

- `<script>` and `<svg>` elements, including their contents.
- Event handler attributes, such as `onclick` and `onerror`.
- Other tags outside the allowed set, such as `<head>`, `<section>`, `<tfoot>`, `<iframe>`, form elements, and buttons. Their text and child elements stay on the page, including `<style>` blocks inside `<head>`, but the tag's own attributes, including its `class`, are lost.
- Inline `style` properties other than these formatting properties: `background-color`, `border`, `border-collapse`, `border-color`, `border-style`, `border-width`, `color`, `float`, `font-family`, `font-size`, `font-style`, `font-weight`, `height`, `line-height`, `margin`, `margin-left`, `margin-right`, `max-height`, `max-width`, `padding`, `padding-left`, `text-align`, `text-decoration`, `vertical-align`, and `width`. For example, an inline `display: flex` or `margin-top` is removed. Put rules like these in a `<style>` block instead.
- Link and image URLs with a scheme other than `http`, `https`, `mailto`, or `tel`, such as `javascript:`. Images can also use `data:` URLs. The link text stays on the page.

## Limitations

- Custom commands are read-only and cannot capture user input
- Interactive elements (forms, buttons, input fields) are not supported
- Commands must be configured in the manifest before use
- The `schema_key` must be unique across every plugin installed on the Canvas instance. Installing a plugin whose `schema_key` is already owned by another installed plugin will fail with a validation error.


<br/>
<br/>
<br/>
