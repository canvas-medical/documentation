# Getting Started with Plugins {#quickstart-plugins}

This quickstart guide will take you through the basic cycle of
developing your first Canvas plugin.

## Prerequisites

Before you begin, there are a few prerequisites that you will need to
have installed on your system:

-   Python 3.10 or later (we recommend using
    [pyenv](https://github.com/pyenv/pyenv))
-   The [Poetry package manager](https://python-poetry.org/)
-   Credentials for the Canvas PyPI mirror
-   An API key for your Canvas instance

## Step 1: Configure Poetry

Since we\'re using our private PyPI mirror, you need to configure poetry
to be able to access it.

In order to do that, you need to run:

``` console
$ poetry config http-basic.canvas-pypi read-only
```

And input the password when prompted

## Step 2: Install the Brush command-line tool

Brush is Canvas\' command-line tool that we\'ll use to manage the plugin
development lifecycle. You can install it with `pip`:

``` console
$ pip install --index-url https://pypicloud.canvasmedical.com/simple canvas-brush
```

Note that you may be prompted for the credentials to our internal PyPI
mirror, which you can get from Canvas Support.

## Step 3: Authenticate Brush to your Canvas instance

Next, we need to configure Brush with an API key so that it can manage
plugins on your Canvas instance.

``` console
$ brush auth add-api-key --host https://your-canvas-instance.canvasmedical.com --api-key your-api-key --is-default
```

## Step 4: Initialize a new plugin

Now that we\'re authenticated, we\'ll initialize a new plugin to develop
on.

``` console
# Navigate to your workspace (wherever you keep your projects)
$ cd /path/to/your/workspace

# Initialize the plugin and follow the prompts.
$ brush plugin init
full_name [Plugin Developer]: Jane Developer
email [developer@email.com]: jane@example.com
version [0.1.0]:
project_name [Plugin Boilerplate]: My Plugin
project_slug [my-plugin]:
project_package_name [my_plugin]:
project_short_description [A plugin to interact with a Canvas Instance]:
Project created in /path/to/your/workspace/my-plugin
```

## Step 5: Install the plugin

We can install the plugin into our Canvas instance by running:

``` console
$ brush plugin install ./my-plugin
Using python3 (3.11.0)
Creating virtualenv my-plugin-...
Building my-plugin (0.1.0)
Installing package: dist/my_plugin-0.1.0-py3-none-any.whl into https://your-canvas-instance.canvasmedical.com
Package successfully uploaded!

# `plugin install` accepts optional `--host` and `--api-key` arguments so you can specify an instance and its key to install a plugin:
# You can also pass a pre-built wheel (.whl) or compressed tarball (.tar.gz) file and Brush will skip building it
$ brush plugin install dist/my_plugin-0.1.0-py3-none-any.whl --host https://another-canvas-instance.canvasmedical.com --api-key your-instance-api-key
Installing package: dist/my_plugin-0.1.0-py3-none-any.whl into https://another-canvas-instance.canvasmedical.com
Package successfully uploaded!
```

## Step 6: Update the plugin

As you develop your plugin, you\'ll want to test your changes. You can
either use `brush plugin install` to update a plugin, or use
`brush plugin update` for extra options.

## Step 7: Manage the plugin

You can use `brush plugin update` to enable/disable a plugin, or even
update it\'s package.

If you want to update the plugin\'s status (enabled/disabled), or its
package, here\'s how you\'d do it:

``` console
$ poetry build
Using python3 (3.11.0)
Creating virtualenv my-plugin-...
Building my-plugin (0.1.0)

$ brush plugin update my-plugin --package dist/my_plugin-0.1.0-py3-none-any.whl
Update plugin my-plugin from https://your-canvas-instance.canvasmedical.com with is_enabled=None, package=PosixPath('dist/my_plugin-0.1.0-py3-none-any.whl')
Package successfully updated!
```

If your plugin is misbehaving and you\'re running into trouble, you can
disable it with:

``` console
$ brush plugin update my-plugin --disable
{
    "success": true,
    "message":
    {
        "name": "my-plugin",
        "description": "My plugin",
        "package": "https://canvas-client-media.s3.amazonaws.com/local/plugins/plugin/my_plugin-0.1.0-py3-none-any.whl.......",
        "package_checksum": "9420d3a041503f9d227516a675efd579bfya729fb0b9b60b353b4ec3dca9488d",
        "version": "0.1.0",
        "is_enabled": false
    },
    "status_code": 200
}

$ brush plugin update my-plugin --enable
{
    "success": true,
    "message":
    {
        "name": "my-plugin",
        "description": "My plugin",
        "package": "https://canvas-client-media.s3.amazonaws.com/local/plugins/plugin/my_plugin-0.1.0-py3-none-any.whl.......",
        "package_checksum": "9420d3a041503f9d227516a675efd579bfya729fb0b9b60b353b4ec3dca9488d",
        "version": "0.1.0",
        "is_enabled": true
    },
    "status_code": 200
}
```

## Step 7: Uninstall the plugin

Finally, you can remove your plugin from the instance entirely (e.g., if
you want to rename it) you can disable and uninstall it.

``` console
$ brush plugin update my-plugin --disable
{
    "success": true,
    "message":
    {
        "name": "my-plugin",
        "description": "My plugin",
        "package": "https://canvas-client-media.s3.amazonaws.com/local/plugins/plugin/my_plugin-0.1.0-py3-none-any.whl.......",
        "package_checksum": "9420d3a041503f9d227516a675efd579bfya729fb0b9b60b353b4ec3dca9488d",
        "version": "0.1.0",
        "is_enabled": false
    },
    "status_code": 200
}

$ brush plugin delete my-plugin
{"success": true, "status_code": 204}
```

## Bonus: Debug the plugin

Brush is also able to connect to your instance and stream all the logs.
This is helpful to debug any issues with your plugins, since breakpoints
aren\'t available. In order to do this, you only need to run:

``` console
$ brush logs
{"success": true, "message": "Connecting to the log stream. Please be patient as there may be a delay before log messages appear."}
{"success": true, "message": {"event": "GET /favicon.ico"}}
{"success": true, "message": {"event": "GET /host-information/?key=randomkey - 200"}}
```

And like everything else in `brush`, the command accepts optional
`--host` and `--api-key` arguments so you can specify an instance and
its api key.

Since everything is always streamed in json, you can pipe brush\' output
to `jq --stream` in order to indent the logs, or even to filter its
output:

``` console
# The following command will only show logs when its success is false
$ brush logs | jq --stream 'select(.success==false)'
```
