---
title: "Plugin Development Tips and Sandbox Limits"
guide_for:
- /sdk/canvas_cli/
- /sdk/utils/
- /sdk/secrets/
---

<!-- sources: discussions #924, #804, #741, #928, #584, #573 -->

Canvas plugins run inside a restricted Python sandbox, which shapes what you can import and how you can manipulate data. This guide collects practical tips for building, deploying, and troubleshooting plugins, plus the sandbox behaviors that most commonly trip people up.

## Troubleshooting: is my code actually deployed?

Before debugging logic, confirm the code running on the instance is the code you think it is:

1. **Save and deploy your edits.** Editing a file locally does nothing until you push it to the instance with the [Canvas CLI](/sdk/canvas_cli/). Re-deploy after every change you want to test.
2. **Verify through the logs.** Stream the instance logs with `canvas logs` and add `log.info(...)` statements to confirm your handler is firing and to inspect the values it sees. If you do not see your log lines, the event you expect is not reaching your handler, or the plugin did not load.

```python
from logger import log

log.info(f"Handler fired for note {self.context.get('note')}")
```

If a handler fails to load (for example, an import error at install time), only that handler is skipped — other handlers in the same plugin keep running — so check the logs for load-time errors as well as runtime ones.

## Deployment does not require IP whitelisting

Deploying plugins does **not** require any IP allowlisting. You only need the correct OAuth authentication, as described in [Your First Plugin](/guides/your-first-plugin/#2-configure-the-canvas-cli-for-your-instances) and [customer authentication](/api/customer-authentication/).

IP allowlisting is only relevant for **read-replica database access**. If your team needs that, [file a support ticket](https://portal.usepylon.com/canvas-medical/forms/standard) and the Canvas team will set it up.

## Relative imports within a plugin

Relative imports are allowed *within a single plugin*. If you have several handlers that do nearly the same thing, factor the shared logic into a base class and import it:

```python
# protocols/base.py
from canvas_sdk.handlers import BaseHandler


class SharedBase(BaseHandler):
    def shared_helper(self):
        ...
```

```python
# protocols/my_handler.py
from .base import SharedBase


class MyHandler(SharedBase):
    ...
```

This lets you share a base handler class across the protocols in one plugin. (Note that the sandbox still enforces the allowed-imports list for third-party and standard-library modules — relative imports between your own plugin files are what is permitted here.)

## Time zones: use `zoneinfo.ZoneInfo`

`zoneinfo.ZoneInfo` is allowlisted in the sandbox, so it is the recommended way to handle time zones:

```python
from zoneinfo import ZoneInfo

TIME_ZONE = "US/Eastern"
TZ = ZoneInfo(TIME_ZONE)
```

(Early on, `ZoneInfo` was not allowlisted and raised `ImportError: 'zoneinfo' is not an allowed import.`; it has since been added, so prefer it over workarounds.)

## Calling AWS services without Boto3 (e.g. SNS for reminders)

The Boto3 library is not available in the sandbox, but you can still call AWS HTTP APIs directly. For example, to build custom branded email/SMS reminders you can publish to Amazon SNS with a normal HTTP request to the region's SNS endpoint:

```
https://sns.us-east-2.amazonaws.com/?Action=Publish
&TopicArn=arn%3Aaws%3Asns%3Aus-east-2%3A698519295917%3AMy-Topic
&Subject=My%20first%20message
&Message=Hello%20world%21
&Version=2010-03-31
&AUTHPARAMS
```

(See the [AWS SNS Publish API docs](https://docs.aws.amazon.com/sns/latest/api/API_Publish.html).)

These requests must be signed with [AWS Signature Version 4](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html). You can build the signature inside a plugin because `hmac.new` and `hashlib.sha256` are both allowed imports; [this open-source implementation](https://github.com/andrewjroth/requests-auth-aws-sigv4/blob/master/requests_auth_aws_sigv4/__init__.py) shows how. Make the requests with the [`Http`](/sdk/utils/) util and keep your AWS credentials in [secrets](/sdk/secrets/). This is more manual than using Boto3, but it lets you avoid hosting and maintaining a separate proxy service for the AWS calls.

A typical reminders setup is a [CronTask](/sdk/handlers-cron/) that runs on a schedule, builds the list of appointments needing reminders, and sends the notifications (directly to SNS as above, or to your own endpoint).

## Sandbox restrictions on dict reads and writes

The sandbox wraps item access and assignment with internal `_safe_getitem` and `_safe_write` checks. In normal use these are transparent, but they explain occasional errors you may see in the logs around dictionary access — for example reading a key that is not present, or writing to an object the guard does not recognize:

```
File ".../sandbox.py", line 690, in _safe_getitem
    return ob[index]
KeyError: 0
```

```
File ".../sandbox.py", line 668, in _safe_write
    full_name = f"{_ob.__module__}.{_ob.__class__.__qualname__}"
AttributeError: 'dict' object has no attribute '__module__'
```

To stay on the supported path, guard your lookups rather than indexing blindly:

- Read optional keys with `.get(...)` and provide defaults instead of `ob[key]`, so a missing key does not raise.
- Confirm a collection is non-empty before indexing into it (`ob[0]`).

If previously working code suddenly starts raising these errors after a platform update, it may indicate the sandbox briefly tightened more than intended; report it through a support ticket so the team can confirm and, if needed, release a fix.
