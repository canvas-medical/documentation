---
title: "Sandboxing and Allowed Imports"
---

Plugins developed with the Canvas SDK operate within a sandboxed environment. This sandbox strictly limits access to the host operating system, filesystem, and database. This security measure is designed to mitigate risks associated with accidental misconfigurations or malicious activities, thereby safeguarding sensitive patient data.

## Standard Library Modules

The following Python standard library modules and their allowed imports are available within the sandbox:

##### `__future__`
Provides access to features from future Python versions for backwards compatibility. [read more](https://docs.python.org/3/library/__future__.html)
- `annotations`

##### `abc`
Provides infrastructure for defining Abstract Base Classes (ABCs) to enforce interfaces and create structured inheritance hierarchies. [read more](https://docs.python.org/3/library/abc.html)
- `ABC`
- `abstractmethod`

##### `base64`
Provides functions for encoding and decoding data in base64 format, commonly used for data transmission and storage. [read more](https://docs.python.org/3/library/base64.html)
- `b64decode`
- `b64encode`

##### `collections`
Provides specialized container datatypes that extend beyond the built-in types like lists and dictionaries. [read more](https://docs.python.org/3/library/collections.html)
- `Counter`
- `defaultdict`

##### `dataclasses`
This module provides a decorator and functions for automatically adding generated special methods such as __init__() and __repr__() to user-defined classes. [read more](https://docs.python.org/3/library/dataclasses.html)

- `asdict`
- `astuple`
- `dataclass`
- `field`
- `Field`
- `fields`
- `InitVar`
- `replace`

##### `datetime`
Provides classes for working with dates and times, essential for medical applications that need to track appointment schedules and patient timelines. [read more](https://docs.python.org/3/library/datetime.html)
- `date`
- `datetime`
- `time`
- `timedelta`
- `timezone`
- `UTC`

##### `dateutil`
Extends Python's datetime capabilities with more flexible date parsing and arithmetic. [read more](https://dateutil.readthedocs.io/en/stable/)
- `relativedelta`

##### `dateutil.relativedelta`
Provides relative time delta calculations for more complex date arithmetic operations. [read more](https://dateutil.readthedocs.io/en/stable/relativedelta.html)
- `relativedelta`

##### `decimal`
Provides precise decimal arithmetic for financial and scientific calculations where floating-point accuracy is critical. [read more](https://docs.python.org/3/library/decimal.html)
- `Decimal`

##### `defusedxml.ElementTree`
The defusedxml package contains several Python-only workarounds and fixes for denial of service and other vulnerabilities in Python’s XML libraries. [read more](https://pypi.org/project/defusedxml/)
- `fromstring`

##### `enum`
Provides support for enumerations, useful for defining sets of named constants such as status codes or categories. [read more](https://docs.python.org/3/library/enum.html)
- `Enum`
- `StrEnum`

##### `functools`
Provides utilities for higher-order functions and operations on callable objects. [read more](https://docs.python.org/3/library/functools.html)
- `reduce`
- `wraps`

##### `hashlib`
Provides secure hash and message digest algorithms for data integrity verification and security purposes. [read more](https://docs.python.org/3/library/hashlib.html)
- `sha256`

##### `hmac`
Provides hash-based message authentication code (HMAC) functions for secure message authentication. [read more](https://docs.python.org/3/library/hmac.html)
- `compare_digest`
- `new`

##### `html`
Provides functions for escaping and unescaping HTML entities, useful for safely handling HTML text in web applications. [read more](https://docs.python.org/3/library/html.html)
- `escape`
- `unescape`

##### `http`
Provides HTTP status codes and related constants for web API development and HTTP response handling. [read more](https://docs.python.org/3/library/http.html)
- `HTTPStatus`

##### `json`
Provides functions for parsing and generating JSON data, essential for API communication and data serialization. [read more](https://docs.python.org/3/library/json.html)
- `dumps`
- `loads`

##### `operator`
Provides function equivalents of operators for functional programming and complex data operations. [read more](https://docs.python.org/3/library/operator.html)
- `and_`

##### `random`
Provides functions for generating random numbers and making random selections, useful for sampling and testing scenarios. [read more](https://docs.python.org/3/library/random.html)
- `choices`
- `uniform`
- `randint`

##### `re`
Provides regular expression matching operations for pattern matching and text processing. [read more](https://docs.python.org/3/library/re.html)
- `compile`
- `DOTALL`
- `findall`
- `IGNORECASE`
- `match`
- `search`
- `split`
- `sub`

##### `string`
Provides string constants and template classes for string manipulation and formatting operations. [read more](https://docs.python.org/3/library/string.html)
- `ascii_lowercase`
- `digits`

##### `time`
Provides time-related functions for measuring execution time and adding delays in processing. [read more](https://docs.python.org/3/library/time.html)
- `time`
- `sleep`

##### `typing`
Provides support for type hints and static type checking to improve code clarity and IDE support. [read more](https://docs.python.org/3/library/typing.html)
- `Any`
- `Callable`
- `cast`
- `ClassVar`
- `Dict`
- `Final`
- `Iterable`
- `List`
- `Literal`
- `NamedTuple`
- `NotRequired`
- `Pattern`
- `Protocol`
- `Optional`
- `Sequence`
- `Tuple`
- `Type`
- `TypedDict`
- `TypeGuard`
- `Union`

##### `urllib`
Provides modules for working with URLs, including URL parsing and manipulation. [read more](https://docs.python.org/3/library/urllib.html)
- `parse`

##### `urllib.parse`
Provides URL parsing utilities for breaking apart and constructing URLs and query strings. [read more](https://docs.python.org/3/library/urllib.parse.html)
- `quote`
- `unquote`
- `urlencode`

##### `uuid`
Provides functions for generating universally unique identifiers (UUIDs) for creating unique record identifiers. [read more](https://docs.python.org/3/library/uuid.html)
- `uuid4`
- `UUID`

##### `zoneinfo`
Provides timezone support for handling datetime objects across different time zones. [read more](https://docs.python.org/3/library/zoneinfo.html)
- `ZoneInfo`

## Third-Party Modules

The following third-party modules and their allowed imports are available within the sandbox:

##### `arrow`
A human-friendly approach to creating, manipulating, formatting and converting dates and times. [read more](https://arrow.readthedocs.io/en/latest/)
- `get`
- `now`
- `utcnow`

##### `django.db.models`
Django's database abstraction layer for defining database models and performing queries. [read more](https://docs.djangoproject.com/en/stable/topics/db/models/)
- `Avg`
- `BigIntegerField`
- `Case`
- `CharField`
- `Count`
- `Exists`
- `FloatField`
- `Func`
- `IntegerField`
- `Max`
- `Min`
- `Model`
- `OuterRef`
- `Prefetch`
- `Q`
- `RowRange`
- `Subquery`
- `Sum`
- `Value`
- `ValueRange`
- `When`
- `Window`

##### `django.db.models.expressions`
Django's database expressions for complex query operations and conditional logic. [read more](https://docs.djangoproject.com/en/stable/ref/models/expressions/)
- `Case`
- `Exists`
- `OuterRef`
- `Subquery`
- `Value`
- `When`

##### `django.db.models.functions`
Django's database functions for transforming and computing values in queries, including window functions for analytics. [read more](https://docs.djangoproject.com/en/stable/ref/models/database-functions/)
- `Coalesce`
- `CumeDist`
- `DenseRank`
- `FirstValue`
- `Lag`
- `LastValue`
- `Lead`
- `NthValue`
- `Ntile`
- `PercentRank`
- `Rank`
- `RowNumber`
- `Trim`

##### `django.db.models.query`
Django's QuerySet class for database query operations and result handling. [read more](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- `Prefetch`
- `QuerySet`

##### `django.db`
Django's database module providing core database exceptions. [read more](https://docs.djangoproject.com/en/stable/ref/exceptions/#database-exceptions)
- `IntegrityError`

##### `django.utils.functional`
Django's functional programming utilities including caching and lazy evaluation tools. [read more](https://docs.djangoproject.com/en/stable/ref/utils/)
- `cached_property`

##### `jwt`
A library for encoding and decoding JSON Web Tokens (JWT) for secure data transmission and authentication. [read more](https://pyjwt.readthedocs.io/en/stable/)
- `decode`
- `encode`
- `ExpiredSignatureError`
- `InvalidTokenError`
- `PyJWKClient`

##### `pydantic`
A data validation library using Python type annotations for parsing and validating data structures. [read more](https://docs.pydantic.dev/)
- `BaseModel`
- `conint`
- `ConfigDict`
- `constr`
- `Field`
- `RootModel`
- `ValidationError`

##### `rapidfuzz`
A fast string matching library for fuzzy string comparison and search operations. [read more](https://maxbachmann.github.io/RapidFuzz/)
- `fuzz`
- `process`
- `utils`

##### `requests`
A simple and elegant HTTP library for making web requests and API calls. [read more](https://docs.python-requests.org/en/latest/)
- `delete`
- `get`
- `patch`
- `post`
- `put`
- `request`
- `RequestException`
- `Response`
- `Session`

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
- `getattr`
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
- `sum`
- `super`
- `vars`

Plus all the standard safe builtins from RestrictedPython including basic types (`bool`, `int`, `float`, `str`, `tuple`, etc.) and safe operations.

## Requesting Additional Imports

If there is a library or function not on this list that you wish to import in your plugin, reach out on the [Canvas developer forum](https://github.com/canvas-medical/canvas-plugins/discussions). Additional imports can often be added after a security review.

The allowed imports are defined in the [Canvas Plugins repository](https://github.com/canvas-medical/canvas-plugins/blob/main/plugin_runner/sandbox.py) and are regularly updated to support common development needs while maintaining security.

## Policy on Vendor-Specific Libraries:

The current policy strongly discourages the inclusion of vendor-specific libraries. Introducing such libraries presents several challenges:

* Vendor Prioritization: It risks implicitly favoring one vendor over others, which can be problematic in a multi-vendor ecosystem.

* Dependency Bloat: Incorporating libraries for each vendor within a specific category (e.g., AI model providers like OpenAI, Anthropic) leads to a significant increase in overall dependencies.

## Technical Implications of Excessive Dependencies:

Adding a multitude of vendor-specific libraries can result in:

* Increased Memory Usage: Each additional library contributes to the application's memory footprint.

* Dependency Conflicts: Different libraries may require different versions of shared dependencies, leading to versioning conflicts and system instability.

Given these considerations, the platform maintains a strict and judicious approach to approving and incorporating external libraries or imports.
