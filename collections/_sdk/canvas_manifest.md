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
└── acme__my_plugin/             # plugin package
    ├── CANVAS_MANIFEST.json
    ├── OVERVIEW.md
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

A handler in `acme__my_plugin/handlers/event_handlers.py` is referenced as `acme__my_plugin.handlers.event_handlers:ClassName`, and the icon as `assets/icon.png`. Pass the package directory, the one that holds `CANVAS_MANIFEST.json`, to `canvas validate` and `canvas deploy`: `canvas validate my_plugin/acme__my_plugin` from outside the project, or `canvas validate acme__my_plugin` from inside it.

Canvas runs only the handlers and applications the manifest lists. A handler class in the package that the manifest doesn't reference is never loaded, and `canvas validate` warns about each one it finds. Every other file in the package directory still ships with the plugin, so your handlers can import your own modules and read templates and assets without listing them in the manifest. `canvas deploy` ships the files committed to the plugin's git repository, so `.gitignore` decides what is left out. See [Plugin repository layout](/sdk/canvas_cli/#canvas-deploy).

## Basic structure

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "acme__my_plugin",
  "publisher": "acme",
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
| `name` | string | Yes | The plugin's name, which is also its package folder name: lowercase letters, digits and underscores, starting with a letter, at most 255 characters. A plugin that already runs under a name outside that rule keeps it; see [Signing in to Canvas Platform](/sdk/canvas_cli/#signing-in-to-canvas-platform). We recommend your organization's prefix, `<org prefix>__<package>` (for example `acme__intake`); `canvas login` lists your organizations' prefixes. |
| `publisher` | string | No | Slug of the Canvas Platform organization that publishes the plugin, such as `acme`. `canvas login` lists each organization's slug in parentheses. `canvas init` sets it, and `canvas deploy` writes it when you pick a publisher at a terminal. To leave the publisher unset, leave the field out: `canvas deploy` refuses `"publisher": null`, like any other value that isn't a string. See Choosing the publisher under [`canvas deploy`](/sdk/canvas_cli/#canvas-deploy). |
| `description` | string | Yes | What the plugin does, in one sentence. The Canvas Platform catalog shows it under the plugin's title and on its card. |
| `components` | object | Yes, except in a bundle | The handlers, applications, commands, and questionnaires the plugin provides. Must contain at least one component type. See [Components](#components). |
| `tags` | object | Yes | Categorization tags. Can be empty (`{}`). See [Tags](#tags). |
| `license` | string | Yes | A license identifier such as `"MIT"`, or an empty string. |
| `readme` | string or boolean | Yes | Path to the plugin's README, or `false`. |
| `variables` | array | No | Configuration values and secrets the plugin reads at runtime. See [Variables](#variables). |
| `secrets` | array | No | Deprecated. Use `variables` instead. |
| `url_permissions` | array | No | External URLs the plugin's iframes may load, and what each may do. See [URL permissions](#url-permissions). |
| `origins` | object | No | Legacy form of `url_permissions`. |
| `custom_data` | object | No | The custom data namespace the plugin uses. See [Custom data](#custom-data). |
| `catalog` | object | No | The plugin's listing in the Canvas Platform plugin catalog. See [Catalog](#catalog). |
| `dependencies` | array | No, except in a bundle | Other plugins Canvas Platform installs with this one, each pinned to an exact version or a compatible release. See [Dependencies and bundles](#dependencies-and-bundles). |
| `bundle` | boolean | No | `true` for a plugin made only of its `dependencies` and its catalog listing. Defaults to `false`. See [Dependencies and bundles](#dependencies-and-bundles). |
| `references` | array of strings | No | Links to related documentation or resources. |
| `diagram` | string or boolean | No | Path to an architecture or workflow diagram, or `false`. |

### Versioning your plugin

Change `plugin_version` every time you deploy a new build, including builds sent only to a test instance. Canvas accepts a redeploy with an unchanged version, so the version is the only way to tell which build an instance is running. It appears in:

- the Plugins list in the Canvas Admin
- `canvas list`, as `name@version`
- the log lines written when the plugin is installed and loaded, for example `Successfully loaded plugin "acme__my_plugin", version 1.4.0`

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

A pre-release suffix such as `1.5.0-rc.1` or `1.5.0-dev.3` tells test builds apart without spending release numbers. For a plugin listed in the Canvas Platform catalog, the suffix on `main` also sets the listing's stage (see [Release stages](#release-stages)): a `-rc.1` or `-dev.3` build pushed to `main` lists the plugin as Beta, and other organizations cannot install it. Push test builds of a listed plugin to another branch with `canvas deploy --branch`, and keep `main` at the version other organizations install.

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
        "class": "acme__my_plugin.handlers.patient_sync:PatientSync",
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
        "class": "acme__my_plugin.applications.risk_calculator:RiskCalculator",
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

Embedded applications (note applications, scheduling applications, docked applications, and portal docked applications) are declared under `handlers`, not `applications`, and take no `scope` or `icon`. See [Embedded Applications](/sdk/handlers-embedded-applications/).

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

`catalog` is the plugin's listing in the Canvas Platform plugin catalog. Canvas Platform reads it from the manifest each time a push moves the plugin's `main` branch, so the listing ships with the code it describes; pushes to other branches and tags leave the catalog as it is. It refuses a push whose listing breaks the rules below. [`canvas deploy --push-only`](/sdk/canvas_cli/#canvas-deploy) updates the listing without deploying to an instance, and `canvas validate` checks it locally.

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
    "video": {
      "url": "https://www.youtube.com/watch?v=<video-id>",
      "poster": "assets/video-poster.png",
      "caption": "Summarizing an intake"
    },
    "pricing": [
      {"unit": "visit", "price_per_unit": "1.50"},
      {"unit": "token", "markup_bps": 1500}
    ],
    "vendors": [
      {"name": "Twilio", "relationship": "self_managed", "additional_fees": true}
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
| `video` | object | No | A YouTube video that the plugin's page plays first in its screenshot row. It has a `url` (a YouTube watch, `youtu.be` or embed link over `https`, naming the video's 11-character id), a `poster` image shown until the video plays (with the same rules as a screenshot `path`), and an optional `caption` of at most 40 characters. The video must allow embedding, which is YouTube's default for an unlisted upload. |
| `pricing` | array | No | What the plugin's publisher charges, up to 10 components in the order the plugin's page lists them. Each has a `unit` in the singular (at most 40 characters, named once) and a `price_per_unit`: a string of US dollars such as `"5.75"`, with at most four decimal places. The `token` unit takes no price, because the inference gateway prices tokens by model. It can take an optional `markup_bps` instead: how far above the gateway's list price the plugin's tokens bill, as a whole number of basis points from `0` to `10000`, so `1500` is 15%. For a plugin Canvas publishes that declares the sensitive variable `INFERENCE_GATEWAY_KEY`, Canvas Platform issues the installing organization an inference gateway key in that variable and bills its tokens at this markup. No other unit takes a `markup_bps`. For every other unit, the plugin counts the work it charges for by returning a [`RecordUsage`](/sdk/effect-record-usage/) effect. Leave `pricing` out for a plugin with no charge. |
| `vendors` | array | No | The third parties the plugin depends on, up to 10. Each has a `name` (at most 64 characters, named once), a `relationship` of `canvas_managed` (Canvas sets up the account) or `self_managed` (the customer does), and `additional_fees`: `true` when the vendor bills the customer directly for its own fees, separately from Canvas. |
| `icon` | string | No | Path to the image shown beside the title on the plugin's card, ending in `.png`, `.jpg`, `.jpeg` or `.webp` in lowercase. |
| `setup_guide` | string | No | Path to a markdown file describing setup for the person deciding whether to install the plugin: what to have ready, the steps, how long it takes. The plugin's page shows it under How setup works. |
| `setup_instructions` | string | No | Path to a file that Studio's agent reads when an organization installs the plugin. It is not shown on the plugin's page. |
| `release_notes` | object | No | What changed in this `plugin_version`: `kind` (`fix`, `performance` or `breaking`), `title`, and an optional `body`. Canvas Platform assembles the history from every pushed revision. |

Every path is inside the package folder: no leading `/`, no `..` anywhere in it, and no backslash. Unknown fields are refused at every level, and optional fields are left out rather than set to `null`.

Someone holding the Publisher role in the plugin's organization can also edit the listing from the plugin's page in the Canvas Platform catalog, including the `description`. Saving there is a commit to `main` with the listing changed and `plugin_version` bumped within its stage, so pull before your next push. A release takes a patch bump (`1.4.2` to `1.4.3`). A pre-release keeps its suffix and bumps its last number (`1.0.0-beta.2` to `1.0.0-beta.3`), or gains `.1` when it ends in a word (`1.0.0-alpha` to `1.0.0-alpha.1`). Any other version, such as `1.0.0a1` or one with build metadata (`+build.5`), cannot take a bump, and the edit is refused.

### Release stages

The suffix on the highest `plugin_version` that `main` has carried sets the listing's stage in the Canvas Platform catalog:

| `plugin_version` | Stage | Examples |
|------------------|-------|----------|
| No pre-release suffix | Generally available | `1.0.0` |
| A suffix whose first identifier is `alpha` | Coming soon | `1.0.0-alpha`, `1.0.0-alpha.2`, `1.0.0a1` |
| Any other suffix | Beta | `1.0.0-beta.1`, `1.0.0-rc.1`, `1.0.0b2`, `1.0.0.dev3` |

While a plugin is Coming soon or Beta:

- Other organizations see the plugin's card and page with a Coming soon or Beta label. The page offers **Join the waiting list**, with an optional note, in place of installing it.
- Every install outside the plugin's organization is refused, and `canvas deploy` names the plugin's catalog page in its refusal. The plugin's own organization installs it as usual, for testing, and so does each practice it manages when that organization is an MSO.
- The plugin's organization sees each waiting-list request on its own view of the plugin's page, with the requester's note and whether they would test a beta.

To make the plugin generally available, push its release with no suffix, such as `1.0.0` after `1.0.0-rc.1`. A lower release, such as `0.9.1` pushed after `1.0.0-rc.1`, leaves the stage as it is. A listing that shows a released version to other organizations keeps that release when a pre-release is pushed after it, while any instance outside the plugin's organization has the plugin installed, so customers keep installing the release they run.

An `OVERVIEW.md` file beside `CANVAS_MANIFEST.json` in the package folder is the plugin's overview, and needs no field in `catalog`. When it is there, the plugin's page shows it as rendered markdown beside the plugin's pricing and setup. `canvas init` creates one to start from.

## Dependencies and bundles

A plugin that needs other plugins on the same instance names them in `dependencies`. When you deploy it with [`canvas deploy`](/sdk/canvas_cli/#canvas-deploy), Canvas Platform installs each dependency before the plugins that need it, at the highest version on the dependency's `main` that every pin on it accepts. A compatible release pin leaves out prereleases.

A dependency doesn't make its code importable: a plugin can still import only its own package. Declare a dependency when your plugin relies on what another plugin provides on the instance, such as the APIs one of its applications serves, so that plugin is installed and enabled wherever yours is.

```json
{
  "dependencies": [
    {"name": "acme__intake_form", "publisher": "acme", "version": "1.16.0"},
    {"name": "acme__intake_summary", "publisher": "acme", "version": "~=1.14"}
  ]
}
```

Each entry has exactly these three fields, all required:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The dependency's manifest [`name`](#top-level-fields), such as `acme__intake_form`. |
| `publisher` | string | The slug of the Canvas Platform organization that publishes the dependency, as [`canvas login`](/sdk/canvas_cli/#signing-in-to-canvas-platform) lists it, such as `acme` for `Acme Health (acme)`. |
| `version` | string | The versions of the dependency this plugin works with: one exact version or a compatible release. See [Version pins](#version-pins). |

A plugin can't depend on itself or list the same dependency twice, and a dependency can't be a [bundle](#bundles).

Each dependency must already be on Canvas Platform at a version its pin accepts. Its publisher puts each release there, without deploying it to an instance, with [`canvas deploy --push-only`](/sdk/canvas_cli/#canvas-deploy), adding `--snapshot` for a plugin inside a larger repository such as a monorepo.

### Version pins

A dependency's `version` takes one of two forms:

- **An exact version**, such as `"1.16.0"`, installs that version. Write it in its normal form: `"v1.16.0"` fails validation, and the error gives the form to write instead.
- **A compatible release**, `~=` followed by a version with at least two parts, accepts any version in its range. `"~=1.16"` accepts 1.16 or later, below 2.0. `"~=0.1.1"` accepts 0.1.1 or later, below 0.2.

Other forms, such as `">=1.16"`, `"==1.16.0"`, `"1.*"`, `"~=1"`, or a comma-separated range, fail validation.

Version your plugins with [semantic versioning](#versioning-your-plugin) so these pins work: a compatible release stays within one major version, so a new major version reaches only plugins whose pin names it.

When several plugins pin the same dependency, they move to its new major version together. Release a version of each that pins the new major version, then deploy those releases in one deployment with [`canvas deploy --plugin`](/sdk/canvas_cli/#deploying-released-plugins-together).

### Bundles

A bundle lists several plugins that Canvas Platform deploys together under one catalog listing. Set `"bundle": true`, name the plugins in `dependencies`, and describe the bundle in [`catalog`](#catalog). A bundle has no code of its own, so it needs at least one dependency and leaves out `components`, `custom_data`, `variables`, and `secrets`:

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "1.0.0",
  "name": "acme__intake_suite",
  "publisher": "acme",
  "description": "Intake form and visit summary, deployed together",
  "bundle": true,
  "dependencies": [
    {"name": "acme__intake_form", "publisher": "acme", "version": "1.16.0"},
    {"name": "acme__intake_summary", "publisher": "acme", "version": "1.14.0"}
  ],
  "catalog": {
    "title": "Intake Suite",
    "category": "Charting",
    "surfaces": ["Note"]
  },
  "tags": {},
  "license": "",
  "readme": false
}
```

Deploy a bundle with `canvas deploy`, like any other plugin. `canvas install` can't install one.

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
canvas validate acme__my_plugin
```

`canvas validate` checks the manifest against the schema and then loads every handler in the plugin sandbox, which catches disallowed imports and other errors that only appear on the instance. `canvas validate-manifest my_plugin` runs the manifest checks alone.
