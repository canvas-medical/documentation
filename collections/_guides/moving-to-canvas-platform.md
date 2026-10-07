---
title: "Moving to Canvas Platform"
guide_for:
- /sdk/canvas_cli/
- /sdk/canvas_manifest/
---

The Canvas CLI signs in to [Canvas Platform](https://platform.canvasmedical.com) with `canvas login` and ships plugins with `canvas deploy`. Canvas Platform hosts each plugin's git repository, deploys a pushed commit to the instances your organization manages, and stores each instance's plugin variables.

{% include alert.html type="warning" content="<b>Support for <code>credentials.ini</code> and <code>canvas install</code> ends on December 14, 2026.</b> After that date the Canvas CLI authenticates only through Canvas Platform, and plugins reach an instance only through <code>canvas deploy</code>. Move each plugin over before then using the steps below." %}

## What changes

| Task | Deprecated | Current |
| --- | --- | --- |
| Sign in | An OAuth client per instance, saved in `~/.canvas/credentials.ini` | `canvas login` once per machine, in your browser |
| Sign in from CI | An instance's `client_id` and `client_secret` as CI secrets | A service account token as `CANVAS_PLATFORM_TOKEN` |
| Ship code | `canvas install <dir> --host <instance>` uploads a package | `canvas deploy <package dir> --instance <instance>` pushes a git commit and deploys it |
| Plugin name | Any name | `<org prefix>__<package>`, such as `acme__intake` |
| Set variables | `canvas install --secret` / `--variable`, or `canvas config set --host` | `canvas config set <name> KEY=VALUE --instance <instance>` |
| Uninstall | `canvas uninstall <name> --host <instance>` | `canvas uninstall <name> --instance <instance>` |
| Code history | Whatever was last uploaded | Every pushed commit, in the plugin's repository on Canvas Platform |

`canvas install` prints a deprecation warning on every run, and every other command reminds you about the change once a day.

## Before you start

- Upgrade the Canvas CLI: `pip install --upgrade canvas`, or `uv tool upgrade canvas`.
- Install git. Canvas Platform hosts each plugin as a git repository.
- Get the roles you need in your Canvas Platform organization. Pushing plugin code needs the **Plugin developer** role; deploying, configuring and uninstalling need **Deploy manager**. An **Organization admin** grants them.

## Move a plugin

The steps below move a plugin named `intake` to the organization whose prefix is `acme`, on the instance `acme-staging`.

### 1. Sign in

```console
$ canvas login
Signed in to https://platform.canvasmedical.com as you@example.com.
  Acme Health (acme): plugin prefix acme__
```

`canvas login` lists each organization you belong to and its plugin prefix. The prefix you choose for a plugin decides which organization publishes it.

### 2. Rename the plugin with the prefix

Rename the plugin to `<org prefix>__<package>` in three places:

- the manifest `name`: `"name": "acme__intake"`
- the package folder: `intake/` becomes `acme__intake/`
- every import and class path that names the package, including the handler and application paths in `CANVAS_MANIFEST.json`: `intake.handlers.events:Handler` becomes `acme__intake.handlers.events:Handler`

If the plugin declares [`custom_data`](/sdk/canvas_manifest/#custom-data):

- Leave its `namespace` as it is, so the renamed plugin reads and writes the same tables.
- Remove `namespace_read_access_key` and `namespace_read_write_access_key` from the manifest's `variables`. Canvas Platform holds each namespace's keys and sends them to every plugin entitled to them, and it refuses a manifest that declares them.
- Before the first deploy, Canvas Platform needs the keys of a namespace that already exists on the instance. Until it has them, `canvas deploy` stops with a message that the instance already has the namespace. Send the instance name, the namespace name, and both keys (the old plugin holds them as secrets) to your Canvas team, who record them with Canvas Platform.

See [Custom data on Canvas Platform](/sdk/custom-data-sharing-data/#custom-data-on-canvas-platform) for how plugins share a namespace.

Then run [`canvas validate`](/sdk/canvas_cli/#canvas-validate) on the renamed package.

### 3. Give the plugin its own repository

Canvas Platform hosts one repository per plugin, rooted at the directory that contains the package:

```text
intake-plugin/            # repository root
├── acme__intake/
│   ├── CANVAS_MANIFEST.json
│   └── handlers/
├── pyproject.toml
└── tests/
```

If the package is not in a git repository yet, `canvas deploy` offers to create one at its parent directory. If the package sits inside a larger repository with other code, move it into a repository of its own first, since `deploy` refuses a package nested deeper than that. Add a `.gitignore` for virtual environments and local secrets, because the repository is what gets deployed.

### 4. Push the code and store its variables

Push the code without deploying it, so Canvas Platform knows the plugin:

```console
$ canvas deploy intake-plugin/acme__intake --push-only
```

Then store its variable values for the instance. The plugin is not installed there yet, so the values wait for the first deploy:

```console
$ canvas config set acme__intake API_URL=https://api.example.com API_TOKEN=abc123 --instance acme-staging
```

A variable's sensitivity comes from the manifest's [`variables`](/sdk/canvas_manifest/#variables) block. `canvas config list intake --host acme-staging` shows which variables the old plugin has set.

### 5. Switch the instance over

The renamed plugin is a separate plugin from the one installed under the old name, and both respond to the same events while both are enabled. Disable the old plugin, deploy the new one, then remove the old one once the new one is working:

```console
$ canvas disable intake --host acme-staging
$ canvas deploy intake-plugin/acme__intake --instance acme-staging
$ canvas uninstall intake --host acme-staging
```

`canvas deploy` waits for each instance's outcome and exits non-zero unless every instance succeeds.

Repeat steps 4 and 5 for each instance that runs the plugin. From now on, ship changes with `canvas deploy`.

## Move CI

A CI job signs in as a service account. An Organization admin, Plugin developer or Deploy manager creates one on the Credentials page in Canvas Platform. Its token is shown once and lasts a year; store it as a CI secret, expose it as `CANVAS_PLATFORM_TOKEN`, and delete the instance's `client_id` and `client_secret` from CI:

```yaml
- run: pip install canvas
- run: canvas deploy intake-plugin/acme__intake --instance acme-staging --yes
  env:
    CANVAS_PLATFORM_TOKEN: {% raw %}${{ secrets.CANVAS_PLATFORM_TOKEN }}{% endraw %}
```

`--yes` commits any uncommitted changes with the default message. A deploy that needs consent for custom data access exits non-zero and lists the requests, so answer those from a terminal.

## Other machines and teammates

Each developer runs `canvas login` once on their own machine. A teammate who has not worked on the plugin yet gets a ready-to-deploy checkout with [`canvas clone`](/sdk/canvas_cli/#canvas-clone):

```console
$ canvas clone acme__intake
```

After December 14, 2026, the CLI does not read `~/.canvas/credentials.ini`. Delete it then, and revoke the OAuth clients it named on each instance.
