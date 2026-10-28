---
title: "Upgrading to Canvas Platform"
redirect_from:
  - /guides/moving-to-canvas-platform/
guide_for:
- /sdk/canvas_cli/
- /sdk/canvas_manifest/
---

Canvas is upgrading how plugins are authenticated and deployed. For your developers, the upgrade comes down to two changes to the commands they already run:

- **Sign in with `canvas login`** instead of keeping instance credentials in `~/.canvas/credentials.ini`.
- **Ship plugins with `canvas deploy`** instead of `canvas install`.

Automated pipelines make the same switch, signing in with a service account token. Your plugins keep their names, their code, their variables, their SimpleAPI URLs and their custom data. Canvas handles the rest of the upgrade.

{% include alert.html type="info" content="<b><code>canvas install</code> and <code>credentials.ini</code> keep working until December 14, 2026.</b> Switch your development workflow and CI to <code>canvas login</code> and <code>canvas deploy</code> before then." %}

{% include alert.html type="info" content="<b>This guide replaces an earlier version.</b> From October 16 to October 28, 2026, this page described a more complicated upgrade. We've worked hard to simplify it. Common questions are answered in the <a href='#faqs'>FAQs</a> section below." %}

## Why the change

`canvas login` signs each developer in with their own Canvas Platform identity instead of a client secret shared per instance. Your organization manages who has access centrally in Canvas Platform, with options for single sign-on (SSO) through your identity provider, SCIM (automatic provisioning and deprovisioning of users from your identity provider), and SIEM (sending audit events to your security monitoring system). When someone leaves your organization, removing them in one place ends their access to every instance.

`canvas deploy` publishes each plugin's code to Canvas Platform before it reaches an instance, so every deploy is a recorded commit you can trace to the person or service account that made it. Roles in Canvas Platform decide who can push code and who can deploy it, and instance-specific credentials files go away entirely.

## Timeline

### 1. Join your organization on Canvas Platform

