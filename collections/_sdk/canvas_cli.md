---
title: "Canvas CLI"
---

## Getting Started

### Installation using `pip`

To install the Canvas CLI using `pip`, execute `pip install canvas`. Python 3.11, 3.12, or 3.13 is required.

To upgrade the Canvas CLI if you installed using `pip`, execute `pip install --upgrade canvas`.

### Installation using `uv`

To install the Canvas CLI using `uv`, execute `uv tool install canvas`. `uv` will find or procure an acceptable Python version.

To upgrade the Canvas CLI if you installed using `uv`, execute `uv tool upgrade canvas`.

### Configuration and Authenticating to Your Canvas Instance

Create a file `~/.canvas/credentials.ini` with sections for each of your Canvas instance subdomains, and add client_id and client_secret credentials to each section. For example, if your Canvas instance url is `https://buttered-popcorn.canvasmedical.com/`, you would have a section `[buttered-popcorn]` with key-value pairs for `client_id` and `client_secret`.

{% include alert.html type="info" content= "<b>Getting Credentials: </b>Learn how to get register a client_id and client_secret <a href='/api/customer-authentication/#registering-a-third-party-application-on-canvas'>here</a>.<br/>The Canvas CLI uses OAuth, just like the FHIR API."  %}

**Example:**

```ini
[buttered-popcorn]
client_id=butter
client_secret=salt

[dev-buttered-popcorn]
client_id=devbutter
client_secret=devsalt
is_default=true

[localhost]
client_id=localclientid
client_secret=localclientsecret
```

You can define your default host with `is_default=true`. If no default is explicitly defined, the Canvas CLI will use the first instance in the file as the default for each of the CLI commands.

**You are now ready to use the Canvas CLI**

## Update Notifications

