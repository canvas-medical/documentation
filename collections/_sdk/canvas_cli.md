---
title: "Canvas CLI"
---

## Getting Started

### Installation

To install the Canvas CLI, simply `pip install canvas`. Python 3.11 or 3.12 is required.

### Configuration and Authenticating to Your Canvas Instance
Create a file `~/.canvas/credentials.ini` with sections for each of your Canvas instance subdomains, and add client_id and client_secret credentials to each section. For example, if your Canvas instance url is `https://buttered-popcorn.canvasmedical.com/`, you would have a section `[buttered-popcorn]` with key-value pairs for `client_id` and `client_secret`.

{% include alert.html type="info" content= "<b>Getting Credentials: </b>Learn how to get register a client_id and client_secret <a href='/api/customer-authentication/#registering-a-third-party-application-on-canvas'>here</a>.<br/>The Canvas CLI uses OAuth, just like the FHIR API."  %}

**Example:**

```
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
- `list`: List all plugins from a Canvas instance
- `validate-manifest`: Validate the Canvas Manifest json file
- `logs`: Listen and print log streams from a Canvas instance

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

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.

### `canvas uninstall`

Uninstall a plugin from a Canvas instance.

**Usage**:

```console
$ canvas uninstall [OPTIONS] NAME
```

**Arguments**:

- `NAME`: Plugin name to delete [required]

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

Subscribes to a log stream and prints to your console.

**Usage**:

```console
$ canvas logs [OPTIONS]
```

**Options**:

- `--host TEXT`: Canvas instance to connect to
- `--help`: Show this message and exit.
