---
title: "Plugin Logs"
slug: "plugin-logs"
hidden: false
---

Canvas provides two ways to access **Plugin Logs**:

- **UI:** `https://<your-instance>.canvasmedical.com/admin/plugin-io` → **Logs**
- **CLI:** `canvas logs --help`

This guide explains how to open the UI view and how to use the CLI to filter, paginate, and (optionally) follow live logs.

---

### Plugin Logs in the Admin UI

From the Django Admin:

Navigation path:  
`Home` › `Plugin_IO` › **Plugin Logs**

The UI lets you:
- Filter by **source** (e.g., `plugin-runner`, `effect-interpreter`)
- Filter by **level** (`ERROR`, `WARN`, `INFO`, `DEBUG`)
- Filter by **plugin** — multi-select; the dropdown is pre-populated with plugins seen in the last 7 days, and accepts free-text entries for older or yet-to-log plugins
- Filter by **handler** — multi-select on the fully-qualified handler class; works the same as plugin (last 7 days + free-text)
- Filter by **time** (start/end)
- Inspect **full JSON** of a log entry in a modal
- **Load more** results without leaving the page

The results table shows columns for `@timestamp`, `level`, `source`, `plugin`, and `message`. Click a row to open the full log entry as JSON.

{% include alert.html type="info" content="The UI defaults to showing the most recent logs first (sorted by <code>@timestamp desc</code>)." %}

---

### CLI Overview

`canvas logs` now supports **historical lookback**, **filters**, **stateless pagination** with **cursors**, and **interactive paging**, all without breaking the original behavior.

- **Default (no flags)** → live stream (unchanged)
- **Add a time window** → fetch history (tail), then **follow** by default
- **Stop after history** → `--no-follow`
- **Page through large result sets** → `--limit`, `--page-size`, `--interactive`, or **cursor** tokens

Run `canvas logs --help` to see all options.


### Common Filters & Examples

##### Filter by source
```console
$ canvas logs --source plugin-runner
```

##### Filter by level (repeat flag)
```console
# Only errors:
$ canvas logs --level ERROR

# Errors and warnings:
$ canvas logs --level ERROR --level WARN
```

##### Filter by plugin / handler (repeatable)
```console
# One plugin:
$ canvas logs --plugin my_plugin

# Multiple plugins:
$ canvas logs --plugin my_plugin --plugin other_plugin

# A specific handler (fully qualified class name):
$ canvas logs --handler my_plugin.handlers.foo.MyHandler

# Multiple handlers:
$ canvas logs --handler my_plugin.handlers.foo.MyHandler --handler my_plugin.handlers.bar.OtherHandler
```

##### Time windows: since / start / end

**Relative lookback (`--since`)**  
Fetch the last 24 hours, then continue following:
```console
$ canvas logs --since 24h
```

**Absolute window (`--start/--end`)**  
Fetch a fixed window and stop:
```console
$ canvas logs --start "2025-09-12T10:00:00Z" --end "2025-09-12T12:00:00Z" --no-follow
```

{% include alert.html type="info" content="<code>--since</code> is mutually exclusive with <code>--start/--end</code>." %}

##### Combine filters
```console
# Errors from plugin-runner in the last 2 hours:
$ canvas logs --since 2h --level ERROR --source plugin-runner --no-follow
```

---

### Interactive Mode

Use `--interactive` in <b>historical</b> mode to page through results one page at a time:

```console
$ canvas logs --no-follow --since 24h --interactive
# Shows one page, prompts:
# Load more? [Y/n]
```

- The prompt repeats after each page.

---

### Stateless Paging with Cursors

When more results are available, the CLI prints a <b>resume command</b> with a <b>cursor token</b> (encodes the <code>search_after</code> and original filters). Re-run it to continue exactly where you left off:

```console
More available. To load the next page, run:
  canvas logs \
  --no-follow \
  --cursor <TOKEN>
```

{% include alert.html type="warning" content="<code>--cursor</code> is <b>mutually exclusive</b> with filters (<code>--since</code>, <code>--start/--end</code>, <code>--level</code>, <code>--source</code>, <code>--plugin</code>, <code>--handler</code>) to enforce consistency. Use the token alone to resume" %}.

---

### Limits & Page Size

- **`--page-size`**: how many logs to fetch per request (batching).  
  Default is optimized for typical usage.
- **`--limit`**: maximum number of logs to print **across pages**.

Examples:

```console
# One fixed page of size 200 (default page-size):
$ canvas logs --no-follow --since 24h

# Fetch up to 2000 logs across pages (non-interactive):
$ canvas logs --no-follow --since 72h --limit 2000

# Smaller batches for slow connections:
$ canvas logs --no-follow --since 24h --limit 1000 --page-size 100
```

{% include alert.html type="info" content="In non-interactive, no-limit mode, the CLI prints <b>one page</b>. Add <code>--limit</code>, <code>--interactive</code>, or <code>--all</code> to keep paging." %}

---

### No-Follow (Historical Only)

Add `--no-follow` to fetch **only** historical logs and exit:

```console
$ canvas logs --no-follow --since 24h
```


