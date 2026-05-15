---
title: "SSO Capabilities"
slug: "sso"
hidden: false
---

Canvas supports SAML 2.0 single sign-on, and exposes hooks that let plugins
participate in the post-login flow. Use these hooks to capture data from the
identity provider's SAML response, or to send a user to a custom landing page
after they authenticate.

Both hooks fire after the SAML assertion has been validated and the user has
been logged in. The user's identity is available as
[`self.event.actor`](/sdk/events/#event-actor); the SAML response data is
available in `self.event.context`.

## Hooks at a glance

| Hook | Type | Purpose |
|---|---|---|
| [`SSO__PROCESS_ADDITIONAL_REQUEST_DATA`](#sso__process_additional_request_data) | Event | Read-only access to the SAML response so a plugin can capture IdP attributes (group memberships, employee ID, etc.). |
| [`SSO__GET_POST_LOGIN_REDIRECT`](#sso__get_post_login_redirect) | Event | Override the URL the user lands on after SSO login. |
| [`REDIRECT_CONTEXT`](#redirect_context) | Effect | The effect returned from `SSO__GET_POST_LOGIN_REDIRECT` to set the post-login destination. |

## `SSO__PROCESS_ADDITIONAL_REQUEST_DATA`

Fires once per successful SAML login, immediately after the user is
authenticated. The event is **read-only**: any effects a handler returns are
discarded. Use it for side-effects such as syncing IdP attributes onto a
[`Staff`](/sdk/data-staff/) record, writing an audit log, or notifying an
external system that a user signed in.

### Context

| Key | Type | Description |
|---|---|---|
| `session_info` | dict | The validated SAML response data from pysaml2. Common keys include `name_id` (the SAML NameID), `issuer` (IdP entity ID), `ava` (a dict of IdP-supplied user attributes keyed by attribute name with list-valued entries), `session_index`, `not_on_or_after`, and `authn_info`. |

### Target

The Canvas user that just logged in. `self.event.target` resolves to a
[`Staff`](/sdk/data-staff/) or [`Patient`](/sdk/data-patient/) via
`self.event.actor.instance.person_subclass`.

### Example

```python
import json

from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler
from logger import log


class CaptureSSOAttributes(BaseHandler):
    """Log the IdP-supplied group memberships for every SSO login."""

    RESPONDS_TO = EventType.Name(EventType.SSO__PROCESS_ADDITIONAL_REQUEST_DATA)

    def compute(self):
        session_info = json.loads(self.event.context)["session_info"]
        groups = session_info.get("ava", {}).get("groups", [])
        log.info(f"SSO login for {session_info['name_id']} with groups={groups}")
        return []
```

## `SSO__GET_POST_LOGIN_REDIRECT`

Fires once per successful SAML login, right before Canvas decides where to
send the user. A plugin that returns a [`REDIRECT_CONTEXT`](#redirect_context)
effect sets the destination URL; if no plugin returns one (or the value is
falsy), Canvas falls back to its default post-login redirect.

Only the first `REDIRECT_CONTEXT` effect returned is used. If multiple plugins
register a handler, ordering between them is not guaranteed — coordinate
across plugins to avoid conflicting redirects.

### Context

| Key | Type | Description |
|---|---|---|
| `relay_state` | str | The SAML `RelayState` value from the original login request, if any. Often used by IdPs to encode a "deep link" — the URL the user was trying to reach before they were bounced to the IdP. |
| `session_info` | dict | Same shape as for `SSO__PROCESS_ADDITIONAL_REQUEST_DATA`. |

### Target

Same as `SSO__PROCESS_ADDITIONAL_REQUEST_DATA` — the Canvas user that just
logged in.

### Example

```python
import json

from canvas_generated.messages.effects_pb2 import EffectType
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from canvas_sdk.handlers.base import BaseHandler


class RouteSSOByGroup(BaseHandler):
    """Send admins to the admin app and everyone else to the inbox."""

    RESPONDS_TO = EventType.Name(EventType.SSO__GET_POST_LOGIN_REDIRECT)

    def compute(self):
        session_info = json.loads(self.event.context)["session_info"]
        groups = session_info.get("ava", {}).get("groups", [])

        if "canvas-admins" in groups:
            url = "/admin/"
        else:
            url = "/inbox/"

        return [
            Effect(
                type=EffectType.REDIRECT_CONTEXT,
                payload=json.dumps({"url": url}),
            )
        ]
```

## `REDIRECT_CONTEXT`

The effect that carries the post-login URL back to Canvas. It is only
meaningful when returned from a `SSO__GET_POST_LOGIN_REDIRECT` handler.

### Payload

| Key | Type | Description |
|---|---|---|
| `url` | str | The URL Canvas should redirect the user to after SSO login. Relative paths (e.g. `/inbox/`) and absolute URLs are both accepted. |

There is no SDK helper class for this effect — construct it directly with
`Effect(type=EffectType.REDIRECT_CONTEXT, payload=json.dumps({"url": ...}))`
as shown in the example above.
