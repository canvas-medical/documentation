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
- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

**Notes**:

Files can be excluded from the packaged plugin using a `.canvasignore` in the current working directory. The file behaves similarly to [.gitignore](https://git-scm.com/docs/gitignore)

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
-  `--page-size INTEGER`:  Fetch size per page (historical).  \[default: 200]
-  `--limit INTEGER`:      Max historical logs to print.
-  `--all`:                Fetch all pages until exhausted (historical).
-  `--interactive`:        After each page, prompt to load more.
-  `--cursor TEXT`:        Resume token from a previous run.
-  `--help`:               Show this message and exit.


### `canvas config list`

List plugin variables on a Canvas instance. Variables display as `[set]` or `[not set]` to indicate whether a value has been configured. Actual values are never shown through the CLI for security reasons. To view variable values, use the Django admin interface (requires managing user permissions).

**Usage**:

```console
$ canvas config list [OPTIONS] PLUGIN
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

Set plugin variables on a Canvas instance.

**Usage**:

```console
$ canvas config set [OPTIONS] PLUGIN VARIABLES...
```

**Arguments**:

 - `PLUGIN`:  Plugin name to set variables for
 - `VARIABLES...`: Variables to set, e.g. Key=value

**Options**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.
