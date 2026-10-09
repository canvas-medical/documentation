---
title: "Canvas Manifest"
excerpt: "Reference for every field in a plugin's CANVAS_MANIFEST.json"
hidden: false
---

Every plugin has a `CANVAS_MANIFEST.json` file at the root of its package. The manifest names the plugin, lists the handlers and applications Canvas loads, and declares the variables, URL permissions, and custom data namespace the plugin needs.

The manifest is validated against a JSON schema when you run [`canvas validate`](/sdk/canvas_cli/#canvas-validate), or [`canvas validate-manifest`](/sdk/canvas_cli/#canvas-validate-manifest), and Canvas Platform checks it again on every [`canvas deploy`](/sdk/canvas_cli/#canvas-deploy) push. Unknown top-level keys and unknown component types fail validation.

## Where the manifest lives

[`canvas init`](/sdk/canvas_cli/#canvas-init) creates a project with the plugin package inside it. The manifest sits at the top of the package directory, next to the plugin's code, and every path in the manifest (handler classes, icons, templates, the README) is relative to that directory.

```text
my_plugin/                       # project directory
├── pyproject.toml
├── tests/
│   └── test_event_handlers.py
└── my_plugin/                   # plugin package
    ├── CANVAS_MANIFEST.json
    ├── README.md
    ├── __init__.py
    ├── assets/
    │   └── icon.png
    ├── handlers/
    │   ├── __init__.py
    │   └── event_handlers.py
    └── templates/
        └── intake_form.yml
```

A handler in `my_plugin/handlers/event_handlers.py` is referenced as `my_plugin.handlers.event_handlers:ClassName`, and the icon as `assets/icon.png`. Pass the package directory, the one that holds `CANVAS_MANIFEST.json`, to `canvas validate` and `canvas deploy`: `canvas validate my_plugin/my_plugin` from outside the project, or `canvas validate my_plugin` from inside it.

Canvas runs only the handlers and applications the manifest lists. A handler class in the package that the manifest doesn't reference is never loaded, and `canvas validate` warns about each one it finds. Every other file in the package directory still ships with the plugin, so your handlers can import your own modules and read templates and assets without listing them in the manifest. `canvas deploy` ships the files committed to the plugin's git repository, so `.gitignore` decides what is left out. See [Plugin repository layout](/sdk/canvas_cli/#canvas-deploy).

## Basic structure

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "my_plugin",
  "description": "A description of what this plugin does",
  "components": {
    "handlers": [],
    "applications": [],
    "commands": [],
    "questionnaires": []
  },
  "variables": [],
  "tags": {},
  "references": [],
  "license": "",
  "diagram": false,
  "readme": "./README.md"
}
```

## Top-level fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sdk_version` | string | Yes | The Canvas SDK version the plugin was built against. |
| `plugin_version` | string | Yes | The plugin's version. Must not be empty. Increase it on every deploy. See [Versioning your plugin](#versioning-your-plugin). |
| `name` | string | Yes | The plugin's name, which is also its package folder name. For a plugin deployed through Canvas Platform it is publisher-prefixed, `<org prefix>__<package>` (for example `acme__intake`): lowercase letters, digits and underscores, starting with a letter on both sides of the double underscore. `canvas login` lists your organizations' prefixes. |
| `description` | string | Yes | What the plugin does. |
| `components` | object | Yes | The handlers, applications, commands, and questionnaires the plugin provides. Must contain at least one component type. See [Components](#components). |
| `tags` | object | Yes | Categorization tags. Can be empty (`{}`). See [Tags](#tags). |
| `license` | string | Yes | A license identifier such as `"MIT"`, or an empty string. |
| `readme` | string or boolean | Yes | Path to the plugin's README, or `false`. |
| `variables` | array | No | Configuration values and secrets the plugin reads at runtime. See [Variables](#variables). |
| `secrets` | array | No | Deprecated. Use `variables` instead. |
| `url_permissions` | array | No | External URLs the plugin's iframes may load, and what each may do. See [URL permissions](#url-permissions). |
| `origins` | object | No | Legacy form of `url_permissions`. |
| `custom_data` | object | No | The custom data namespace the plugin uses. See [Custom data](#custom-data). |
| `catalog` | object | No | The plugin's listing in the Canvas Platform plugin catalog. See [Catalog](#catalog). |
| `references` | array of strings | No | Links to related documentation or resources. |
| `diagram` | string or boolean | No | Path to an architecture or workflow diagram, or `false`. |

### Versioning your plugin

Change `plugin_version` every time you deploy a new build, including builds sent only to a test instance. Canvas accepts a redeploy with an unchanged version, so the version is the only way to tell which build an instance is running. It appears in:

- the Plugins list in the Canvas Admin
- `canvas list`, as `name@version`
- the log lines written when the plugin is installed and loaded, for example `Successfully loaded plugin "my_plugin", version 1.4.0`

Use [semantic versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`):

| Change | Bump | Example |
|--------|------|---------|
| A fix that doesn't change behavior users rely on | `PATCH` | `1.4.0` → `1.4.1` |
| New functionality that leaves existing behavior in place | `MINOR` | `1.4.1` → `1.5.0` |
| A change that breaks existing behavior, such as a renamed variable, a removed handler, or a changed custom data model | `MAJOR` | `1.5.0` → `2.0.0` |

#### Versioning with git

`canvas deploy` deploys a commit pushed to the plugin's git repository on Canvas Platform, so every build on an instance maps to a commit. Tie each version to that history:

- **Bump the version in the commit or pull request that changes the code.** Each merged change then carries its own version, and a reviewer can see what the new number ships.
- **Tag the commit you release** (for example `git tag v1.5.0`, then `git push origin v1.5.0`). A version seen in the logs or the Admin then leads straight to the source that produced it, `git diff v1.4.1 v1.5.0` shows what changed between two releases, and `canvas deploy <package dir> --ref v1.5.0 --instance <instance>` deploys exactly that tag.

To tell test builds apart without spending release numbers, add a pre-release suffix such as `1.5.0-rc.1` or `1.5.0-dev.3`, and drop the suffix for the build you release.

## Components

The `components` object groups everything Canvas loads from your plugin. Each key holds a list, and the object must contain at least one key.

| Key | Holds |
|-----|-------|
| [`handlers`](#handlers) | Classes that respond to Canvas events and serve plugin APIs. |
| [`applications`](#applications) | Applications that appear in the Canvas UI. |
| [`commands`](#commands) | Custom commands the plugin adds to notes. |
| [`questionnaires`](#questionnaires) | Questionnaire templates Canvas creates on install. |

### Handlers

Handlers respond to Canvas events: [event handlers](/sdk/handlers-basehandler/), [SimpleAPI](/sdk/handlers-simple-api/) endpoints, [CronTasks](/sdk/handlers-crontask/), [action buttons](/sdk/handlers-action-buttons/), [embedded applications](/sdk/handlers-embedded-applications/), and the rest of the [handler types](/sdk/handlers/).

`protocols` is deprecated in favor of `handlers`. Canvas still loads classes listed under `protocols`, so existing plugins keep working, but new plugins should use `handlers`. To migrate, rename the key. The entries inside it stay the same.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `class` | string | Yes | Import path to the handler class, in `package.module:ClassName` form. |
| `description` | string | Yes | What the handler does. |
| `meta` | object | No | Handler metadata. Used by clinical quality measure protocols. |
| `data_access` | object | No | Accepted by the schema with `event`, `read`, and `write` keys, but not enforced. A handler's data access is not limited by this field. |

```json
{
  "components": {
    "handlers": [
      {
        "class": "my_plugin.handlers.patient_sync:PatientSync",
        "description": "Sends patient updates to an external system"
      }
    ]
  }
}
```

### Applications

Applications add entry points to the Canvas UI. See [Applications](/sdk/handlers-applications/) for where each one appears and the handler that runs when a user opens it.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `class` | string | Yes | Import path to the `Application` subclass, in `package.module:ClassName` form. |
| `name` | string | Yes | Display name. Up to 32 characters. |
| `description` | string | Yes | What the application does. Up to 256 characters. |
| `icon` | string | Yes | Path to an image inside the plugin package, or an `https://` URL to one. Rendered at 48 × 48 px. |
| `scope` | string | Yes | Where the application appears. See [Application Scopes](/sdk/handlers-applications/#application-scopes) for the values. |
| `menu_position` | string | No | `"top"` or `"bottom"`. Defaults to `"top"`. |
| `menu_order` | integer | No | Order of the application within its menu position. Lower numbers appear first. |
| `show_in_panel` | boolean | No | Shows the application alongside the panel buttons instead of in the app drawer. Defaults to `false`. |
| `panel_priority` | integer | No | Order of the application among panel applications. |

```json
{
  "components": {
    "applications": [
      {
        "class": "my_plugin.applications.risk_calculator:RiskCalculator",
        "name": "Risk Calculator",
        "description": "Calculates cardiovascular risk for the open patient",
        "icon": "assets/risk_calculator.png",
        "scope": "patient_specific",
        "show_in_panel": true,
        "panel_priority": 100
      }
    ]
  }
}
```

Embedded applications (note applications, scheduling applications, and docked applications) are declared under `handlers`, not `applications`, and take no `scope` or `icon`. See [Embedded Applications](/sdk/handlers-embedded-applications/).

### Commands

The `commands` list declares [custom commands](/sdk/commands-custom-command/): commands with plugin-rendered HTML content that can be added to a note.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for the command. |
| `schema_key` | string | Yes | Identifier the `CustomCommand` effect uses to refer to this command. Must be unique across every plugin installed on the instance, or installation fails. |
| `label` | string | No | Label shown in the Canvas UI. |
| `section` | string | No | Note section the command belongs to: `subjective`, `objective`, `assessment`, `plan`, `procedures`, `history`, or `internal`. |

```json
{
  "components": {
    "commands": [
      {
        "name": "RiskAssessment",
        "label": "Risk Assessment",
        "schema_key": "myPluginRiskAssessment",
        "section": "assessment"
      }
    ]
  }
}
```

### Questionnaires

The `questionnaires` list points at YAML templates in the plugin package. Canvas creates each questionnaire when the plugin is installed. See [Questionnaires](/sdk/effect-questionnaires/#manifest-yaml-template) for the template format.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `template` | string | Yes | Path to the questionnaire's YAML template inside the plugin package. |

```json
{
  "components": {
    "questionnaires": [
      {
        "template": "templates/intake_form.yml"
      }
    ]
  }
}
```

### Content, effects, and views

`content`, `effects`, and `views` are accepted for compatibility and have no effect. `canvas init` adds them as empty lists, and you can remove them.

## Variables

`variables` declares the configuration values and secrets a plugin reads from `self.secrets` at runtime. Values are set per instance with [`canvas config set`](/sdk/canvas_cli/#canvas-config-set). See [Managing Variables](/sdk/secrets/).

`namespace_read_access_key` and `namespace_read_write_access_key` are reserved for a plugin deployed through Canvas Platform: Canvas Platform supplies them to plugins entitled to a [custom data](#custom-data) namespace, and refuses a manifest that declares them.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | The key the value is read under in `self.secrets`. |
| `sensitive` | boolean | No | When `true`, the value is hidden in the Admin UI and CLI listings. Defaults to `false`. |
| `default` | string | No | Accepted by the schema for non-sensitive variables only. Canvas does not pre-fill the variable with it, so set the value with `canvas config set`. |

```json
{
  "variables": [
    {"name": "API_TOKEN", "sensitive": true},
    {"name": "API_BASE_URL"}
  ]
}
```

The older `secrets` field is a list of names, each treated as a non-sensitive variable. `canvas validate-manifest` prints a deprecation warning when a manifest uses it.

```json
{
  "secrets": ["API_TOKEN"]
}
```

## URL permissions

A [`LaunchModalEffect` or `PortalWidget`](/sdk/layout-effect/#additional-configuration) only loads URLs and external scripts listed in `url_permissions`. Each entry names a URL and the iframe capabilities it is granted.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | The URL to allow, in [CSP host-source](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy#host-source) format. |
| `permissions` | array of strings | Yes | Capabilities granted to the URL. Can be empty. |

| Permission | Grants |
|------------|--------|
| `SCRIPTS` | JavaScript execution |
| `ALLOW_SAME_ORIGIN` | Same-origin access |
| `MICROPHONE` | Microphone access |
| `CAMERA` | Camera access |
| `CLIPBOARD_READ` | Reading from the clipboard |
| `CLIPBOARD_WRITE` | Writing to the clipboard |

```json
{
  "url_permissions": [
    {
      "url": "https://example.com",
      "permissions": ["SCRIPTS", "ALLOW_SAME_ORIGIN", "MICROPHONE"]
    }
  ]
}
```

See [Additional Configuration](/sdk/layout-effect/#additional-configuration) on the layout effects page for when each permission is needed.

### Origins (legacy)

`origins` is the older form of `url_permissions`. A manifest can use one or the other, not both. Canvas converts each `urls` entry to a URL with no permissions and each `scripts` entry to a URL with `SCRIPTS`.

```json
{
  "origins": {
    "urls": ["https://example.com"],
    "scripts": ["https://cdn.example.com"]
  }
}
```

## Custom data

`custom_data` declares the namespace a plugin stores [custom data](/sdk/custom-data/) in, and whether it can write to it. See the [Custom Data Quick Start](/sdk/custom-data-quick-start/).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `namespace` | string | Yes | Namespace name in `org__name` form: lowercase letters, digits, and underscores, with a double underscore between the two parts. Up to 63 characters. |
| `access` | string | Yes | `"read"` for read-only access, or `"read_write"`. |

```json
{
  "custom_data": {
    "namespace": "my_org__my_plugin",
    "access": "read_write"
  }
}
```

## Catalog

`catalog` is the plugin's listing in the Canvas Platform plugin catalog. Canvas Platform reads it from the manifest of each pushed revision, so the listing ships with the code it describes, and it refuses a push whose listing breaks the rules below. [`canvas deploy --push-only`](/sdk/canvas_cli/#canvas-deploy) updates the listing without deploying to an instance, and `canvas validate` checks it locally.

```json
{
  "catalog": {
    "title": "Intake Summary",
    "kind": "plugin",
    "category": "Charting",
    "surfaces": ["Note"],
    "keywords": ["intake", "summary"],
    "screenshots": [
      {"path": "assets/summary.png", "caption": "In the note", "alt": "An intake summary in a note"}
    ],
    "icon": "assets/icon.png",
    "setup_guide": "setup_guide.md",
    "setup_instructions": "setup_instructions.md",
    "release_notes": {"kind": "fix", "title": "Summaries keep their line breaks"}
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | The name on the plugin's card and page. At most 64 characters. |
| `category` | string | Yes | One of `Billing & RCM`, `Charting`, `Decision support`, `Interoperability`, `Labs & devices`, `Operations`, `Patient engagement`, `Population health`, `Prescribing`, `Scheduling`. |
| `surfaces` | array | Yes | Every place in Canvas the plugin's work shows up, at least one and none repeated: `Note`, `Chart app`, `Command`, `Background`, `Patient portal`, `Waffle`. |
| `kind` | string | No | `agent` for a plugin that calls a model and acts with latitude, or `plugin` for a deterministic one. Defaults to `plugin`. |
| `agent` | object | When `kind` is `agent` | The agent's boundary: `does`, `does_not`, `runs_when` (text) and `models` (at least one model name). A `plugin` must leave it out. |
| `keywords` | array | No | Free search terms, separate from [Tags](#tags): lowercase letters, digits and hyphens, up to 32 characters each. |
| `screenshots` | array | No | Up to eight images, in display order. Each has a `path` ending in `.png`, `.jpg`, `.jpeg` or `.webp` in lowercase, a required `alt` of at most 200 characters, and an optional `caption` of at most 40. |
| `integration` | object | No | For an integration: `unit` names what its volume counts, such as `"visits"`. |
| `icon` | string | No | Path to the image shown beside the title on the plugin's card, in place of the category's icon. Ends in `.png`, `.jpg`, `.jpeg` or `.webp` in lowercase. |
| `setup_guide` | string | No | Path to a Markdown file for the person deciding whether to install the plugin: what to have ready, the steps, and how long setup takes. The catalog shows it as **How setup works**, beside **Pricing**. |
| `setup_instructions` | string | No | Path to a file that Studio's agent reads when an organization installs the plugin. For the setup description shown in the catalog, use `setup_guide`. |
| `release_notes` | object | No | What changed in this `plugin_version`: `kind` (`fix`, `performance` or `breaking`), `title`, and an optional `body`. Canvas Platform assembles the history from every pushed revision. |

Every path is inside the package folder: no leading `/`, no `..` anywhere in it, and no backslash. Unknown fields are refused at every level, and optional fields are left out rather than set to `null`.

## Tags

Tags categorize a plugin. Unrecognized tag categories and values produce warnings during validation rather than errors.

| Category | Allowed values |
|----------|----------------|
| `patient_sourcing_and_intake` | `symptom_triage`, `coverage_capture` |
| `interaction_modes_and_utilization` | `supply_policies`, `demand_policies`, `auto_followup` |
| `content` | `patient_intake` |
| `diagnostic_range_and_inputs` | None yet. Use an empty list. |
| `pricing_and_payments` | None yet. Use an empty list. |
| `care_team_composition` | None yet. Use an empty list. |
| `interventions_and_safety` | None yet. Use an empty list. |

```json
{
  "tags": {
    "patient_sourcing_and_intake": ["symptom_triage"]
  }
}
```

## Complete example

A plugin with a patient chart application, the SimpleAPI handler that serves it, a custom command, and a sensitive variable:

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "1.0.0",
  "name": "risk_calculator",
  "description": "Calculates clinical risk scores for patients",
  "url_permissions": [
    {
      "url": "https://risk.example.com",
      "permissions": ["SCRIPTS", "ALLOW_SAME_ORIGIN"]
    }
  ],
  "components": {
    "applications": [
      {
        "class": "risk_calculator.applications.calculator:RiskCalculatorApp",
        "name": "Risk Calculator",
        "description": "Calculates cardiovascular risk for the open patient",
        "icon": "assets/risk_calculator.png",
        "scope": "patient_specific",
        "show_in_panel": true,
        "panel_priority": 100
      }
    ],
    "handlers": [
      {
        "class": "risk_calculator.handlers.api:RiskCalculatorAPI",
        "description": "Serves the calculator page and its data"
      }
    ],
    "commands": [
      {
        "name": "RiskAssessment",
        "label": "Risk Assessment",
        "schema_key": "riskCalculatorAssessment",
        "section": "assessment"
      }
    ]
  },
  "variables": [
    {"name": "RISK_API_TOKEN", "sensitive": true}
  ],
  "tags": {},
  "references": [],
  "license": "MIT",
  "diagram": false,
  "readme": "./README.md"
}
```

## Validation

Validate a manifest with the [Canvas CLI](/sdk/canvas_cli/):

```bash
canvas validate my_plugin
```

`canvas validate` checks the manifest against the schema and then loads every handler in the plugin sandbox, which catches disallowed imports and other errors that only appear on the instance. `canvas validate-manifest my_plugin` runs the manifest checks alone.
