---
title: "Working with a Monorepo"
guide_for:
- /sdk/canvas_cli/
---

If your plugins live in a repository with other code, such as a monorepo holding several plugins and services, `canvas deploy --snapshot` publishes each plugin from where it sits. Your repository stays the source of truth. Canvas Platform keeps one repository per plugin, and each snapshot of a changed package adds one commit to that plugin's `main` holding the package folder as committed in your repository. A snapshot of an unchanged package pushes nothing.

## Lay out each plugin

Each plugin's package folder, the folder holding `CANVAS_MANIFEST.json`, can sit anywhere in your repository. Name it after the plugin's publisher-prefixed name, `<org prefix>__<package>`, and use that name for the manifest `name` and the package's imports:

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

A snapshot ships only the package folder. Tests, other plugins and the rest of your repository never reach Canvas Platform. The manifest `name` decides which Canvas Platform repository a snapshot goes to, so rename plugins in one reviewed change before the first deploy, and every checkout and pipeline then deploys to the same place.

## Deploy from your machine

Sign in once with `canvas login`, commit your changes, and pass the path to the package folder:

```console
$ canvas deploy plugins/acme__intake --snapshot --instance acme-staging
```

`deploy` builds one commit on top of the plugin's `main` on Canvas Platform, pushes it from a temporary repository, and deploys it. Your repository's `origin`, git config and index are never changed. Uncommitted changes in the package are refused rather than committed. Add `--push-only` to publish the code and its [catalog listing](/sdk/canvas_manifest/#catalog) without deploying to an instance.

## Deploy from CI

A pipeline signs in as a [service account](/sdk/canvas_cli/#service-accounts-for-cicd): create one on the Credentials page in Canvas Platform, store its token as a CI secret, and expose it as `CANVAS_PLATFORM_TOKEN`. A snapshot works from a shallow checkout and needs no git identity on the runner. This GitHub Actions workflow deploys one plugin whenever a change to it merges:

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
      - run: pip install canvas
      - run: canvas deploy plugins/acme__intake --snapshot --instance acme-staging
        env:
          CANVAS_PLATFORM_TOKEN: {% raw %}${{ secrets.CANVAS_PLATFORM_TOKEN }}{% endraw %}
```

The commit on Canvas Platform is authored as the service account, and its message names the commit and path it came from (`Monorepo-Commit` and `Monorepo-Path`). Give each plugin its own job, or loop over the plugins a merge changed.

## With Canvas Studio and gated release

When your organization builds plugins in Canvas Studio with gated release pointed at your repository, Studio's work reaches your instances only through your repository's review:

<div style="text-align: center; margin: 1.5rem 0;">
<svg viewBox="0 0 760 440" role="img" aria-labelledby="mr-flow-title mr-flow-desc" style="width: 100%; max-width: 720px; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <title id="mr-flow-title">Gated release from Canvas Studio through a monorepo</title>
  <desc id="mr-flow-desc">1. Studio users build and test a plugin. 2. Publishing opens a pull request that writes the plugin into its folder in your repository. 3. Your engineers review it, edit it if needed, and merge it. 4. CI or an engineer runs canvas deploy with --snapshot, which adds one commit to the plugin's main on Canvas Platform and deploys it. 5. Studio brings the snapshot on main into the project, and the next iteration starts from it.</desc>
  <defs>
    <marker id="mr-arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6 Z" fill="#475569"/>
    </marker>
  </defs>
  <!-- lanes -->
  <rect x="15" y="12" width="210" height="416" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>
  <rect x="275" y="12" width="210" height="416" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>
  <rect x="535" y="12" width="210" height="416" rx="10" fill="#f8fafc" stroke="#e2e8f0"/>
  <g font-size="13" font-weight="600" fill="#0f172a" text-anchor="middle">
    <text x="120" y="40">Canvas Studio</text>
    <text x="380" y="40">Your repository</text>
    <text x="640" y="40">Canvas Platform</text>
  </g>
  <!-- arrows -->
  <g stroke="#475569" stroke-width="1.5" fill="none">
    <line x1="215" y1="124" x2="281" y2="124" marker-end="url(#mr-arrow)"/>
    <line x1="380" y1="164" x2="380" y2="200" marker-end="url(#mr-arrow)"/>
    <line x1="475" y1="244" x2="541" y2="244" marker-end="url(#mr-arrow)"/>
    <line x1="545" y1="278" x2="219" y2="352" stroke-dasharray="6 4" marker-end="url(#mr-arrow)"/>
    <line x1="120" y1="324" x2="120" y2="168" stroke-dasharray="6 4" marker-end="url(#mr-arrow)"/>
  </g>
  <g font-size="11" fill="#475569">
    <text x="248" y="116" text-anchor="middle">Publish</text>
    <text x="508" y="236" text-anchor="middle">--snapshot</text>
    <text x="640" y="304" text-anchor="middle">pushed by CI or an engineer</text>
    <text x="410" y="328" text-anchor="middle">reviewed code</text>
    <text x="128" y="250">next iteration</text>
  </g>
  <!-- 1 -->
  <rect x="25" y="84" width="190" height="80" rx="8" fill="#ede9fe" stroke="#c4b5fd"/>
  <text x="120" y="106" text-anchor="middle" font-size="12.5" font-weight="600" fill="#5b21b6">1 · Build and test</text>
  <text x="120" y="124" text-anchor="middle" font-size="11" fill="#6d28d9">work in progress stays on a</text>
  <text x="120" y="139" text-anchor="middle" font-size="11" fill="#6d28d9">development branch and the</text>
  <text x="120" y="154" text-anchor="middle" font-size="11" fill="#6d28d9">Studio test instance</text>
  <!-- 2 -->
  <rect x="285" y="84" width="190" height="80" rx="8" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="380" y="106" text-anchor="middle" font-size="12.5" font-weight="600" fill="#1e40af">2 · Pull request</text>
  <text x="380" y="124" text-anchor="middle" font-size="11" fill="#1d4ed8">Studio writes the plugin</text>
  <text x="380" y="139" text-anchor="middle" font-size="11" fill="#1d4ed8">into its folder in your repo</text>
  <text x="380" y="154" text-anchor="middle" font-size="11" fill="#1d4ed8">(GitLab: merge request)</text>
  <!-- 3 -->
  <rect x="285" y="204" width="190" height="80" rx="8" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="380" y="226" text-anchor="middle" font-size="12.5" font-weight="600" fill="#1e40af">3 · Review and merge</text>
  <text x="380" y="244" text-anchor="middle" font-size="11" fill="#1d4ed8">approve, push edits, or</text>
  <text x="380" y="259" text-anchor="middle" font-size="11" fill="#1d4ed8">change it after merging,</text>
  <text x="380" y="274" text-anchor="middle" font-size="11" fill="#1d4ed8">then merge to main</text>
  <!-- 4 -->
  <rect x="545" y="204" width="190" height="80" rx="8" fill="#dcfce7" stroke="#86efac"/>
  <text x="640" y="226" text-anchor="middle" font-size="12.5" font-weight="600" fill="#166534">4 · Snapshot on main</text>
  <text x="640" y="244" text-anchor="middle" font-size="11" fill="#15803d">one commit holding the</text>
  <text x="640" y="259" text-anchor="middle" font-size="11" fill="#15803d">package as merged, deployed</text>
  <text x="640" y="274" text-anchor="middle" font-size="11" fill="#15803d">to your instances</text>
  <!-- 5 -->
  <rect x="25" y="328" width="190" height="80" rx="8" fill="#ede9fe" stroke="#c4b5fd"/>
  <text x="120" y="350" text-anchor="middle" font-size="12.5" font-weight="600" fill="#5b21b6">5 · Studio picks it up</text>
  <text x="120" y="368" text-anchor="middle" font-size="11" fill="#6d28d9">brings the snapshot on</text>
  <text x="120" y="383" text-anchor="middle" font-size="11" fill="#6d28d9">main into the project, and</text>
  <text x="120" y="398" text-anchor="middle" font-size="11" fill="#6d28d9">the next iteration starts there</text>
</svg>
</div>

1. **Build and test.** Studio users build the plugin and test it on the Studio test instance. Studio keeps this work in progress on a development branch of the plugin's Canvas Platform repository, so the plugin's `main` holds only code that has been through your review.
2. **Pull request.** Publishing from Studio's Final Review opens a pull request in your repository (on GitLab, a merge request) that writes the plugin into its folder there.
3. **Review and merge.** Your engineers review it like any other change. They can approve it as it is, push edits to its branch, or change the plugin after merging.
4. **Snapshot.** Once it merges, CI or an engineer runs `canvas deploy <package folder> --snapshot`. The package folder is the one holding `CANVAS_MANIFEST.json` inside the folder Studio's pull request writes. Canvas Platform's `main` gets one commit with the plugin exactly as merged, and it deploys to the instances you name.
5. **Studio picks it up.** Studio brings the snapshot on Canvas Platform's `main` into the project, so your engineers' edits become the starting point of the next iteration instead of being overwritten by it.

## When a snapshot stops

`deploy --snapshot` exits non-zero without pushing when:

- **The package has uncommitted changes**, or holds a git submodule, a symbolic link or a Git LFS file. Commit the changes, or replace those entries with regular files.
- **HEAD is behind the last snapshot.** Update the checkout, for example with `git pull`, and deploy again.
- **`main` on Canvas Platform has changes the snapshot would replace**, such as an edit to the plugin's catalog listing made in Canvas Platform. `deploy` lists the files. To keep the changes, `canvas clone` the plugin, copy its versions of those files into your repository, commit them, and deploy again. To replace them, run the deploy at a terminal and confirm.

The [`canvas deploy` reference](/sdk/canvas_cli/#deploying-from-a-larger-repository) covers each case in full.
