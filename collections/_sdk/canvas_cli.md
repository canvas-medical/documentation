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

## Control Room beta

This section covers the Canvas CLI commands available in the Control Room beta.

Control Room is the authoritative git home for a plugin. The CLI never talks to it directly: it goes through your own Canvas instance, which proxies to Control Room and signs short-lived tokens on your behalf. There is no separate Control Room login — authentication stays per-instance and automatic through the `~/.canvas/credentials.ini` OAuth flow described in [Configuration and Authenticating to Your Canvas Instance](#configuration-and-authenticating-to-your-canvas-instance). The git credential helper mints a fresh, short-lived credential for each push, so nothing long-lived is stored. These commands assume you're comfortable with basic git operations — commits, remotes, and pushes.

Before you use these commands, make sure your Canvas account meets both prerequisites below. If it doesn't, every beta command fails:

- **A developer role.** The user must hold the Administrative Developer or Clinical Developer role on the instance. Without one of these roles, the command fails and tells you which roles are required.
- **An email address.** The user must have an email address on their account. Control Room identifies you — the developer it is acting on behalf of — by that email, so a command run as a user with no email, including a client-credentials token, which has no user, fails and tells you to add an email address.

To use these commands, set the environment variable `CONTROL_ROOM_BETA` to `true` (case-insensitive). You must export it yourself. No distribution sets it for you. When it is not set, these commands do not appear and the CLI keeps its existing behavior.

{% include alert.html type="info" content="These commands are part of the <b>Control Room beta</b>. They register only when the <code>CONTROL_ROOM_BETA</code> environment variable is set to <code>true</code>. Without it, the CLI keeps its existing behavior." %}

## Commands

- `init`: Create a new plugin
- `install`: Install a plugin into a Canvas instance
- `deploy`: Build and install a plugin on this instance through Control Room, publishing the current code first if needed (Control Room beta)
- `cr-init`: Connect a plugin's git repo to Control Room (Control Room beta)
- `uninstall`: Uninstall a plugin from a Canvas instance (behaves differently in the Control Room beta)
- `enable`: Enable a plugin from a Canvas instance
- `disable`: Disable a plugin from a Canvas instance
- `list`: List all plugins from a Canvas instance
- `validate`: Validate a plugin's manifest and that all handlers load in the sandbox
- `validate-manifest`: Validate the Canvas Manifest json file
- `logs`: Listen and print log streams from a Canvas instance
- `config list`: List plugin variables on a Canvas instance
- `config set`: Set plugin variables on a Canvas instance (behaves differently in the Control Room beta)
- `config unset`: Unset plugin variables via Control Room (Control Room beta)

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

### `canvas deploy`

Build and install a plugin on this instance through Control Room, publishing the current code to Control Room's git repository first if needed.

{% include alert.html type="info" content="Available only in the <a href='#control-room-beta'>Control Room beta</a>." %}

**Usage**:

```console
$ canvas deploy [OPTIONS] PLUGIN_NAME
```

**Arguments**:

- `PLUGIN_NAME`: Path to the plugin to deploy [required]

**Options**:

- `--ref TEXT`: Deploy an already-published git ref (a tag or older commit) as-is, without pushing.
- `--no-push`: Deploy the current `main` ref as-is, without pushing `HEAD` first.
- `--host TEXT`: Canvas instance to connect to.
- `--yes`, `-y`: Approve all consent prompts non-interactively.
- `--help`: Show this message and exit.

**Notes**:

The one-shot happy path runs without `--ref` or `--no-push`. In order, `canvas deploy`:

1. Checks that the plugin is in a git repo. At an interactive terminal, it offers to run `git init` at the repo root — the parent of the plugin package directory — if none exists yet.
2. Registers the plugin's Control Room repo.
3. Points `origin` at Control Room and wires up the push-credential helper.
4. Commits the working tree interactively: it shows the pending changes, asks to commit and deploy, and prompts for a commit message that defaults to `Deploy via canvas`.
5. Pushes `HEAD` to `main`.
6. Builds and installs, polling until the deploy reaches a terminal outcome: succeeded, failed, partial, or cancelled.

On a non-success outcome (failed, partial, or cancelled), or if it cannot confirm completion within the wait window, `canvas deploy` exits with a nonzero status (code 1) — the same convention as [`canvas validate`](#canvas-validate). A successful deploy exits 0. Check `canvas logs` for the cause, then re-run `canvas deploy` once you've fixed the issue.

Pushes are authenticated by a git credential helper the CLI wires up automatically.

To deploy an already-published ref instead of pushing, use one of `--ref` or `--no-push`: `--ref` deploys the named tag or commit, and `--no-push` deploys the current `main` as-is. Omit both to publish and deploy the current `HEAD`.

Running with a dirty or uninitialized git tree and no interactive terminal — in CI or a script — errors rather than committing unattended. Commit and initialize the repo first, or pass `--ref` or `--no-push` to deploy an already-published ref.

Control Room requires the `canvas init` layout `<repo>/<package>/CANVAS_MANIFEST.json` and rejects a manifest at the repo root, so the git repo must be rooted one level above the package directory. See [Handler resolution and directory layout](#handler-resolution-and-directory-layout).

A gated deploy — one that needs cross-plugin custom-data access, for example — prints its consent requests and prompts you to approve or deny each one inline. Pass `--yes` or `-y` to approve all non-interactively.

### `canvas cr-init`

Connect a plugin's git repo to Control Room by setting up its `origin` remote and the push-credential helper, without deploying. Running it is a one-time, idempotent setup step.

Use `cr-init` when you'd rather manage commits and pushes yourself with plain git, or want to connect the repo to Control Room before you're ready to deploy. The one-shot `canvas deploy` runs this same setup for you, so the default flow needs no `cr-init` first.

{% include alert.html type="info" content="Available only in the <a href='#control-room-beta'>Control Room beta</a>." %}

**Usage**:

```console
$ canvas cr-init [OPTIONS] PLUGIN_NAME
```

**Arguments**:

- `PLUGIN_NAME`: Path to the plugin to connect to Control Room [required]

**Options**:

- `--host TEXT`: Canvas instance to connect to.
- `--repo-name TEXT`: Git repository name in Control Room. The plugin path must be an existing directory, but with `--repo-name` its `CANVAS_MANIFEST.json` need not exist yet — Control Room tracks the git repository name separately from the plugin package name. Without `--repo-name`, `cr-init` reads the manifest to default the repository name, so the manifest must be present in that case.
- `--help`: Show this message and exit.

**Example**:

On success, `cr-init` prints a confirmation naming the connected repository and the `origin` remote, then shows the plain-git commands to publish and deploy — the sequence below. If it cannot reach Control Room, or you lack a plugin-developer role, it fails with an actionable error instead. Git authenticates the push through the credential helper that `cr-init` set up.

```console
$ git add -A && git commit -m "your message"
$ git push origin HEAD:main
$ canvas deploy my_plugin --host buttered-popcorn
```

### `canvas uninstall`

Uninstall a plugin from a Canvas instance.

**Usage**:

```console
$ canvas uninstall [OPTIONS] NAME
```

**Arguments**:

- `NAME`: Plugin name to delete [required]

**Options (GA)**:

- `--force`: Force uninstallation of the plugin
- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

#### Control Room beta

In the [Control Room beta](#control-room-beta), `uninstall` routes through Control Room, because the instance refuses a direct CLI uninstall of a Control-Room-managed plugin. The beta variant takes the plugin name and `--host` only. It does not expose `--force`.

**Options (Control Room beta)**:

- `--host TEXT`: Canvas instance to connect to.
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

Set (or update) one or more plugin variables directly on a Canvas instance (the GA path). Each variable must already be declared in the plugin's `CANVAS_MANIFEST.json`. Pass one or more `KEY=value` pairs as positional arguments.

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

**Options (GA)**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

> On the direct-to-instance (GA) path, whether each value is treated as sensitive is determined by the plugin's `CANVAS_MANIFEST.json` (`variables: [{name, sensitive}]`) — `canvas config set` does not change the sensitive flag.

#### Control Room beta

In the [Control Room beta](#control-room-beta), `config set` routes through Control Room, which owns each variable's sensitivity.

**Options (Control Room beta)**:

- `--secret TEXT`: Set a sensitive, write-only variable, e.g. Key=value. Repeatable.
- `--variable TEXT`: Set a plain, non-sensitive variable, e.g. Key=value. Repeatable.
- `--host TEXT`: Canvas instance to connect to.
- `--help`: Show this message and exit.

Positional `VARIABLES` are bare `KEY=value` pairs.

**Sensitivity rules**:

- Declaring a net-new variable requires a flag, either `--secret` or `--variable`.
- A bare `KEY=value` updates an existing variable and preserves its current sensitivity.
- A bare `KEY=value` for a key that does not exist yet is rejected until you declare it with a flag.
- A plain variable can be promoted to a secret with `--secret`, but a secret is never demoted to plain.

If the plugin is not installed on the instance, the values are stored in Control Room and applied on the next deploy. The command reports this.

### `canvas config unset`

Unset plugin variables via Control Room. This command has no direct-instance equivalent and appears only in the Control Room beta.

{% include alert.html type="info" content="Available only in the <a href='#control-room-beta'>Control Room beta</a>." %}

**Usage**:

```console
$ canvas config unset [OPTIONS] PLUGIN_NAME KEYS...
```

**Arguments**:

- `PLUGIN_NAME`: Plugin name to configure [required]
- `KEYS...`: Variable key names to unset, e.g. API_KEY [required]

**Options**:

- `--host TEXT`: Canvas instance to connect to.
- `--help`: Show this message and exit.

**Notes**:

`config unset` clears each key's value on the instance and pushes a reconcile so the instance drops them — omitting a key from the plugin's configuration deletes it. The change is immediate and needs no redeploy. Clearing a key that was never set is a no-op.
