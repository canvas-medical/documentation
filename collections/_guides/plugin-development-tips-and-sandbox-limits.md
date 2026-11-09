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

```python?partial=true
from logger import log

# inside a handler method
log.info(f"Handler fired for note {self.event.context.get('note')}")
```

If a handler fails to load (for example, an import error at install time), only that handler is skipped — other handlers in the same plugin keep running — so check the logs for load-time errors as well as runtime ones. The exception is a helper module whose functions contain code the sandbox refuses. Then none of the plugin's handlers load, as [Helper modules](/sdk/sandboxing-and-allowed-imports/#helper-modules) describes.

## Deployment does not require IP whitelisting

Deploying plugins does **not** require any IP allowlisting. You only need the correct OAuth authentication, as described in [Your First Plugin](/guides/your-first-plugin/#2-configure-the-canvas-cli-for-your-instances) and [customer authentication](/api/customer-authentication/).

## Sharing code between modules in a plugin

A plugin can import its own modules. If you have several handlers that do nearly the same thing, factor the shared logic into a base class and import it by its full path from the plugin package (here the plugin package is `my_plugin`):

```python?partial=true
# my_plugin/protocols/base.py
from canvas_sdk.handlers import BaseHandler


class SharedBase(BaseHandler):
    def shared_helper(self):
        ...
```

```python?partial=true
# my_plugin/protocols/my_handler.py
from my_plugin.protocols.base import SharedBase


class MyHandler(SharedBase):
    ...
```

Relative imports such as `from .base import SharedBase` work too. They resolve against the importing module's package, and one that reaches above your plugin package raises `ImportError`. The allowed-imports list applies to third-party and standard-library modules; any module inside your own plugin package is importable.

## Time zones: use `zoneinfo.ZoneInfo`

`zoneinfo.ZoneInfo` is allowlisted in the sandbox, so it is the recommended way to handle time zones:

```python
from zoneinfo import ZoneInfo

TIME_ZONE = "US/Eastern"
TZ = ZoneInfo(TIME_ZONE)
```

## Calling AWS services without Boto3 (e.g. SNS for reminders)

The Boto3 library is not available in the sandbox, but you can still call AWS HTTP APIs directly. For example, to build custom branded email/SMS reminders you can publish to Amazon SNS with a normal HTTP request to the region's SNS endpoint:

```text
https://sns.us-east-2.amazonaws.com/?Action=Publish
&TopicArn=arn%3Aaws%3Asns%3Aus-east-2%3A698519295917%3AMy-Topic
&Subject=My%20first%20message
&Message=Hello%20world%21
&Version=2010-03-31
&AUTHPARAMS
```

(See the [AWS SNS Publish API docs](https://docs.aws.amazon.com/sns/latest/api/API_Publish.html).)

These requests must be signed with [AWS Signature Version 4](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv.html). You can build the signature inside a plugin because `hmac.new` and `hashlib.sha256` are both allowed imports; [this open-source implementation](https://github.com/andrewjroth/requests-auth-aws-sigv4/blob/master/requests_auth_aws_sigv4/__init__.py) shows how. Make the requests with the [`Http`](/sdk/utils/) util and keep your AWS credentials in [secrets](/sdk/secrets/). This is more manual than using Boto3, but it lets you avoid hosting and maintaining a separate proxy service for the AWS calls.

A typical reminders setup is a [CronTask](/sdk/handlers-crontask/) that runs on a schedule, builds the list of appointments needing reminders, and sends the notifications (directly to SNS as above, or to your own endpoint).

## Emails and texts on non-production instances

On an instance that isn't a production instance, Canvas doesn't deliver the emails and text messages it sends itself unless the recipient is on an allow list. That covers portal invites and login links, patient message notifications, appointment reminders, and lab result notifications. Anything else is logged instead of sent, and the UI still shows it as sent, so a portal invite can show **Invite sent** even though no email went out.

- **Email:** addresses ending in `@canvasmedical.com` are always delivered. To receive email at any other address, add it to the organization setting named `emailAddressAllowList`.
- **Text messages:** add the number to the organization setting named `phoneNumberAllowList`.

Each setting's value is a JSON list. An entry has to match the destination exactly, so use the email address or phone number as it appears on the patient's profile (phone numbers as 10 digits):

```json
["test.patient@example.com", "developer@example.com"]
```

```json
["5555550100"]
```

If the setting doesn't exist on the instance yet, create it under the organization's settings with that exact name. After you save it, resend the invite or message. Messages that a plugin delivers through its own provider, such as a link from [`get_login_url`](/sdk/utils/#getting-a-patient-portal-login-link) sent over your own SMS or email account, don't go through these allow lists.

### Allow list changes can take up to an hour to apply everywhere

Each Canvas server process caches organization settings in memory for up to an hour. Saving a setting clears the cache only in the process that handled the save, so other processes, including the ones that apply effects from scheduled tasks and other handlers, can keep reading the previous allow list for up to an hour. During that window a send to a newly added address can still be skipped, while a send handled by a process with a fresh cache goes out. Add test addresses and numbers well before you test with them, or wait an hour after editing the list.

### Telling a skipped send from a delivered one

When the email address or phone number isn't on the allow list, the send is counted as successful. For a patient message, the [`MessageTransmission`](/sdk/data-message/) is still stamped `delivered` and `failed` stays empty, so the transmission alone doesn't show whether the email or text left Canvas. `delivered_by` is only set when a staff member relays a message manually, so it's empty for every automated email or text.

To check a skipped send, compare the transmission's `contact_point_value` with the allow list entries (the match is exact and case-sensitive), and compare the transmission's `created` time with when the allow list was last saved. A transmission created within an hour of an allow list change may have been checked against the earlier list.

## Sandbox restrictions on dict reads and writes

The sandbox routes item access and assignment through internal `_safe_getitem` and `_safe_write` checks. Ordinary lookup errors pass straight through them, so a traceback for a missing key or an empty list names the guard even though the cause is your data:

```text
File ".../sandbox.py", in _safe_getitem
    return ob[index]
KeyError: 0
```

Guard your lookups rather than indexing blindly:

- Read optional keys with `.get(...)` and provide defaults instead of `ob[key]`, so a missing key does not raise.
- Confirm a collection is non-empty before indexing into it (`ob[0]`).

The guards also raise their own `AttributeError`s for a few patterns:

- Dictionaries accept item keys that start with `_`. Other objects may not, such as one of your own classes that implements `__getitem__`. Reading `obj["_private"]` from one raises `"_private" is an invalid item name because it starts with "_"`.
- Some writes to an object that does not come from your plugin raise `Forbidden assignment to a non-module attribute: ...`. These are overwriting an attribute or item that holds a callable, and setting an attribute on something you imported (`SomeImportedClass.attr = ...`).
