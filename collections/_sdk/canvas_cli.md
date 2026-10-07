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

{% include alert.html type="warning" content="<b>Deprecated:</b> Installing plugins directly on an instance with <code>credentials.ini</code> and <code>canvas install</code> is deprecated in favor of deploying through <a href='#canvas-platform'>Canvas Platform</a>. It isn't supported as of December 14, 2026. See <a href='#moving-from-credentialsini-to-canvas-platform'>Moving from credentials.ini to Canvas Platform</a>."  %}

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

## Canvas Platform

Canvas Platform hosts each plugin's git repository and deploys the plugin to the Canvas instances it manages. Instead of uploading a package to one instance with `canvas install`, you push the plugin's code with `canvas deploy`. Canvas Platform then rolls it out to the instances you choose.

### Signing in

Sign in once per machine with [`canvas login`](#canvas-login), which opens your browser. The CLI stores the session in `~/.canvas/platform-credentials.json`, readable only by you, and refreshes it automatically. `canvas login` also lists the plugin prefix of each organization you belong to.

The CLI connects to `https://platform.canvasmedical.com` by default. To use a different Canvas Platform, pass `--platform <url>` to `canvas login` or set the `CANVAS_PLATFORM_URL` environment variable. Later commands keep using the platform you last signed in to.

### Plugin names

A plugin deployed through Canvas Platform has a publisher-prefixed name in the form `<org prefix>__<package>`, such as `acme__intake`. The prefix decides which of your organizations publishes the plugin. Use the full name for the manifest `name`, the package folder, and the package's imports. A name can contain only lowercase letters, digits, and underscores, and the part after the prefix must start with a letter.

When you're signed in, [`canvas init`](#canvas-init) adds your organization's prefix to the name for you.

### Which plugins go through Canvas Platform

`canvas config set`, `canvas config unset`, and `canvas uninstall` work for plugins Canvas Platform manages and for plugins installed directly on an instance. Each command decides per plugin:

- If the name has no prefix, or you aren't signed in to Canvas Platform, the command goes directly to the instance.
- Otherwise, the CLI asks Canvas Platform whether it manages the plugin. If it does, the command goes through Canvas Platform, and you name target instances with `--instance`. If it doesn't, the command goes directly to the instance named by `--host`.

An instance refuses `canvas install`, `canvas uninstall`, `canvas enable`, `canvas disable`, and `canvas config set` requests made directly against a plugin that Canvas Platform manages on it. Publish new code for that plugin with `canvas deploy`, and change its variables or remove it with `--instance` while signed in.

`canvas deploy`, `canvas init`, and `canvas clone` set up the plugin's repository so that git signs in to Canvas Platform's git server through the CLI. You don't need a separate git password.

**Example:**

```console
$ canvas login
$ canvas init                                   # scaffolds acme__my_cool_plugin and registers it
$ canvas deploy my-cool-plugin/acme__my_cool_plugin --instance acme-staging
$ canvas config set acme__my_cool_plugin API_URL=https://api.example.com --instance acme-staging
```

### Moving from `credentials.ini` to Canvas Platform

Installing plugins directly on an instance with `credentials.ini` and `canvas install` is deprecated in favor of deploying through Canvas Platform. It isn't supported as of December 14, 2026. Until then, both ways work side by side on the same machine. `canvas install` prints a deprecation warning each time it runs, and other commands print a notice about the change to standard error at most once a day.

To move a plugin to Canvas Platform:

1. Run `canvas login`. It lists the prefix of each organization you belong to.
2. Rename the plugin to `<org prefix>__<package>`. Update the manifest `name`, the package folder, and the package's own imports. See [Plugin names](#plugin-names).
3. Deploy the renamed plugin with `canvas deploy <plugin dir> --instance <instance>`.
4. Set its variables with `canvas config set <name> KEY=VALUE --instance <instance>`.
5. Remove the plugin installed under the old name. The renamed plugin is a separate plugin, so the old one keeps running until you remove it:

   ```console
   $ canvas disable <old name> --host <instance>
   $ canvas uninstall <old name> --host <instance>
   ```

### Using a service account in CI

A CI system, such as GitHub Actions, can run the CLI against Canvas Platform without anyone signing in. Create a service account token on the Canvas Platform **Credentials** page and store it as a CI secret. Expose the secret to the job as the `CANVAS_PLATFORM_TOKEN` environment variable. To target a platform other than `https://platform.canvasmedical.com`, also set `CANVAS_PLATFORM_URL`.

When `CANVAS_PLATFORM_TOKEN` is set, every command uses the service account, even on a machine where someone previously ran `canvas login`. The token doesn't expire or refresh. If Canvas Platform rejects it, the token was probably rotated or revoked on the **Credentials** page; create a new one and update the CI secret.

Without a terminal, `canvas deploy` can't prompt you:

- Commit your changes before deploying, or pass `--yes` to commit them with a default message. Otherwise, deploy refuses to push uncommitted changes.
- Deploy can't answer consent requests for cross-plugin custom data access. A deployment that needs consent lists the requests with the deployment ID and exits with a non-zero status. Answer them from a terminal.

**Example:**

{% raw %}
```yaml
- name: Deploy plugin
  env:
    CANVAS_PLATFORM_TOKEN: ${{ secrets.CANVAS_PLATFORM_TOKEN }}
  run: canvas deploy acme__intake --instance acme-staging --yes
```
{% endraw %}

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
- `install`: Install a plugin into a Canvas instance
- `uninstall`: Uninstall a plugin
- `enable`: Enable a plugin from a Canvas instance
- `disable`: Disable a plugin from a Canvas instance
- `list`: List all plugins from a Canvas instance
- `validate`: Validate a plugin's manifest and that all handlers load in the sandbox
- `validate-manifest`: Validate the Canvas Manifest json file
- `logs`: Listen and print log streams from a Canvas instance
- `config list`: List plugin variables on a Canvas instance
- `config set`: Set plugin variables
- `config unset`: Clear plugin variable values

### `canvas login`

Sign in to Canvas Platform through your browser. The CLI also prints the sign-in URL, so you can finish signing in on another device when the machine has no browser. See [Canvas Platform](#canvas-platform).

**Usage**:

```console
$ canvas login [OPTIONS]
```

**Options**:

- `--platform TEXT`: Canvas Platform URL. Defaults to `CANVAS_PLATFORM_URL`, then the platform you last signed in to, then `https://platform.canvasmedical.com`.
- `--help`: Show this message and exit.

### `canvas logout`

Sign out of Canvas Platform. This revokes the machine's session and deletes its stored tokens.

**Usage**:

```console
$ canvas logout [OPTIONS]
```

**Options**:

- `--platform TEXT`: Canvas Platform URL
- `--help`: Show this message and exit.

### `canvas init`

Create a new plugin.

When you're signed in to Canvas Platform, the CLI names the package `<org prefix>__<package>` and registers the plugin. It also creates a git repository whose `origin` remote is Canvas Platform. When you're signed out, the plugin is named from the project name you enter and isn't registered.

**Usage**:

```console
$ canvas init [OPTIONS] [PLUGIN_TYPE]
```

**Arguments**:

- `PLUGIN_TYPE`: The type of plugin to create, `handler` or `application`. Defaults to `handler`.

**Options**:

- `--org TEXT`: The organization that publishes the plugin, when you can publish in more than one. Without it, the CLI asks you to choose.
- `--help`: Show this message and exit.

### `canvas deploy`

Publish a plugin's code to Canvas Platform and deploy it to one or more instances.

The manifest `name` must be [publisher-prefixed](#plugin-names). By default, deploy:

1. Registers the plugin with Canvas Platform, if it isn't registered yet.
2. Points the repository's `origin` remote at Canvas Platform. If the plugin isn't in a git repository yet, deploy offers to create one.
3. Commits uncommitted changes after you confirm.
4. Pushes `HEAD` to `main` and deploys that commit.
5. Waits for the result on each instance and exits with a non-zero status unless the deployment succeeds on every one.

To update the plugin's code and its catalog listing on Canvas Platform without deploying it to any instance, pass `--push-only`. Deploy registers the plugin and pushes `HEAD` to `main` the same way, then stops and prints the `canvas deploy --ref` command that deploys the pushed commit. A publisher with no instance of its own, or a CI job, can use it to keep a plugin's listing current.

The repository must be rooted at the directory that contains the plugin package. If the package is nested deeper in a larger repository, move it into its own repository or check it out with [`canvas clone`](#canvas-clone).

If the deployment needs consent for cross-plugin custom data access, deploy shows each request and asks you to answer it. Under `--yes`, or without a terminal, deploy lists the requests and exits with a non-zero status without answering them.

**Usage**:

```console
$ canvas deploy [OPTIONS] PLUGIN_DIR
```

**Arguments**:

- `PLUGIN_DIR`: Path to the plugin package to deploy [required]

**Options**:

- `--instance TEXT`: Instance to deploy to. Repeat it to deploy to several instances. Without it, deploy targets the only instance you can deploy to, or lists the choices when there are several.
- `--ref TEXT`: Deploy a branch, tag, or commit that's already pushed, without pushing.
- `--no-push`: Deploy the pushed `main` branch as-is, without pushing `HEAD` first.
- `--push-only`: Push `HEAD` to `main` without deploying it to any instance. Can't be combined with `--instance`, `--ref`, or `--no-push`.
- `-y, --yes`: Commit uncommitted changes without prompting, using a default commit message. This doesn't approve consent requests.
- `--help`: Show this message and exit.

### `canvas clone`

Clone a plugin's repository from Canvas Platform, with `origin` and git sign-in already set up so you can run `canvas deploy`.

**Usage**:

```console
$ canvas clone [OPTIONS] NAME [DIRECTORY]
```

**Arguments**:

- `NAME`: Name of the plugin to clone, such as `acme__intake` [required]
- `DIRECTORY`: Where to clone it. Defaults to a directory named after the plugin.

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

`canvas install` uploads the plugin to the instance directly. This is deprecated and isn't supported as of December 14, 2026, so the command prints a deprecation warning each time it runs. Use [`canvas deploy`](#canvas-deploy) to publish plugins through Canvas Platform instead. See [Moving from `credentials.ini` to Canvas Platform](#moving-from-credentialsini-to-canvas-platform).

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

Uninstall a plugin.

For a plugin Canvas Platform manages, an uninstall deployment removes it from each instance you name with `--instance`, which is required. For any other plugin, the CLI removes it from the instance directly. See [Which plugins go through Canvas Platform](#which-plugins-go-through-canvas-platform).

**Usage**:

```console
$ canvas uninstall [OPTIONS] NAME
```

**Arguments**:

- `NAME`: Plugin name to uninstall [required]

**Options**:

- `--instance TEXT`: Instance to uninstall from. Repeat it to uninstall from several instances.
- `--force`: Uninstall an enabled plugin from an instance directly
- `--host TEXT`: Canvas instance to connect to, for a plugin Canvas Platform doesn't manage
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

Set or update one or more plugin variables. Pass one or more `KEY=value` pairs as positional arguments.

For a plugin Canvas Platform manages, the CLI stores the values in Canvas Platform, and a configure deployment applies them to the running plugin. Without `--instance`, the command targets the only instance the plugin is installed on that you can configure. An instance where the plugin isn't installed yet receives the stored values when the plugin is next deployed there.

For any other plugin, the CLI writes the values to the instance directly, and each variable must already be declared in the plugin's `CANVAS_MANIFEST.json`.

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

- `--instance TEXT`: Instance to configure, for a plugin Canvas Platform manages. Repeat it to configure several instances.
- `--secret TEXT`: For a plugin Canvas Platform manages, set a variable that no revision of the manifest declares, as sensitive, e.g. Key=value. Repeatable.
- `--variable TEXT`: For a plugin Canvas Platform manages, set a variable that no revision of the manifest declares, as non-sensitive, e.g. Key=value. Repeatable.
- `--host TEXT`: Canvas instance to connect to, for a plugin Canvas Platform doesn't manage
- `--help`: Show this message and exit.

> Whether each value is treated as sensitive is determined by the plugin's `CANVAS_MANIFEST.json` (`variables: [{name, sensitive}]`) — `canvas config set` does not change the sensitive flag of a declared variable.

### `canvas config unset`

Clear one or more plugin variable values.

For a plugin Canvas Platform manages, the CLI clears the values in Canvas Platform, and a configure deployment removes them from the running plugin. Without `--instance`, the command targets the only instance the plugin is installed on that you can configure. For any other plugin, the CLI sets each value to empty on the instance directly.

**Usage**:

```console
$ canvas config unset [OPTIONS] PLUGIN KEYS...
```

**Example**:

```console
$ canvas config unset acme__intake API_TOKEN --instance acme-staging
```

**Arguments**:

 - `PLUGIN`: Plugin name to clear variables for
 - `KEYS...`: Variable keys to clear, e.g. API_TOKEN

**Options**:

- `--instance TEXT`: Instance to configure, for a plugin Canvas Platform manages. Repeat it to configure several instances.
- `--host TEXT`: Canvas instance to connect to, for a plugin Canvas Platform doesn't manage
- `--help`: Show this message and exit.
