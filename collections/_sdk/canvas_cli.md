---
title: "Canvas CLI"
---

{% include alert.html type="warning" content="The Canvas CLI signs in with <a href='#signing-in-to-canvas-platform'><code>canvas login</code></a> and ships plugins with <a href='#canvas-deploy'><code>canvas deploy</code></a>. Instance API credentials in <code>credentials.ini</code> and <code>canvas install</code> are deprecated, and support for them ends on <b>December 14, 2026</b>. See <a href='/guides/moving-to-canvas-platform/'>Moving to Canvas Platform</a>." %}

## Getting Started

### Installation using `pip`

To install the Canvas CLI using `pip`, execute `pip install canvas`. Python 3.11, 3.12, or 3.13 is required.

To upgrade the Canvas CLI if you installed using `pip`, execute `pip install --upgrade canvas`.

### Installation using `uv`

To install the Canvas CLI using `uv`, execute `uv tool install canvas`. `uv` will find or procure an acceptable Python version.

To upgrade the Canvas CLI if you installed using `uv`, execute `uv tool upgrade canvas`.

### Signing in to Canvas Platform

The Canvas CLI signs in to [Canvas Platform](https://platform.canvasmedical.com), which hosts each plugin's git repository and deploys it to the instances your organizations manage. Sign in once per machine:

```console
$ canvas login
Signed in to https://platform.canvasmedical.com as you@example.com.
  Acme Health (acme): plugin prefix acme__
```

`canvas login` opens your browser and also prints the sign-in URL, for a machine without a browser. It lists each organization you belong to with its plugin prefix. The session is stored in `~/.canvas/platform-credentials.json`, readable only by you, and refreshes itself. `canvas logout` revokes it. A CI/CD pipeline signs in with a [service account](#service-accounts-for-cicd) instead.

A plugin deployed through Canvas Platform has a publisher-prefixed name, `<org prefix>__<package>` (for example `acme__intake`), used for the manifest `name`, the package folder and its imports. The prefix decides which organization publishes the plugin.

`canvas login --platform <url>` or the `CANVAS_PLATFORM_URL` environment variable points the CLI at a platform other than https://platform.canvasmedical.com, and later commands keep using the platform you last signed in to.

**You are now ready to use the Canvas CLI.** Continue with [`canvas init`](#canvas-init) and [`canvas deploy`](#canvas-deploy).

### Service accounts for CI/CD

The Canvas CLI supports service accounts for automated pipelines such as GitHub Actions, GitLab CI or any other CI/CD system. A service account is an identity that belongs to your organization rather than to a person, so a pipeline that publishes and deploys plugins keeps working when the person who set it up leaves, and Canvas Platform's audit log names the service account behind each push and deploy. A pipeline signs in with the account's token instead of `canvas login`, which needs a browser.

**Create a service account.** An organization admin, plugin developer or deploy manager creates one on the Credentials page in Canvas Platform. A service account can hold the plugin developer and deploy manager roles, and never more than the person creating it holds: a plugin developer cannot create an account that deploys. Its token is shown once and is valid for a year.

**Use it in a pipeline.** Store the token as a secret in your CI/CD system and expose it to the job as the `CANVAS_PLATFORM_TOKEN` environment variable. No `canvas login` step is needed:

```yaml
- run: pip install canvas
- run: canvas deploy my-plugin/acme__my_plugin --instance acme-staging --yes
  env:
    CANVAS_PLATFORM_TOKEN: {% raw %}${{ secrets.CANVAS_PLATFORM_TOKEN }}{% endraw %}
```

- When `CANVAS_PLATFORM_TOKEN` is set, every command uses it in place of a `canvas login` session, including the git pushes `canvas deploy` makes. It takes precedence over a session already stored on the machine, so a runner always acts as its service account.
- `--yes` commits uncommitted changes without prompting. A deployment that needs consent for another plugin's custom data exits non-zero and lists the requests, because only a person at a terminal answers those.
- `CANVAS_PLATFORM_URL` points the job at a platform other than https://platform.canvasmedical.com.

**Rotate or revoke it.** The token does not refresh. Rotating it on the Credentials page ends the old token, and revoking the service account ends it for good; either way the CLI's next request says that Canvas Platform did not accept `CANVAS_PLATFORM_TOKEN`. `canvas logout` signs out only a browser session and leaves the token alone.

### Instance API credentials (`credentials.ini`): deprecated

{% include alert.html type="warning" content="<b>Deprecated:</b> authenticating the Canvas CLI with OAuth client credentials in <code>~/.canvas/credentials.ini</code>, and installing plugins with <code>canvas install</code>, are deprecated. Support ends on <b>December 14, 2026</b>. Sign in with <a href='#signing-in-to-canvas-platform'><code>canvas login</code></a> and deploy with <a href='#canvas-deploy'><code>canvas deploy</code></a> instead. <a href='/guides/moving-to-canvas-platform/'>Moving to Canvas Platform</a> walks through the switch." %}

With `credentials.ini`, the CLI authenticates to each instance with an OAuth client registered on that instance. `canvas install`, `enable`, `disable`, `list`, `config list` and `logs` authenticate this way today, as do `config set`, `config unset` and `uninstall` for a plugin Canvas Platform does not manage. Each of these commands moves to your Canvas Platform sign-in before December 14, 2026.

A machine can hold both a Canvas Platform sign-in and `credentials.ini` at once; the CLI picks per command and per plugin, as described in [Which plugins go through Canvas Platform](#which-plugins-go-through-canvas-platform).

The file has a section for each Canvas instance subdomain, with that instance's `client_id` and `client_secret`. For example, if your Canvas instance URL is `https://buttered-popcorn.canvasmedical.com/`, its section is `[buttered-popcorn]`. [Customer Authentication](/api/customer-authentication/#registering-a-third-party-application-on-canvas) explains how to register a client.

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

### Deprecation notices

`canvas install` prints a deprecation warning to standard error on every run. Every other command, at most once a day, prints a notice that authentication and deployment are changing, with a link to the migration steps. Both go to standard error, so they do not interfere with piped or redirected output.

### Which plugins go through Canvas Platform

`canvas config set`, `canvas config unset` and `canvas uninstall` work for plugins Canvas Platform manages and for plugins installed straight onto an instance, and each decides per plugin:

- A name without a prefix, or a machine that is not signed in, goes straight to the instance.
- Otherwise the CLI asks Canvas Platform for the plugin. If Canvas Platform has it, the command goes through Canvas Platform; if not, it goes to the instance.

`--instance` names the instances for a plugin Canvas Platform manages, and `--host` names an instance for one it does not; `--host` is refused for a managed plugin. An instance refuses `canvas install` for a plugin Canvas Platform manages, and the error names `canvas deploy`.

git signs in to Canvas Platform's git server through `canvas git-credential`, a hidden command that `canvas deploy`, `canvas init` and `canvas clone` register as the repository's credential helper. It mints a one-hour git token for the plugin named in the repository path.

## Update Notifications

The Canvas CLI automatically checks [PyPI](https://pypi.org/project/canvas/) for newer versions. If an update is available, a notice is printed to standard error after the command output:

```shell
[notice] A newer version of canvas is available (0.112.0 → 0.113.0). Upgrade with: pip install --upgrade canvas
```

- The check runs at most once every 12 hours; the result is cached locally to avoid unnecessary network requests.
- Because the notice is printed to standard error, it will not interfere with piped or redirected command output.
- To disable update checks, set the environment variable `CANVAS_NO_UPDATE_CHECK=1`.

<!-- source: discussion #611 -->
## Checking the SDK/runtime version on an instance

`canvas --version` reports the version of the locally installed CLI. To find the SDK/runtime version actually running on a given Canvas instance — useful when verifying that an expected SDK change is live — import `version` from `canvas_sdk.handlers.base` inside a plugin running on that instance:

```python
from canvas_sdk.handlers.base import version
from logger import log

log.info(f"SDK version: {version}")
```

## Usage

```console
$ canvas [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--version`
- `--help`: Show this message and exit.

## Commands

- `login`: Sign in to Canvas Platform through your browser
- `logout`: Sign out of Canvas Platform
- `init`: Create a new plugin
- `deploy`: Publish a plugin to Canvas Platform and deploy it
- `clone`: Clone a plugin's repository from Canvas Platform
- `uninstall`: Uninstall a plugin
- `enable`: Enable a plugin from a Canvas instance
- `disable`: Disable a plugin from a Canvas instance
- `list`: List all plugins from a Canvas instance
- `validate`: Validate a plugin's manifest and that all handlers load in the sandbox
- `validate-manifest`: Validate the Canvas Manifest json file
- `logs`: Listen and print log streams from a Canvas instance
- `config list`: List plugin variables on a Canvas instance
- `config set`: Set plugin variables
- `config unset`: Clear plugin variables
- `install`: Install a plugin into a Canvas instance (deprecated; use `deploy`)

### `canvas login`

Sign in to Canvas Platform through your browser (OAuth authorization code with PKCE). The sign-in URL is also printed, for a machine without a browser. See [Signing in to Canvas Platform](#signing-in-to-canvas-platform).

**Usage**:

```console
$ canvas login [OPTIONS]
```

**Options**:

- `--platform TEXT`: Canvas Platform URL. Defaults to `$CANVAS_PLATFORM_URL`, the platform you last signed in to, or https://platform.canvasmedical.com
- `--help`: Show this message and exit.

### `canvas logout`

Revoke this machine's Canvas Platform session and delete its stored tokens. A [service account token](#service-accounts-for-cicd) in `CANVAS_PLATFORM_TOKEN` is left alone, and the command says that commands still act as that account.

**Usage**:

```console
$ canvas logout [OPTIONS]
```

**Options**:

- `--platform TEXT`: Canvas Platform URL
- `--help`: Show this message and exit.

### `canvas init`

Create a new plugin. Signed in to Canvas Platform, the package is named `<org prefix>__<package>`, registered with Canvas Platform, and given a git repository whose `origin` is Canvas Platform, ready for `canvas deploy`. Signed out, it is named from the project name alone.

**Usage**:

```console
$ canvas init [OPTIONS] [PLUGIN_TYPE]
```

**Arguments**:

- `PLUGIN_TYPE`: `handler` (default) or `application`

**Options**:

- `--org TEXT`: Organization that publishes the plugin, when you can publish in several. Without it, `init` asks.
- `--help`: Show this message and exit.

### `canvas deploy`

Publish a plugin's code to Canvas Platform and deploy it to one or more instances.

**Usage**:

```console
$ canvas deploy [OPTIONS] PLUGIN_DIR
```

**Arguments**:

- `PLUGIN_DIR`: Path to the plugin package, the folder that holds `CANVAS_MANIFEST.json` [required]

**Options**:

- `--instance TEXT`: Instance slug to deploy to, repeatable. Without it, `deploy` targets the only instance you can deploy to, and otherwise lists the choices.
- `--ref TEXT`: Deploy a pushed branch, tag or commit as-is, without pushing.
- `--no-push`: Deploy the pushed `main` as-is, without pushing.
- `--push-only`: Push HEAD to `main` without deploying it to any instance, so the plugin's code and its [catalog listing](/sdk/canvas_manifest/#catalog) are updated on Canvas Platform. Takes no `--instance`, `--ref` or `--no-push`.
- `-y, --yes`: Commit uncommitted changes without prompting, with the default message. Does not approve consent requests.
- `--help`: Show this message and exit.

**Example**:

```console
$ canvas deploy paperwork-eviscerator/acme__paperwork_eviscerator --instance acme-staging
```

**Notes**:

**What `deploy` does**

1. Registers the plugin with Canvas Platform under the organization its prefix names. The manifest `name` must be publisher-prefixed.
2. Points the repository's `origin` at Canvas Platform, with `canvas` as git's credential helper for it.
3. Commits uncommitted changes after you confirm. Without a terminal to confirm at, it refuses uncommitted changes unless you pass `--yes`.
4. Pushes HEAD to `main`, deploys that commit to each instance, and waits for each instance's outcome.

The command exits non-zero unless every instance succeeds, so it can gate a CI job.

**Plugin repository layout**

Canvas Platform hosts one git repository per plugin, rooted at the directory that contains the package:

```text
paperwork-eviscerator/          # repository root
├── acme__paperwork_eviscerator/
│   ├── CANVAS_MANIFEST.json
│   └── handlers/
├── pyproject.toml
└── tests/
```

`canvas init` creates this layout. If the package is not in a git repository yet, `deploy` offers to create one at its parent directory. A package nested deeper inside a larger repository is refused; move it into its own repository, or `canvas clone` it.

Because `deploy` pushes a git commit, `.gitignore` decides what reaches Canvas Platform. Keep virtual environments, `node_modules` and local secrets out of the repository with it.

**Consent for cross-plugin data access**

A plugin that reads another plugin's [custom data](/sdk/custom-data-sharing-data/) needs consent before it deploys. At a terminal, `deploy` shows each consent request and asks you to answer it. Under `--yes`, or without a terminal, it lists the requests with the deployment id and exits non-zero without answering them.

**Validate first**

Run [`canvas validate`](#canvas-validate) before you deploy. It runs the manifest checks, the static lint, and sandbox-load validation locally, where errors are faster to fix than after a push.

### `canvas clone`

Clone a plugin's repository from Canvas Platform with `origin` and the credential helper set, ready for `canvas deploy`.

**Usage**:

```console
$ canvas clone [OPTIONS] NAME [DIRECTORY]
```

**Arguments**:

- `NAME`: Plugin name, e.g. `acme__intake` [required]
- `DIRECTORY`: Where to clone it, a directory named after the plugin by default

**Options**:

- `--help`: Show this message and exit.

### `canvas install`

{% include alert.html type="warning" content="<b>Deprecated:</b> <code>canvas install</code> uploads a plugin straight onto an instance using <code>credentials.ini</code>. Support ends on <b>December 14, 2026</b>. Use <a href='#canvas-deploy'><code>canvas deploy</code></a>, and see <a href='/guides/moving-to-canvas-platform/'>Moving to Canvas Platform</a>." %}

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

**Where to run it**

<!-- source: discussion #1159 -->
- Run it from one directory **above** the plugin folder, the one that holds `CANVAS_MANIFEST.json`, and pass the folder name. If the manifest is at `extensions/encounter_list/CANVAS_MANIFEST.json`, run this from `extensions`:

  ```console
  $ canvas install encounter_list --host your-host
  ```
- Or run `canvas install .` from inside the plugin folder.
- The command is `canvas install`. There is no `canvas plugin install`.

**Plugin folder layout**

<!-- source: discussion #1527 -->
- Keep the manifest, the package's `__init__.py`, and the folders it references (such as `routes/` and `protocols/`) in the same directory. Class paths in the manifest, such as `my_plugin.routes.charting`, resolve from there.
- An extra level of nesting, with the manifest outside the inner package folder, makes those paths resolve one level too deep. The plugin loads, but its SimpleAPI endpoints return an empty 404, often with nothing in `canvas logs`. If that happens, check the folder structure and that every import in the referenced modules resolves.

**Validation before upload**

`canvas install` runs the same checks as [`canvas validate`](#canvas-validate) before it uploads anything:
- Manifest validation (schema, tags, handler resolution)
- [Static lint](#static-lint) (scans your source for sandbox-forbidden constructs and Custom Data mistakes)
- Sandbox-load validation (imports every handler in the sandbox)

If the static lint reports an error, or a handler fails to load (for example, because of a disallowed import like `subprocess`), the install stops before the plugin is built or uploaded. Run `canvas validate` first for detailed per-handler results.

**What gets packaged**

The CLI packages every file in the plugin folder except:
- `__pycache__` directories
- `*.pyc` and `*.pyo` files
- `node_modules` directories
- Hidden files and directories (for example, `.git` and `.env`)
- Symlinks

To exclude more files, add a `.canvasignore` file:
- Put it in the directory you run `canvas install` from. The CLI reads it from the current working directory, not from the plugin folder.
- It uses [.gitignore](https://git-scm.com/docs/gitignore) syntax, and its patterns match paths relative to the plugin folder.

```md
# Exclude test files
test_*.py
```

The CLI prints a warning, but still installs, when a single file is over 1 MB, the package holds more than 100 files, or its total size is over 1 MB.

**Troubleshooting**

<!-- source: discussion #795 -->
- **The install fails with an HTTP 500:** the package usually has too many files, most often because a Python virtual environment was created inside the plugin folder. Rename the folder so it starts with a dot (for example, `.canvas-env`), since hidden folders aren't packaged, or list it in `.canvasignore`.

### `canvas uninstall`

Uninstall a plugin. A plugin Canvas Platform manages is removed by an uninstall deployment from each `--instance`, which is required. Any other plugin is removed from the instance directly, using `credentials.ini` (deprecated; see [Instance API credentials](#instance-api-credentials-credentialsini-deprecated)).

**Usage**:

```console
$ canvas uninstall [OPTIONS] NAME
```

**Arguments**:

- `NAME`: Plugin name to uninstall [required]

**Options**:

- `--instance TEXT`: Instance slug to uninstall from, repeatable
- `--host TEXT`: Canvas instance to connect to, for a plugin Canvas Platform does not manage
- `--force`: Uninstall an enabled plugin from an instance directly
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

{% include alert.html type="info" content="Run <code>canvas validate</code> before <code>canvas deploy</code> so violations are caught on your machine before they reach an instance." %}

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

{% include alert.html type="info" content="Use <code>canvas validate</code> before <code>canvas deploy</code> for a full pre-flight check: manifest validation, the static lint, and sandbox-load validation, with detailed per-handler output." %}

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

Set (or update) one or more plugin variables. Pass one or more `KEY=value` pairs as positional arguments.

For a plugin Canvas Platform manages, the values are stored in Canvas Platform and a configure deployment brings them to the running plugin on each `--instance`. Without `--instance`, the only instance the plugin is installed on that you can configure is targeted. Values are kept per instance, and a later `canvas deploy` carries them forward.

For a plugin Canvas Platform does not manage, the values are written to the instance directly with `credentials.ini` (deprecated; see [Instance API credentials](#instance-api-credentials-credentialsini-deprecated)).

**Usage**:

```console
$ canvas config set [OPTIONS] PLUGIN [KEY=VALUE]...
```

**Examples**:

Set a single variable:

```console
$ canvas config set acme__my_plugin API_TOKEN=your_api_token_value --instance acme-staging
```

Set multiple variables in one call:

```console
$ canvas config set acme__my_plugin API_TOKEN=abc123 LOG_LEVEL=info --instance acme-staging
```

Set a variable whose value is a list with one entry per line — for example a redirect allowlist (see the [Redirect effect](/sdk/effect-redirect/)). The value is newline-delimited (not comma-separated), so use your shell's newline quoting to preserve the line breaks. In bash/zsh, ANSI-C quoting (`$'…'`) turns `\n` into a real newline:

```console
$ canvas config set acme__my_plugin $'REDIRECT_ALLOWLIST_INTERNAL=/panel\n/patient' --instance acme-staging
```

**Arguments**:

 - `PLUGIN`:  Plugin name to set variables for
 - `KEY=VALUE...`: Variables to set, keeping each one's declared sensitivity

**Options**:

- `--instance TEXT`: Instance slug to configure, repeatable
- `--secret KEY=VALUE`: Set a sensitive value for a key no revision of the manifest declares, repeatable
- `--variable KEY=VALUE`: Set a non-sensitive value for a key no revision of the manifest declares, repeatable
- `--host TEXT`: Canvas instance to connect to, for a plugin Canvas Platform does not manage
- `--help`: Show this message and exit.

> Whether each value is treated as sensitive is determined by the plugin's `CANVAS_MANIFEST.json` (`variables: [{name, sensitive}]`) — `canvas config set` does not change the sensitive flag of a declared variable.

### `canvas config unset`

Clear one or more plugin variables. For a plugin Canvas Platform manages, the values are cleared in Canvas Platform and a configure deployment removes them from the running plugin. For any other plugin, each value is set to empty on the instance directly.

**Usage**:

```console
$ canvas config unset [OPTIONS] PLUGIN KEY...
```

**Arguments**:

 - `PLUGIN`: Plugin name to clear variables for
 - `KEY...`: Variable keys to clear, e.g. `API_KEY`

**Options**:

- `--instance TEXT`: Instance slug to configure, repeatable
- `--host TEXT`: Canvas instance to connect to, for a plugin Canvas Platform does not manage
- `--help`: Show this message and exit.
