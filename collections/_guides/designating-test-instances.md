---
title: "Designating Test Instances"
guide_for:
- /sdk/canvas_cli/
---

A test instance is an instance where your organization can deploy plugin code that isn't on `main` yet. Canvas Platform deploys a commit that isn't on a plugin's `main` only to your organization's test instances, so a branch can be tried on a test instance before it is merged, while every other instance runs only merged code.

Your organization's Studio instance is always a test instance. A Deploy manager or Organization admin chooses the others in Canvas Platform.

{% include alert.html type="info" content="<b>Help Center:</b> the step-by-step article for Deploy managers and Organization admins is <a href='https://help.canvasmedical.com/articles/4724162094-designating-test-instances'>Designating test instances</a>." %}

## Designate a test instance

You need the **Deploy manager** or **Organization admin** role in the instance's organization. For a practice under an MSO, that is the practice's own organization.

Production instances and instances that hold patient data aren't eligible. The switch's tooltip explains why one can't be changed.

1. In [Canvas Platform](https://platform.canvasmedical.com), open **Canvas Instances** and click the instance.
2. Click the **Plugin management** tab.
3. Under **Testing**, turn on **Designate as test instance**, then click **Make test instance** to confirm.

![The Plugin management tab of testing-instance, with Designate as test instance turned on](/assets/images/guides/designating-test-instances/plugin-management-tab.png){:width="100%"}

A flask marks each test instance beside its name and in the **All instances** table.

![The All instances table, with a flask beside testing-instance and testing-instance-1](/assets/images/guides/designating-test-instances/all-instances.png){:width="100%"}

To remove one, turn the switch off and click **Remove**. Commits that aren't on `main` can no longer be deployed there, and the plugins already installed on the instance stay as they are. Every addition and removal is recorded in your organization's audit log.

## Deploy a branch to a test instance

Deploy a branch with [`canvas deploy --branch`](/sdk/canvas_cli/#canvas-deploy):

```console
$ canvas deploy paperwork-eviscerator/acme__paperwork_eviscerator --branch try-new-intake --instance acme-staging
```

The same rule applies everywhere a build ships: `canvas deploy --ref`, installs from the Plugin Catalog, and promotions all deploy a commit that isn't on `main` only to test instances.

When an instance you name isn't a test instance, nothing is deployed, and `deploy` exits non-zero with a message naming your organization's test instances:

```text
acme__paperwork_eviscerator at 3f2a9c1e7b04 isn't on main, so it deploys only to your organization's test instances (acme-dev, acme-studio), and acme-prod isn't one. It can be deployed to acme-prod once it is on main.
```

When the instance could be a test instance, the message adds who can add it and where. When your organization has no test instances, the message says so and names who can make one. Merge the change to `main` to deploy it to any other instance.

### Deploy a branch that's already on Canvas Platform

To deploy a branch someone else pushed, name it with [`canvas deploy --ref`](/sdk/canvas_cli/#canvas-deploy). Canvas Platform looks the branch up in the plugin's repository, so it doesn't need to be in your local clone, and nothing is pushed. `deploy` reads only the plugin's name and publisher from the folder you give it, so any checkout of the plugin works, such as one from [`canvas clone`](/sdk/canvas_cli/#canvas-clone).

Canvas Studio keeps a project's work in progress on the `canvas-studio` branch, so you can deploy it to any of your organization's test instances:

```console
$ canvas deploy paperwork-eviscerator/acme__paperwork_eviscerator --ref canvas-studio --instance acme-staging
```

`--ref` also takes a tag or a full commit SHA.
