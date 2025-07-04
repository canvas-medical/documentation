---
title: "Sandboxing and Allowed Imports"
---

Plugins developed with the Canvas SDK execute safely and securely in a sandbox that restricts access to the host operating system, filesystem, and database. This precaution reduces the likelihood of accidents or malicious use of the platform that might put patient data at risk.

## Standard Library Modules

The following Python standard library modules and their allowed imports are available within the sandbox:

##### `__future__`
Provides access to features from future Python versions for backwards compatibility. See the [Python __future__ documentation](https://docs.python.org/3/library/__future__.html) for more details.
- `annotations`

##### `base64`
Provides functions for encoding and decoding data in base64 format, commonly used for data transmission and storage. See the [Python base64 documentation](https://docs.python.org/3/library/base64.html) for more details.
- `b64decode`
- `b64encode`

##### `collections`
Provides specialized container datatypes that extend beyond the built-in types like lists and dictionaries. See the [Python collections documentation](https://docs.python.org/3/library/collections.html) for more details.
- `Counter`
- `defaultdict`

##### `datetime`
Provides classes for working with dates and times, essential for medical applications that need to track appointment schedules and patient timelines. See the [Python datetime documentation](https://docs.python.org/3/library/datetime.html) for more details.
- `date`
- `datetime`
- `timedelta`
- `timezone`
- `UTC`

##### `dateutil`
Extends Python's datetime capabilities with more flexible date parsing and arithmetic. See the [dateutil documentation](https://dateutil.readthedocs.io/en/stable/) for more details.
- `relativedelta`

##### `dateutil.relativedelta`
Provides relative time delta calculations for more complex date arithmetic operations. See the [dateutil.relativedelta documentation](https://dateutil.readthedocs.io/en/stable/relativedelta.html) for more details.
- `relativedelta`

##### `decimal`
Provides precise decimal arithmetic for financial and scientific calculations where floating-point accuracy is critical. See the [Python decimal documentation](https://docs.python.org/3/library/decimal.html) for more details.
- `Decimal`

##### `enum`
Provides support for enumerations, useful for defining sets of named constants such as status codes or categories. See the [Python enum documentation](https://docs.python.org/3/library/enum.html) for more details.
- `Enum`
- `StrEnum`

##### `functools`
Provides utilities for higher-order functions and operations on callable objects. See the [Python functools documentation](https://docs.python.org/3/library/functools.html) for more details.
- `reduce`

##### `hashlib`
Provides secure hash and message digest algorithms for data integrity verification and security purposes. See the [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html) for more details.
- `sha256`

##### `hmac`
Provides hash-based message authentication code (HMAC) functions for secure message authentication. See the [Python hmac documentation](https://docs.python.org/3/library/hmac.html) for more details.
- `compare_digest`
- `new`

##### `http`
Provides HTTP status codes and related constants for web API development and HTTP response handling. See the [Python http documentation](https://docs.python.org/3/library/http.html) for more details.
- `HTTPStatus`

##### `json`
Provides functions for parsing and generating JSON data, essential for API communication and data serialization. See the [Python json documentation](https://docs.python.org/3/library/json.html) for more details.
- `dumps`
- `loads`

##### `operator`
Provides function equivalents of operators for functional programming and complex data operations. See the [Python operator documentation](https://docs.python.org/3/library/operator.html) for more details.
- `and_`

##### `random`
Provides functions for generating random numbers and making random selections, useful for sampling and testing scenarios. See the [Python random documentation](https://docs.python.org/3/library/random.html) for more details.
- `choices`
- `uniform`
- `randint`

##### `re`
Provides regular expression matching operations for pattern matching and text processing. See the [Python re documentation](https://docs.python.org/3/library/re.html) for more details.
- `compile`
- `DOTALL`
- `IGNORECASE`
- `match`
- `search`
- `split`
- `sub`

##### `string`
Provides string constants and template classes for string manipulation and formatting operations. See the [Python string documentation](https://docs.python.org/3/library/string.html) for more details.
- `ascii_lowercase`
- `digits`

##### `time`
Provides time-related functions for measuring execution time and adding delays in processing. See the [Python time documentation](https://docs.python.org/3/library/time.html) for more details.
- `time`
- `sleep`

##### `typing`
Provides support for type hints and static type checking to improve code clarity and IDE support. See the [Python typing documentation](https://docs.python.org/3/library/typing.html) for more details.
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

##### `urllib`
Provides modules for working with URLs, including URL parsing and manipulation. See the [Python urllib documentation](https://docs.python.org/3/library/urllib.html) for more details.
- `parse`

##### `urllib.parse`
Provides URL parsing utilities for breaking apart and constructing URLs and query strings. See the [Python urllib.parse documentation](https://docs.python.org/3/library/urllib.parse.html) for more details.
- `urlencode`
- `quote`

##### `uuid`
Provides functions for generating universally unique identifiers (UUIDs) for creating unique record identifiers. See the [Python uuid documentation](https://docs.python.org/3/library/uuid.html) for more details.
- `uuid4`
- `UUID`

##### `zoneinfo`
Provides timezone support for handling datetime objects across different time zones. See the [Python zoneinfo documentation](https://docs.python.org/3/library/zoneinfo.html) for more details.
- `ZoneInfo`

## Third-Party Modules

The following third-party modules and their allowed imports are available within the sandbox:

##### `arrow`
A human-friendly approach to creating, manipulating, formatting and converting dates and times. See the [Arrow documentation](https://arrow.readthedocs.io/en/latest/) for more details.
- `get`
- `now`
- `utcnow`

##### `django.db.models`
Django's database abstraction layer for defining database models and performing queries. See the [Django models documentation](https://docs.djangoproject.com/en/stable/topics/db/models/) for more details.
- `BigIntegerField`
- `Case`
- `CharField`
- `IntegerField`
- `Model`
- `Q`
- `Value`
- `When`

##### `django.db.models.expressions`
Django's database expressions for complex query operations and conditional logic. See the [Django query expressions documentation](https://docs.djangoproject.com/en/stable/ref/models/expressions/) for more details.
- `Case`
- `Value`
- `When`

##### `django.db.models.query`
Django's QuerySet class for database query operations and result handling. See the [Django QuerySet documentation](https://docs.djangoproject.com/en/stable/ref/models/querysets/) for more details.
- `QuerySet`

##### `django.utils.functional`
Django's functional programming utilities including caching and lazy evaluation tools. See the [Django utils documentation](https://docs.djangoproject.com/en/stable/ref/utils/) for more details.
- `cached_property`

##### `jwt`
A library for encoding and decoding JSON Web Tokens (JWT) for secure data transmission and authentication. See the [PyJWT documentation](https://pyjwt.readthedocs.io/en/stable/) for more details.
- `decode`
- `encode`

##### `pydantic`
A data validation library using Python type annotations for parsing and validating data structures. See the [Pydantic documentation](https://docs.pydantic.dev/) for more details.
- `ValidationError`

##### `rapidfuzz`
A fast string matching library for fuzzy string comparison and search operations. See the [RapidFuzz documentation](https://maxbachmann.github.io/RapidFuzz/) for more details.
- `fuzz`
- `process`
- `utils`

##### `requests`
A simple and elegant HTTP library for making web requests and API calls. See the [Requests documentation](https://docs.python-requests.org/en/latest/) for more details.
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
- `canvas_sdk.v1.data`
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