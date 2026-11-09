---
title: "Working with a Monorepo"
guide_for:
- /sdk/canvas_cli/
---

Canvas manages plugin code as one git repository per plugin. Canvas Platform hosts that repository, `canvas init` creates its local copy with `origin` pointing at Canvas Platform, and `canvas deploy` pushes your commits to it, so the repository you work in and the plugin's repository on Canvas Platform share one history.

That works well for a team that develops each plugin on its own. Other teams keep many plugins in one repository, often a monorepo beside shared code and services, and review and release them through that repository. A plain `canvas deploy` refuses a package inside such a repository, because it would push the whole repository as the plugin and point the repository's `origin` at Canvas Platform.

`canvas deploy --snapshot` is for that case. It publishes each plugin from where it sits, and your repository stays the source of truth. Canvas Platform still keeps one repository per plugin: each snapshot of a changed package adds one commit to that plugin's `main` holding the package folder as committed in your repository, and a snapshot of an unchanged package pushes nothing.

## Lay out each plugin

Each plugin's package folder, the folder holding `CANVAS_MANIFEST.json`, can sit anywhere in your repository. Give it the same name as the manifest `name`. Existing plugins keep the names they have. Signed in with `canvas login`, `canvas init` names a new plugin with your organization's prefix, `<org prefix>__<package>`:

```text
your-repo/
├── plugins/
│   ├── acme__intake/              # package folder: this is what a snapshot ships
│   │   ├── CANVAS_MANIFEST.json
│   │   └── handlers/
│   └── referrals/
│       ├── acme__referrals/       # package folder
│       └── tests/                 # stays in your repository
└── services/                      # stays in your repository
```

A snapshot ships only the package folder. Tests, other plugins and the rest of your repository never reach Canvas Platform. The manifest `name` decides which Canvas Platform repository a snapshot goes to, so every checkout and pipeline that deploys a plugin deploys to the same place.

## Deploy from your machine

Sign in once with `canvas login`, commit your changes, and pass the path to the package folder:

```console
$ canvas deploy plugins/acme__intake --snapshot --instance acme-staging
```

