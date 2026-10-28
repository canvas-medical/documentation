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

`canvas install` prints a deprecation warning on every run, and at most once a day any command, `canvas install` included, reminds you about the change.

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

`canvas login` lists each organization you belong to and its plugin prefix. The prefix you choose for a plugin decides which organization publishes it. Later, `canvas whoami` shows the same list, along with the platform the CLI is using and what you can do in each organization.

### 2. Rename the plugin with the prefix

Rename the plugin to `<org prefix>__<package>` in three places:

- the manifest `name`: `"name": "acme__intake"`
- the package folder: `intake/` becomes `acme__intake/`. `canvas deploy` refuses a folder that does not match the manifest `name`, before it commits or pushes anything
- every import and class path that names the package, including the handler and application paths in `CANVAS_MANIFEST.json`: `intake.handlers.events:Handler` becomes `acme__intake.handlers.events:Handler`

If the plugin declares [`custom_data`](/sdk/canvas_manifest/#custom-data):

- Leave its `namespace` as it is, so the renamed plugin reads and writes the same tables.
- Remove `namespace_read_access_key` and `namespace_read_write_access_key` from the manifest's `variables`. Canvas Platform holds each namespace's keys and sends them to every plugin entitled to them, and it refuses a manifest that declares them.
- Before the first deploy, Canvas Platform needs the keys of a namespace that already exists on the instance. Until it has them, `canvas deploy` stops with a message that the instance already has the namespace. Send the instance name, the namespace name, and both keys (the old plugin holds them as secrets) to your Canvas team through the Canvas Platform Support Form, a support ticket, or a 1Password share, and they record them with Canvas Platform. Never send the keys by email or Slack: they grant access to custom data that can hold PHI.

See [Custom data on Canvas Platform](/sdk/custom-data-sharing-data/#custom-data-on-canvas-platform) for how plugins share a namespace.

If the plugin has [SimpleAPI](/sdk/handlers-simple-api-http/) routes, their URLs change with the name. An instance sends each request under `/plugin-io/api/<plugin name>/` only to the plugin with that exact name, so `/plugin-io/api/intake/...` becomes `/plugin-io/api/acme__intake/...`. The old path has no alias or redirect. Before you switch an instance over:

- Update every URL in the plugin's own code that includes the old name, such as application and modal URLs, links in rendered HTML, and calls from front-end JavaScript.
- Plan when external systems that call the plugin, such as webhooks and partner integrations, switch to the new path. The old path stops answering when step 5 disables the old plugin, and the new path answers once the renamed plugin is deployed, so neither path answers between those two commands.

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

If the plugin already has its own repository on GitHub or elsewhere, rename that remote before the first deploy. `canvas deploy` points the repository's `origin` remote at Canvas Platform, replacing whatever `origin` pointed to:

```console
$ git remote rename origin github
```

Your existing repository stays reachable as `github`, and `origin` becomes the plugin's repository on Canvas Platform.

### 4. Push the code and store its variables

Push the code without deploying it, so Canvas Platform knows the plugin:

```console
$ canvas deploy intake-plugin/acme__intake --push-only
Pushed acme__intake 5d768a166204 to main on Canvas Platform.
To install this commit on an instance: canvas deploy intake-plugin/acme__intake --ref 5d768a166204
```

The last line is the command that would install this commit; step 5 deploys the plugin once its variables are stored.

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

`canvas deploy` waits up to 300 seconds for each instance's outcome and exits non-zero unless every instance succeeds in that time.

{% include alert.html type="warning" content="<b>Uninstalling the old plugin deletes its banner alerts.</b> Banners on patient charts and claims belong to the plugin that added them. They're hidden while the old plugin is disabled, and <code>canvas uninstall</code> deletes them. To keep them, have the renamed plugin read the old plugin's banners with <a href='/sdk/data-banner-alert/'><code>BannerAlert</code></a> or <a href='/sdk/data-claim/#claimbanneralert'><code>ClaimBannerAlert</code></a>, filtered on <code>plugin_name='intake'</code> and <code>status='active'</code>, and add them again with <a href='/sdk/effect-banner-alerts/'><code>AddBannerAlert</code></a> or <a href='/sdk/effect-claims/#add-banner'><code>ClaimEffect.add_banner()</code></a> before you uninstall the old plugin." %}

{% include alert.html type="info" content="<b>Protocol cards aren't deleted, but they stop showing.</b> A patient's chart shows only <a href='/sdk/effect-protocol-cards/'>protocol cards</a> from enabled plugins, so the old plugin's cards disappear when you disable it. Uninstalling it leaves them hidden. The renamed plugin's cards appear as it adds them." %}

Repeat steps 4 and 5 for each instance that runs the plugin. From now on, ship changes with `canvas deploy`.

## Move CI

CI/CD pipelines are supported through service accounts. A service account belongs to your organization rather than to a person, so a pipeline keeps deploying when the person who set it up leaves, and Canvas Platform's audit log names the account behind each deploy. An Organization admin, Plugin developer or Deploy manager creates one on the Credentials page in Canvas Platform. An Organization admin can give it both the Plugin developer and Deploy manager roles the pipeline needs; a Plugin developer or Deploy manager can give only the roles they hold. Its token is shown once and lasts a year; store it as a CI secret, expose it as `CANVAS_PLATFORM_TOKEN`, and delete the instance's `client_id` and `client_secret` from CI:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
- run: pip install canvas
- run: canvas deploy intake-plugin/acme__intake --instance acme-staging --yes
  env:
    CANVAS_PLATFORM_TOKEN: {% raw %}${{ secrets.CANVAS_PLATFORM_TOKEN }}{% endraw %}
```

`fetch-depth: 0` checks out the full history, which the push to Canvas Platform needs. That push is not forced, so it is refused when Canvas Platform's `main` has a commit the pipeline's checkout lacks, such as one a developer deployed from their machine without pushing it to the repository the pipeline checks out. Once a pipeline deploys a plugin, deploy it only from the pipeline.

`--yes` commits any uncommitted changes with the default message. A deploy that needs consent for custom data access exits non-zero and lists the requests, so answer those from a terminal. [Service accounts for CI/CD](/sdk/canvas_cli/#service-accounts-for-cicd) covers rotating and revoking the token.

## Other machines and teammates

Each developer runs `canvas login` once on their own machine. A teammate who has not worked on the plugin yet gets a ready-to-deploy checkout with [`canvas clone`](/sdk/canvas_cli/#canvas-clone):

```console
$ canvas clone acme__intake
```

Keep `~/.canvas/credentials.ini` until `canvas logs`, `list`, `enable`, `disable`, `config list` and the `namespace` commands also sign in through Canvas Platform, because they authenticate with it today. [Instance API credentials](/sdk/canvas_cli/#instance-api-credentials-credentialsini-deprecated) lists which commands still use it. Once none do, delete the file and revoke the OAuth clients it named on each instance.
