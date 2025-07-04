---
title: "Sandboxing and Allowed Imports"
---

Plugins developed with the Canvas SDK execute safely and securely in a sandbox that restricts access to the host operating system, filesystem, and database. This precaution reduces the likelihood of accidents or malicious use of the platform that might put patient data at risk.

## Standard Library Modules

The following Python standard library modules and their allowed imports are available within the sandbox:

### `__future__`
- `annotations`

### `base64`
- `b64decode`
- `b64encode`

### `collections`
- `Counter`
- `defaultdict`

### `datetime`
- `date`
- `datetime`
- `timedelta`
- `timezone`
- `UTC`

### `dateutil`
- `relativedelta`

### `dateutil.relativedelta`
- `relativedelta`

### `decimal`
- `Decimal`

### `enum`
- `Enum`
- `StrEnum`

### `functools`
- `reduce`

### `hashlib`
- `sha256`

### `hmac`
- `compare_digest`
- `new`

### `http`
- `HTTPStatus`

### `json`
- `dumps`
- `loads`

### `operator`
- `and_`

### `random`
- `choices`
- `uniform`
- `randint`

### `re`
- `compile`
- `DOTALL`
- `IGNORECASE`
- `match`
- `search`
- `split`
- `sub`

### `string`
- `ascii_lowercase`
- `digits`

### `time`
- `time`
- `sleep`

### `typing`
- `Any`
- `cast`
- `Dict`
- `Final`
- `Iterable`
- `List`
- `NamedTuple`
- `NotRequired`
- `Protocol`
- `Sequence`
- `Tuple`
- `Type`
- `TypedDict`

### `urllib`
- `parse`

### `urllib.parse`
- `urlencode`
- `quote`

### `uuid`
- `uuid4`
- `UUID`

### `zoneinfo`
- `ZoneInfo`

## Third-Party Modules

The following third-party modules and their allowed imports are available within the sandbox:

### `arrow`
- `get`
- `now`
- `utcnow`

### `django.db.models`
- `BigIntegerField`
- `Case`
- `CharField`
- `IntegerField`
- `Model`
- `Q`
- `Value`
- `When`

### `django.db.models.expressions`
- `Case`
- `Value`
- `When`

### `django.db.models.query`
- `QuerySet`

### `django.utils.functional`
- `cached_property`

### `jwt`
- `decode`
- `encode`

### `pydantic`
- `ValidationError`

### `rapidfuzz`
- `fuzz`
- `process`
- `utils`

### `requests`
- `delete`
- `get`
- `patch`
- `post`
- `put`
- `request`
- `RequestException`
- `Response`

## Canvas SDK Modules

All Canvas SDK modules are available for import and use within your plugins:

- `canvas_sdk.caching`
- `canvas_sdk.commands`
- `canvas_sdk.effects`
- `canvas_sdk.events`
- `canvas_sdk.handlers`
- `canvas_sdk.protocols`
- `canvas_sdk.questionnaires`
- `canvas_sdk.templates`
- `canvas_sdk.utils`
- `canvas_sdk.v1`
- `canvas_sdk.value_set`
- `canvas_sdk.views`
- `logger`

## Builtin Functions

The following Python builtin functions are available within the sandbox:

- `all`
- `any`
- `classmethod`
- `dict`
- `enumerate`
- `filter`
- `hasattr`
- `iter`
- `list`
- `map`
- `max`
- `min`
- `next`
- `property`
- `reversed`
- `staticmethod`
- `super`
- `vars`

Plus all the standard safe builtins from RestrictedPython including basic types (`bool`, `int`, `float`, `str`, `tuple`, etc.) and safe operations.

## Requesting Additional Imports

If there is a library or function not on this list that you wish to import in your plugin, reach out to your Canvas support team with the request or visit the [Canvas developer forum](https://github.com/canvas-medical/canvas-plugins/discussions). Additional imports can often be added after a security review.

The allowed imports are defined in the [Canvas Plugins repository](https://github.com/canvas-medical/canvas-plugins/blob/main/plugin_runner/sandbox.py) and are regularly updated to support common development needs while maintaining security.