`deploy` builds one commit on top of the plugin's `main` on Canvas Platform, pushes it from a temporary repository, and deploys it. Your repository's `origin`, git config and index are never changed. Uncommitted changes in the package are refused rather than committed. Add `--push-only` to publish the code and its [catalog listing](/sdk/canvas_manifest/#catalog) without deploying to an instance.

## Deploy from CI

A pipeline signs in as a [service account](/sdk/canvas_cli/#service-accounts-for-cicd): create one on the Credentials page in Canvas Platform, store its token as a CI secret, and expose it as `CANVAS_PLATFORM_TOKEN`. A snapshot needs no git identity on the runner. Check out full history without file contents, as below: the check that stops a deploy from rolling the plugin back needs the commit `main` was last deployed from, and a shallow checkout usually lacks it, so `deploy` skips that check there and says so. This GitHub Actions workflow deploys one plugin whenever a change to it merges:

```yaml
on:
  push:
    branches: [main]
    paths: ["plugins/acme__intake/**"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          filter: blob:none
      - run: pip install canvas
      - run: canvas deploy plugins/acme__intake --snapshot --instance acme-staging
        env:
          CANVAS_PLATFORM_TOKEN: {% raw %}${{ secrets.CANVAS_PLATFORM_TOKEN }}{% endraw %}
```

The commit on Canvas Platform is authored as the service account, and its message names the commit and path it came from (`Monorepo-Commit` and `Monorepo-Path`). Give each plugin its own job, or loop over the plugins a merge changed.

## With Canvas Studio and gated release

When your organization builds plugins in Canvas Studio with gated release pointed at your repository, Studio's work reaches your release instances only through your repository's review:

<div style="text-align: center; margin: 1.5rem 0;">
<svg viewBox="0 0 830 480" role="img" aria-labelledby="mr-flow-title mr-flow-desc" style="width: 100%; max-width: 830px; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <title id="mr-flow-title">Gated release from Canvas Studio through a monorepo</title>
  <desc id="mr-flow-desc">Lanes for your repository, Canvas Studio, Canvas Platform with its canvas-studio and main branches, the test instance, and your release instances. 1. Studio pushes work in progress to canvas-studio and deploys it to the test instance. 2. Promoting opens a pull request in your repository; Studio writes Canvas Platform's main only to create it, with a base commit and no project code, when a project starts. 3. Your engineers review and merge it. 4. CI or an engineer runs canvas deploy with --snapshot, which adds one commit to main and deploys it to your release instances. 5. When the project opens and before each deploy, Studio brings new commits on main and canvas-studio into the project.</desc>
  <defs>
    <marker id="mr-a-push" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#2563eb"/></marker>
    <marker id="mr-a-deploy" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#15803d"/></marker>
    <marker id="mr-a-merge" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#7c3aed"/></marker>
    <marker id="mr-a-cli" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#0e7490"/></marker>
  </defs>
<g font-size="11" fill="#1e293b">
<rect x="130" y="10" width="150" height="460" rx="10" fill="#eff6ff" stroke="#bfdbfe"/>
<text x="205" y="32" text-anchor="middle" font-size="12.5" font-weight="600">Your repository</text>
<rect x="292" y="10" width="120" height="460" rx="10" fill="#f5f3ff" stroke="#ddd6fe"/>
<text x="352" y="32" text-anchor="middle" font-size="12.5" font-weight="600">Canvas Studio</text>
<rect x="424" y="10" width="220" height="460" rx="10" fill="#f0fdf4" stroke="#bbf7d0"/>
<text x="534" y="32" text-anchor="middle" font-size="12.5" font-weight="600">Canvas Platform</text>
<rect x="656" y="10" width="80" height="460" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>
<text x="696" y="32" text-anchor="middle" font-size="12.5" font-weight="600">Test</text>
<text x="696" y="47" text-anchor="middle" font-size="12.5" font-weight="600">instance</text>
<rect x="748" y="10" width="80" height="460" rx="10" fill="#fff7ed" stroke="#fed7aa"/>
<text x="788" y="32" text-anchor="middle" font-size="12.5" font-weight="600">Release</text>
<text x="788" y="47" text-anchor="middle" font-size="12.5" font-weight="600">instances</text>
<rect x="138" y="56" width="61" height="18" rx="9" fill="#ffffff" stroke="#cbd5e1"/>
<text x="168" y="69" text-anchor="middle" font-family="SFMono-Regular, Menlo, monospace">PR / MR</text>
<line x1="168" y1="78" x2="168" y2="462" stroke="#94a3b8" stroke-width="2.5"/>
<rect x="222" y="56" width="41" height="18" rx="9" fill="#ffffff" stroke="#cbd5e1"/>
<text x="242" y="69" text-anchor="middle" font-family="SFMono-Regular, Menlo, monospace">main</text>
<line x1="242" y1="78" x2="242" y2="462" stroke="#94a3b8" stroke-width="2.5"/>
<rect x="301" y="56" width="101" height="18" rx="9" fill="#ffffff" stroke="#cbd5e1"/>
<text x="352" y="69" text-anchor="middle" font-family="SFMono-Regular, Menlo, monospace">canvas-studio</text>
<line x1="352" y1="78" x2="352" y2="462" stroke="#94a3b8" stroke-width="2.5"/>
<rect x="433" y="56" width="101" height="18" rx="9" fill="#ffffff" stroke="#cbd5e1"/>
<text x="484" y="69" text-anchor="middle" font-family="SFMono-Regular, Menlo, monospace">canvas-studio</text>
<line x1="484" y1="78" x2="484" y2="462" stroke="#94a3b8" stroke-width="2.5"/>
<rect x="570" y="56" width="41" height="18" rx="9" fill="#ffffff" stroke="#cbd5e1"/>
<text x="590" y="69" text-anchor="middle" font-family="SFMono-Regular, Menlo, monospace">main</text>
<line x1="590" y1="78" x2="590" y2="462" stroke="#94a3b8" stroke-width="2.5"/>
<line x1="696" y1="56" x2="696" y2="462" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="2 5"/>
<line x1="788" y1="56" x2="788" y2="462" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="2 5"/>
<text x="6" y="124" font-size="11.5" font-weight="600">1. Build and test</text>
<text x="6" y="196" font-size="11.5" font-weight="600">2. Pull request</text>
<text x="6" y="261" font-size="11.5" font-weight="600">3. Review</text>
<text x="19" y="276" font-size="11.5" font-weight="600">and merge</text>
<text x="6" y="340" font-size="11.5" font-weight="600">4. Snapshot</text>
<text x="6" y="405" font-size="11.5" font-weight="600">5. Studio brings</text>
<text x="19" y="420" font-size="11.5" font-weight="600">it in</text>
<line x1="352" y1="120" x2="476" y2="120" stroke="#2563eb" stroke-width="2.5" marker-end="url(#mr-a-push)"/>
<circle cx="352" cy="120" r="4" fill="#2563eb"/>
<rect x="400" y="99" width="36" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="418" y="111" text-anchor="middle">push</text>
<line x1="484" y1="120" x2="688" y2="120" stroke="#15803d" stroke-width="2.5" marker-end="url(#mr-a-deploy)"/>
<circle cx="484" cy="120" r="4" fill="#15803d"/>
<rect x="566" y="99" width="49" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="590" y="111" text-anchor="middle">deploy</text>
<line x1="352" y1="192" x2="176" y2="192" stroke="#2563eb" stroke-width="2.5" marker-end="url(#mr-a-push)"/>
<circle cx="352" cy="192" r="4" fill="#2563eb"/>
<rect x="193" y="171" width="134" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="260" y="183" text-anchor="middle">opens a pull request</text>
<line x1="352" y1="192" x2="580" y2="192" stroke="#dc2626" stroke-width="2" stroke-dasharray="6 5"/>
<circle cx="590" cy="192" r="9" fill="#fef2f2" stroke="#dc2626" stroke-width="1.8"/>
<path d="M586,188 L594,196 M594,188 L586,196" stroke="#dc2626" stroke-width="2"/>
<rect x="395" y="171" width="152" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="471" y="183" text-anchor="middle">no project code to main</text>
<line x1="168" y1="264" x2="234" y2="264" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#mr-a-merge)"/>
<circle cx="168" cy="264" r="4" fill="#7c3aed"/>
<rect x="184" y="243" width="42" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="205" y="255" text-anchor="middle">merge</text>
<line x1="242" y1="336" x2="582" y2="336" stroke="#0e7490" stroke-width="2.5" marker-end="url(#mr-a-cli)"/>
<circle cx="242" cy="336" r="4" fill="#0e7490"/>
<rect x="330" y="315" width="173" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="416" y="327" text-anchor="middle" font-family="SFMono-Regular, Menlo, monospace">canvas deploy --snapshot</text>
<line x1="590" y1="336" x2="780" y2="336" stroke="#15803d" stroke-width="2.5" marker-end="url(#mr-a-deploy)"/>
<circle cx="590" cy="336" r="4" fill="#15803d"/>
<rect x="665" y="315" width="49" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="689" y="327" text-anchor="middle">deploy</text>
<line x1="590" y1="408" x2="360" y2="408" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#mr-a-merge)"/>
<circle cx="590" cy="408" r="4" fill="#7c3aed"/>
<circle cx="484" cy="408" r="4" fill="#7c3aed"/>
<rect x="352" y="387" width="238" height="17" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
<text x="471" y="399" text-anchor="middle">new commits on main and canvas-studio</text>
</g>
</svg>
</div>

1. **Build and test.** Studio users build the plugin and test it on the Studio test instance. Studio keeps this work in progress on the `canvas-studio` branch of the plugin's Canvas Platform repository.
2. **Pull request.** Promoting from Studio's Final Review opens a pull request in your repository (on GitLab, a merge request) that writes the plugin into its folder there. Studio writes the plugin's `main` on Canvas Platform only to create it, with a base commit and no project code, when a project starts. Project code reaches `main` only through review and action by someone at your organization.
3. **Review and merge.** Your engineers review it like any other change. They can approve it as it is, push edits to its branch, or change the plugin after merging.
4. **Snapshot.** Once it merges, CI or an engineer runs `canvas deploy <package folder> --snapshot`. The package folder is the one holding `CANVAS_MANIFEST.json` inside the folder Studio's pull request writes. Canvas Platform's `main` gets one commit with the plugin exactly as merged, and it deploys to the instances you name.
5. **Studio brings it in.** When a Studio project opens, and before any deploy from it, Studio brings in new commits on Canvas Platform's `main` and `canvas-studio` that it has not synced yet. Your engineers' edits become the starting point of the next iteration within Studio, and are never overwritten by it.

Because Studio reads both branches, your engineers can work with Studio users directly on iterative changes: push work in progress to `canvas-studio` with `canvas deploy <package folder> --snapshot --branch canvas-studio`, and the Studio project brings it in similarly.

For the same flow as Studio users see it, share the Canvas help center's [Gated release: from Promote to Production](https://help.canvasmedical.com/articles/7597495196-studio-admin-guide-setting-up-gated-release) and [When code changes outside Studio](https://help.canvasmedical.com/articles/4485157203-when-code-changes-outside-studio).

## When a snapshot stops

`deploy --snapshot` exits non-zero without pushing when:

- **The package has uncommitted changes**, or holds a git submodule, a symbolic link, or a file stored through a git filter such as Git LFS or git-crypt. Commit the changes, or replace those entries with regular files.
- **HEAD lacks changes `main` was last deployed with.** `deploy` lists the package files that the last deployed commit changed and HEAD does not, since deploying would roll them back. Update the checkout, for example with `git pull`, and deploy again. A branch that was deployed and then squash- or rebase-merged does not stop here, because HEAD carries its changes.
- **`main` on Canvas Platform has changes the snapshot would replace**, such as an edit to the plugin's catalog listing made in Canvas Platform. `deploy` lists the files. To keep the changes, `canvas clone` the plugin, copy its versions of those files into your repository, commit them, and deploy again. To replace them, run the deploy at a terminal and confirm.

The [`canvas deploy` reference](/sdk/canvas_cli/#deploying-from-a-larger-repository) covers each case in full.