Most organizations have already received an invitation to join [Canvas Platform](https://platform.canvasmedical.com). If yours has not, ask your Canvas contact for an update.

The first person to join has the **Organization admin** role. They either:

- set up single sign-on according to your organization's policies, following [Set up single sign-on for Canvas Platform](https://help.canvasmedical.com/articles/9800510716-set-up-single-sign-on-for-canvas-platform?lang=en), or
- send email invitations to the people who need access, who then sign in with a password.

### 2. Grant roles

The Organization admin gives each person the roles their work needs. Developers typically need both:

- **Plugin developer**, to push plugin code to Canvas Platform
- **Deploy manager**, to deploy plugins to your instances and set their variables

### 3. Canvas upgrades your plugins

Canvas upgrades your organization's plugins to the platform-based Plugin Development Lifecycle. Your running plugins are not affected in any way: they keep running and handling events and requests throughout. Everyone in your organization with the Organization admin, Plugin developer or Deploy manager role is notified when the upgrade is complete.

### 4. Switch your workflow by December 14, 2026

Once your organization is upgraded, update your development workflow and your CI pipelines as described below. `canvas install` and `credentials.ini` keep working until December 14, 2026, so you can switch at your own pace before then.

## Update your development workflow

Upgrade the Canvas CLI to the latest version, with `pip install --upgrade canvas` or `uv tool upgrade canvas`. Then sign in once on each machine:

```console
$ canvas login
Signed in to https://platform.canvasmedical.com as you@example.com.
  Acme Health (acme): plugin prefix acme__
```

`canvas login` opens your browser, and uses your organization's single sign-on when it is set up. [`canvas whoami`](/sdk/canvas_cli/#canvas-whoami) shows who you are signed in as and what you can do in each organization.

Where you ran `canvas install`, run `canvas deploy` with the path to the plugin package, the folder that holds `CANVAS_MANIFEST.json`, and the instance to deploy to:

```console
$ canvas install intake --host acme-staging            # before
$ canvas deploy intake --instance acme-staging         # after
```

`canvas deploy` commits your changes, pushes the commit to the plugin's repository on Canvas Platform, deploys it, and waits for the instance to report the outcome. Its repository is rooted at the directory that holds the package, and `canvas deploy` points that repository's `origin` remote at Canvas Platform. If `origin` points at another host, such as GitHub, rename it first: `git remote rename origin github`. The [`canvas deploy` reference](/sdk/canvas_cli/#canvas-deploy) covers each step.

### Plugins in a monorepo

If your plugin lives in a subdirectory of a larger repository, such as a monorepo holding several plugins and other code, add `--snapshot`:

```console
$ canvas deploy plugins/intake --snapshot --instance acme-staging
```

A snapshot publishes the plugin's package folder as it is committed in your repository, and leaves your repository's remotes and configuration alone, so your repository stays the source of truth. It works the same from your machine and from CI. [Working with a monorepo](/guides/working-with-a-monorepo/) walks through the setup.

## Update your CI pipelines

A pipeline signs in with a [service account](/sdk/canvas_cli/#service-accounts-for-cicd) instead of an instance's `client_id` and `client_secret`. A service account belongs to your organization rather than to a person, so the pipeline keeps working when the person who set it up leaves, and Canvas Platform's audit log names the account behind each deploy.

1. On the Credentials page in Canvas Platform, create a service account and give it the Plugin developer and Deploy manager roles. An Organization admin can give it both; a Plugin developer or Deploy manager can give it only the roles they hold.
2. Copy its token, which is shown once and is valid for a year, into a secret in your CI system.
3. Expose the secret to the job as `CANVAS_PLATFORM_TOKEN` and replace `canvas install` with `canvas deploy`. The job needs no `canvas login` step.
4. Delete the instance's `client_id` and `client_secret` from your CI secrets.

A GitHub Actions job for a plugin with its own repository:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
- run: pip install canvas
- run: canvas deploy intake --instance acme-staging --yes
  env:
    CANVAS_PLATFORM_TOKEN: {% raw %}${{ secrets.CANVAS_PLATFORM_TOKEN }}{% endraw %}
```

`fetch-depth: 0` checks out the full history, which the push to Canvas Platform needs. A pipeline that deploys from a monorepo uses `--snapshot` instead and works from a shallow checkout; [Working with a monorepo](/guides/working-with-a-monorepo/#deploy-from-ci) has an example. [Service accounts for CI/CD](/sdk/canvas_cli/#service-accounts-for-cicd) covers rotating and revoking the token.

## FAQs

### Do we have to rename our plugins?

No. Your plugins keep the names they have today. Their SimpleAPI URLs stay the same, so the systems that call them need no changes, and banner alerts, protocol cards and other records your plugins created stay where they are.

### We already renamed plugins with our organization prefix. Do we need to undo that?

No. A plugin you renamed keeps working under its new name, and there is nothing to change back.

### Should new plugins use the organization prefix?

We recommend it. Signed in with `canvas login`, [`canvas init`](/sdk/canvas_cli/#canvas-init) names a new plugin with your organization's prefix, such as `acme__intake`, which it knows from your login. The prefix keeps your plugins' names distinct from plugins published by other organizations.

### Do we need to move our plugins into separate repositories?

No. A plugin in a monorepo deploys from where it is with `canvas deploy --snapshot`, from your machine or from CI. See [Plugins in a monorepo](#plugins-in-a-monorepo).

### Do we need to re-enter our plugins' variables and secrets?

No. Your plugins' variables and secrets carry over as they are.

### Does anything change for our custom data?

No. Your plugins keep reading and writing the same custom data, and Canvas handles the namespace access keys as part of the upgrade.

### How much work is this for our team?

Your Organization admin sets up access and roles in Canvas Platform. Each developer runs `canvas login` once per machine and uses `canvas deploy` where they used `canvas install`. Each pipeline gets a service account token and the same command change. Canvas handles every other part of the upgrade.

### Will our plugins stop working during the upgrade?

No. Your running plugins are not affected in any way. See [Canvas upgrades your plugins](#3-canvas-upgrades-your-plugins).

### Do we have to wait for the upgrade before we switch to `canvas deploy`?

Technically, no. We recommend waiting until you're notified that your organization has been upgraded to the platform-based Plugin Development Lifecycle, so your team has as little work to do as possible.

### Can we delete `credentials.ini` after we switch?

Yes. Every Canvas CLI command signs in through Canvas Platform, so once your development workflow and CI have switched, you can delete `~/.canvas/credentials.ini` and revoke the OAuth clients it named on each instance.