The Canvas CLI automatically checks [PyPI](https://pypi.org/project/canvas/) for newer versions. If an update is available, a notice is printed to standard error after the command output:

```shell
[notice] A newer version of canvas is available (0.112.0 → 0.113.0). Upgrade with: pip install --upgrade canvas
```

- The check runs at most once every 12 hours; the result is cached locally to avoid unnecessary network requests.
- Because the notice is printed to standard error, it will not interfere with piped or redirected command output.
- To disable update checks, set the environment variable `CANVAS_NO_UPDATE_CHECK=1`.

## Usage

```console
$ canvas [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--version`
- `--help`: Show this message and exit.

## Commands

- `init`: Create a new plugin
- `install`: Install a plugin into a Canvas instance
- `uninstall`: Uninstall a plugin from a Canvas instance
- `enable`: Enable a plugin from a Canvas instance
- `disable`: Disable a plugin from a Canvas instance
- `list`: List all plugins from a Canvas instance
- `validate`: Validate a plugin's manifest and that all handlers load in the sandbox
- `validate-manifest`: Validate the Canvas Manifest json file
- `logs`: Listen and print log streams from a Canvas instance
- `config list`: List plugin variables on a Canvas instance
- `config set`: Set plugin variables on a Canvas instance

### `canvas init`

Create a new plugin.

**Usage**:

```console
$ canvas init [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

### `canvas install`

Install a plugin into a Canvas instance.

**Usage**:

```console
$ canvas install [OPTIONS] PLUGIN_NAME
```

**Arguments**:

- `PLUGIN_NAME`: Path to plugin to install [required]

**Options**:

- `--variable TEXT`: Non-sensitive variables to set, e.g. Key=value
- `--secret TEXT`: Sensitive variables to set (treated as sensitive=true), e.g. Key=value
- `--enable / --disable`: Install the plugin in an enabled or disabled state. Defaults to `--enable`.
- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

**Notes**:

Before uploading, `canvas install` runs the same pre-flight validation as [`canvas validate`](#canvas-validate):
- Manifest validation (schema, tags, handler resolution)
- [Static lint](#static-lint) (scans your source for sandbox-forbidden constructs and Custom Data mistakes)
- Sandbox-load validation (imports every handler in the sandbox)

If the static lint reports an error, or any handler fails to load — for example, due to a disallowed import like `subprocess` — the install aborts before the plugin is built or uploaded, so it never reaches your instance. Run `canvas validate` first for detailed per-handler results.

The CLI automatically excludes common build artifacts from the plugin bundle:
- `__pycache__` directories
- `*.pyc` and `*.pyo` files
- `node_modules` directories
- Hidden files and directories (e.g., `.git`, `.env`)

To exclude additional files, create a `.canvasignore` file in your plugin directory. This file follows the same syntax as [.gitignore](https://git-scm.com/docs/gitignore).

Example
```md
# Exclude test files
test_*.py
```

### `canvas uninstall`

Uninstall a plugin from a Canvas instance.

**Usage**:

```console
$ canvas uninstall [OPTIONS] NAME
```

**Arguments**:

- `NAME`: Plugin name to delete [required]

**Options**:

- `--force`: Force uninstallation of the plugin
- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

### `canvas enable`

Enable a plugin from a Canvas instance..

**Usage**:

```console
$ canvas enable [OPTIONS] NAME
```

**Arguments**:

- `NAME`: Plugin name to enable [required]

**Options**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

### `canvas disable`

Disable a plugin from a Canvas instance..

**Usage**:

```console
$ canvas disable [OPTIONS] NAME
```

**Arguments**:

- `NAME`: Plugin name to disable [required]

**Options**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

### `canvas list`

List all plugins on a Canvas instance.

**Usage**:

```console
$ canvas list [OPTIONS]
```

**Options**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

### `canvas validate`

Validate a plugin's manifest and that all handlers load in the sandbox.

**Usage**:

```console
$ canvas validate [OPTIONS] PLUGIN_NAME
```

**Arguments**:

- `PLUGIN_NAME`: Path to plugin to validate [required]

**Options**:

- `--help`: Show this message and exit.

This command runs full pre-flight validation combining:

1. **Manifest validation** — Schema checks, tag validation, handler resolution, and unreferenced handler warnings (everything `validate-manifest` does).
2. **Static lint** — Scans the plugin's source for sandbox-forbidden constructs and Custom Data mistakes before any code runs.
3. **Sandbox-load validation** — Imports every handler the way the plugin runner will, catching violations that would otherwise surface only at runtime on the instance.

#### Static lint

Before it loads any handlers, `canvas validate` scans every `.py` file in the plugin — skipping directories like `tests`, `build`, and `dist` *within* the plugin — for patterns that compile cleanly but fail, or silently misbehave, once your code runs on the instance. Each finding is reported with a rule code in brackets. Warnings are printed but do not block validation; any error fails the command and exits with code 1.

```console
$ canvas validate my_plugin
  ⚠ my_plugin/handlers/protocol.py:42  [custom-model-id-vs-dbid]  Widget.objects.filter(id=…) — CustomModels use `dbid` as their primary key (only core SDK models have `id`). Use `dbid=…` instead.

These issues will fail on the instance (sandbox / Custom Data):
  ✗ my_plugin/handlers/protocol.py:18  [setattr-blocked]  `setattr()` is blocked by the sandbox. Use direct attribute assignment (`obj.attr = value`) instead.
```

**Sandbox constructs (errors).** These compile under RestrictedPython but are rejected when a handler runs on the instance, so a plain sandbox load can miss them. See [Sandboxing and Allowed Imports](/sdk/sandboxing-and-allowed-imports/#forbidden-constructs) for the full list and the allowed alternatives.

| Rule code | Flags |
| --- | --- |
| `setattr-blocked` | `setattr(obj, "x", value)` — use `obj.x = value` |
| `delattr-blocked` | `delattr(obj, "x")` — use `del obj.x` |
| `bytearray-blocked` | `bytearray(...)` — use `bytes` for binary data |
| `type-blocked` | Any call to `type()`. It is absent from the sandbox builtins, so even the one-argument `type(x)` raises `NameError` — use `isinstance(x, SomeClass)` or `x.__class__.__name__`, and declare classes with `class …:` rather than `type(name, bases, dict)` |
| `augmented-subscript` | Augmented assignment on a subscript, e.g. `d[k] += v` — rewrite as `d[k] = d[k] + v` |
| `augmented-attribute` | Augmented assignment on an attribute, e.g. `obj.attr += v` — rewrite as `obj.attr = obj.attr + v` |

`@dataclass(frozen=True)` and `@dataclass(slots=True)` load and run fine in the sandbox and are intentionally not flagged.

**Custom Data (errors).** Both leave tables silently uncreated, so queries fail at runtime. See [Custom Models](/sdk/custom-data-custom-models/) and the [Quick Start](/sdk/custom-data-quick-start/) for setup.

| Rule code | Flags |
| --- | --- |
| `custom-model-wrong-dir` | A `CustomModel` subclass defined outside `<plugin>/models/` — Canvas only loads models from that directory |
| `missing-custom-data-block` | CustomModels are present but the manifest has no `custom_data` block (an empty block counts as missing — it must be non-empty) |

**Custom Data (warnings).** These don't block validation but usually indicate a bug:

| Rule code | Flags |
| --- | --- |
| `custom-model-id-vs-dbid` | `.filter(id=…)` / `.get(id=…)` on a local CustomModel — CustomModels key on `dbid`, not `id`. Use `dbid=…` |
| `lazy-fk-string-ref` | A `ForeignKey`/`OneToOneField`/`ManyToManyField` with a string reference to a CustomModel defined in this plugin — import the class and pass it directly |

#### Sandbox-load validation

After the static lint passes, sandbox-load validation executes each handler module in the plugin sandbox to catch:

- **Disallowed imports** — Modules like `subprocess`, `socket`, or `os` that are blocked by the sandbox.
- **RestrictedPython compile-time errors** — Syntax or constructs that RestrictedPython cannot compile.
- **Import errors** — Missing dependencies or broken imports.

For each handler, the output shows whether it loaded successfully:

```console
$ canvas validate my_plugin
Loading 2 handler(s) in the sandbox:
  ✓ my_plugin.handlers.events:MyHandler
  ✗ my_plugin.handlers.api:APIHandler
    ImportError: 'subprocess' is not an allowed import
1 of 2 handler(s) failed to load in the sandbox.
```

The command exits with code 1 if any handler fails validation.

#### Limitations

A passing `canvas validate` confirms that handlers import cleanly under the sandbox — it does not guarantee the plugin is fully sandbox-clean. RestrictedPython checks attribute and item access inside `compute()` at request time, not at import time, so violations during handler execution won't be caught by this command.

{% include alert.html type="info" content="<code>canvas install</code> runs this same static lint and sandbox-load validation before uploading, so violations are caught before they reach your instance." %}

### `canvas validate-manifest`

Validate the Canvas Manifest json file.

**Usage**:

```console
$ canvas validate-manifest [OPTIONS] PLUGIN_NAME
```

**Arguments**:

- `PLUGIN_NAME`: Path to plugin to validate [required]

**Options**:

- `--help`: Show this message and exit.

**Validations performed**:

1. **Schema validation** — Checks that `CANVAS_MANIFEST.json` contains all required fields and valid values.
2. **Handler resolution** — Verifies that every handler class declared in the manifest (`protocols`, `applications`, and `handlers`) resolves to a file the plugin runner can find at runtime.

#### Handler resolution and directory layout

The plugin runner loads handlers by mapping dotted module paths to files relative to the plugin's install directory. For a plugin named `my_plugin` with a handler class `my_plugin.handlers.events:MyHandler`, the runner expects `handlers/events.py` inside the plugin directory — the directory containing `CANVAS_MANIFEST.json`.

A common mistake is placing `CANVAS_MANIFEST.json` in a parent directory above the plugin package. This passes schema validation and works locally, but fails at runtime with `ModuleNotFoundError` — the handler files are nested one level too deep.

**Correct layout:**

```text
my_plugin/
├── CANVAS_MANIFEST.json   # ← manifest inside the package
├── handlers/
│   └── events.py
└── ...
```

**Incorrect layout:**

```text
project/
├── CANVAS_MANIFEST.json   # ← manifest above the package (wrong!)
└── my_plugin/
    └── handlers/
        └── events.py
```

If `validate-manifest` detects handlers that won't resolve, it reports which classes are affected and the file paths the runner expects:

```console
Error: these handler classes won't be found by the plugin runner with the current directory layout:
  - my_plugin.handlers.events:MyHandler
    runner expects: my_plugin/handlers/events.py

CANVAS_MANIFEST.json must live inside the plugin's package directory (the directory whose name matches the manifest "name"), alongside the handler packages — not in a parent directory above them.
```

{% include alert.html type="info" content="<code>canvas install</code> runs manifest validation, the static lint, and sandbox-load validation before uploading. Use <code>canvas validate</code> for a full pre-flight check with detailed per-handler output." %}

### `canvas logs`

Subscribes to a log stream and prints to your console. Optionally fetches historical logs first.

**Usage**:

```console
$ canvas logs [OPTIONS]
```

**Options**:

- `--host TEXT`:           Canvas instance to connect to
- `--help`:                Show this message and exit.
-  `--since TEXT`:         Lookback window (e.g. '24h', '2h30m'). Mutually exclusive with --start/--end.
-  `--start TEXT`:         Start time (ISO/RFC3339) or 'now'.
-  `--end TEXT`:           End time (ISO/RFC3339) or 'now'. Defaults to now if start is provided.
-  `--no-follow`:          Historical only; do not stream live logs.
-  `--level TEXT`:         Repeatable. --level ERROR --level WARN
-  `--source TEXT`:        Filter by source/service.
-  `--plugin TEXT`:        Repeatable. --plugin foo --plugin bar.
-  `--handler TEXT`:       Repeatable. Qualified handler name (e.g. my_plugin.handlers.Foo).
-  `--page-size INTEGER`:  Fetch size per page (historical).  \[default: 200]
-  `--limit INTEGER`:      Max historical logs to print.
-  `--all`:                Fetch all pages until exhausted (historical).
-  `--interactive`:        After each page, prompt to load more.
-  `--cursor TEXT`:        Resume token from a previous run.
-  `--help`:               Show this message and exit.


### `canvas config list`

List plugin variables on a Canvas instance. Each variable is rendered as `[set]` or `[not set]`, with a `(sensitive)` annotation for sensitive variables. Values themselves are never displayed — to read a value, use the Django Admin UI (gated by managing-user permissions).

**Usage**:

```console
$ canvas config list [OPTIONS] PLUGIN
```

**Example output**:

```console
$ canvas config list my_plugin
  API_TOKEN  [set]  (sensitive)
  LOG_LEVEL  [not set]
```

**Arguments**:

 - `PLUGIN`:  Plugin name to list variables for

**Options**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

**Example Output**:

```console
$ canvas config list my_plugin
  API_TOKEN = [set]  (sensitive)
  WEBHOOK_URL = [set]
  DEBUG_MODE = [not set]
```


### `canvas config set`

Set (or update) one or more plugin variables on a Canvas instance. Each variable must already be declared in the plugin's `CANVAS_MANIFEST.json`. Pass one or more `KEY=value` pairs as positional arguments.

**Usage**:

```console
$ canvas config set [OPTIONS] PLUGIN VARIABLES...
```

**Examples**:

Set a single variable:

```console
$ canvas config set my_plugin API_TOKEN=your_api_token_value
```

Set multiple variables in one call:

```console
$ canvas config set my_plugin API_TOKEN=abc123 LOG_LEVEL=info
```

Set a variable whose value is a list with one entry per line — for example a redirect allowlist (see the [Redirect effect](/sdk/effect-redirect/)). The value is newline-delimited (not comma-separated), so use your shell's newline quoting to preserve the line breaks. In bash/zsh, ANSI-C quoting (`$'…'`) turns `\n` into a real newline:

```console
$ canvas config set my_plugin $'REDIRECT_ALLOWLIST_INTERNAL=/panel\n/patient'
```

**Arguments**:

 - `PLUGIN`:  Plugin name to set variables for
 - `VARIABLES...`: Variables to set, e.g. Key=value

**Options**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

> Whether each value is treated as sensitive is determined by the plugin's `CANVAS_MANIFEST.json` (`variables: [{name, sensitive}]`) — `canvas config set` does not change the sensitive flag.
