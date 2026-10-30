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
- `urlsafe_b64decode`
- `urlsafe_b64encode`

##### `bisect`
Provides functions for finding insertion points in a sorted list and inserting items while keeping it sorted. [read more](https://docs.python.org/3/library/bisect.html)
- `bisect_left`
- `bisect_right`
- `insort`

##### `collections`
Provides specialized container datatypes that extend beyond the built-in types like lists and dictionaries. [read more](https://docs.python.org/3/library/collections.html)
- `Counter`
- `defaultdict`
- `OrderedDict`

##### `copy`
Provides shallow and deep copy operations for duplicating objects. [read more](https://docs.python.org/3/library/copy.html)
- `copy`
- `deepcopy`

##### `dataclasses`
This module provides a decorator and functions for automatically adding generated special methods such as __init__() and __repr__() to user-defined classes. [read more](https://docs.python.org/3/library/dataclasses.html)
- `asdict`
- `astuple`
- `dataclass`
- `field`
- `Field`
- `fields`
- `InitVar`
- `is_dataclass`
- `make_dataclass`
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
Extends Python’s datetime capabilities with more flexible date parsing and arithmetic. [read more](https://dateutil.readthedocs.io/en/stable/)
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

##### `email.mime.multipart`
Provides the MIME class for building multipart email messages, such as a message with a plain-text and an HTML part. [read more](https://docs.python.org/3/library/email.mime.html)
- `MIMEMultipart`

##### `email.mime.text`
Provides the MIME class for the text parts of an email message. [read more](https://docs.python.org/3/library/email.mime.html)
- `MIMEText`

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
- `sha1`
- `sha256`

##### `hmac`
Provides hash-based message authentication code (HMAC) functions for secure message authentication. [read more](https://docs.python.org/3/library/hmac.html)
- `compare_digest`
- `new`

##### `html`
Provides functions for escaping and unescaping HTML entities. [read more](https://docs.python.org/3/library/html.html)
- `escape`
- `HTML`
- `unescape`

##### `http`
Provides HTTP status codes and related constants for web API development and HTTP response handling. [read more](https://docs.python.org/3/library/http.html)
- `HTTPStatus`

##### `io`
Provides in-memory text and binary streams for working with data as if it were a file. [read more](https://docs.python.org/3/library/io.html)
- `BytesIO`
- `StringIO`

##### `json`
Provides functions for parsing and generating JSON data, essential for API communication and data serialization. [read more](https://docs.python.org/3/library/json.html)
- `dump`
- `dumps`
- `JSONDecodeError`
- `load`
- `loads`

##### `operator`
Provides function equivalents of operators for functional programming and complex data operations. [read more](https://docs.python.org/3/library/operator.html)
- `and_`
- `or_`

##### `random`
Provides functions for generating random numbers and making random selections, useful for sampling and testing scenarios. [read more](https://docs.python.org/3/library/random.html)
- `choice`
- `choices`
- `randint`
- `random`
- `Random`
- `sample`
- `uniform`

##### `re`
Provides regular expression matching operations for pattern matching and text processing. [read more](https://docs.python.org/3/library/re.html)
- `compile`
- `DOTALL`
- `escape`
- `findall`
- `finditer`
- `fullmatch`
- `I`
- `IGNORECASE`
- `M`
- `match`
- `MULTILINE`
- `S`
- `search`
- `split`
- `sub`

##### `secrets`
Provides cryptographically secure random values for tokens, verification codes, and other values that must be hard to guess. Use it instead of `random`, whose output is predictable. This module is unrelated to the plugin secrets declared in `CANVAS_MANIFEST.json`. [read more](https://docs.python.org/3/library/secrets.html)
- `choice`
- `compare_digest`
- `randbelow`
- `token_bytes`
- `token_hex`
- `token_urlsafe`

##### `statistics`
Provides functions for calculating statistics of numeric data. [read more](https://docs.python.org/3/library/statistics.html)
- `median`

##### `string`
Provides string constants and template classes for string manipulation and formatting operations. [read more](https://docs.python.org/3/library/string.html)
- `ascii_lowercase`
- `digits`

##### `time`
Provides time-related functions for measuring execution time and adding delays in processing. [read more](https://docs.python.org/3/library/time.html)
- `monotonic`
- `perf_counter`
- `time`
- `time_ns`

##### `traceback`
Provides functions for extracting, formatting, and printing stack traces. [read more](https://docs.python.org/3/library/traceback.html)
- `format_exc`

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
- `Optional`
- `Pattern`
- `Protocol`
- `Sequence`
- `Tuple`
- `TYPE_CHECKING`
- `Type`
- `TypedDict`
- `TypeGuard`
- `Union`

##### `urllib`
Provides modules for working with URLs, including URL parsing and manipulation. [read more](https://docs.python.org/3/library/urllib.html)
- `parse`

##### `urllib.parse`
Provides URL parsing utilities for breaking apart and constructing URLs and query strings. [read more](https://docs.python.org/3/library/urllib.parse.html)
- `parse_qs`
- `quote`
- `unquote`
- `urlencode`
- `urlparse`

##### `uuid`
Provides functions for generating universally unique identifiers (UUIDs) for creating unique record identifiers. [read more](https://docs.python.org/3/library/uuid.html)
- `NAMESPACE_URL`
- `UUID`
- `uuid4`
- `uuid5`

##### `xml.etree`
The package that contains the ElementTree XML API. [read more](https://docs.python.org/3/library/xml.etree.elementtree.html)
- `ElementTree`

##### `xml.etree.ElementTree`
Provides the ElementTree API for parsing and building XML documents. In the sandbox, parsing does not resolve external entities. [read more](https://docs.python.org/3/library/xml.etree.elementtree.html)
- `Element`
- `ElementTree`
- `fromstring`
- `indent`
- `iterparse`
- `parse`
- `QName`
- `register_namespace`
- `SubElement`
- `tostring`

##### `zlib`
Provides compression and decompression compatible with gzip, along with checksum functions. [read more](https://docs.python.org/3/library/zlib.html)
- `adler32`
- `compress`
- `compressobj`
- `crc32`
- `decompress`
- `decompressobj`
- `error`
- `MAX_WBITS`

##### `zoneinfo`
Provides timezone support for handling datetime objects across different time zones. [read more](https://docs.python.org/3/library/zoneinfo.html)
- `ZoneInfo`

## Third-Party Modules

The following third-party modules and their allowed imports are available within the sandbox:

##### `arrow`
A human-friendly approach to creating, manipulating, formatting and converting dates and times. [read more](https://arrow.readthedocs.io/en/latest/)
- `Arrow`
- `get`
- `now`
- `parser`
- `utcnow`

##### `arrow.parser`
The exceptions Arrow raises when it can't parse a date or time string. [read more](https://arrow.readthedocs.io/en/latest/api-guide.html#module-arrow.parser)
- `ParserError`
- `ParserMatchError`

##### `certifi`
Provides the path to Mozilla's bundle of trusted root certificates. [read more](https://github.com/certifi/python-certifi)
- `where`

##### `django.contrib.postgres.indexes`
Django’s PostgreSQL-specific index types for advanced indexing strategies. [read more](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/indexes/)
- `GinIndex`

##### `django.core.exceptions`
Django's core exceptions, including the ones model queries and validation raise. [read more](https://docs.djangoproject.com/en/stable/ref/exceptions/#django-core-exceptions)
- `ObjectDoesNotExist`
- `PermissionDenied`
- `ValidationError`

##### `django.db`
Django’s database module providing core database exceptions. [read more](https://docs.djangoproject.com/en/stable/ref/exceptions/#database-exceptions)
- `DatabaseError`
- `IntegrityError`

##### `django.db.models`
Django’s database abstraction layer for defining database models and performing queries. [read more](https://docs.djangoproject.com/en/stable/topics/db/models/)
- `Avg`
- `BigIntegerField`
- `BooleanField`
- `CASCADE`
- `Case`
- `CharField`
- `Count`
- `DateField`
- `DateTimeField`
- `DecimalField`
- `DO_NOTHING`
- `Exists`
- `F`
- `FloatField`
- `ForeignKey`
- `Func`
- `Index`
- `IntegerField`
- `JSONField`
- `ManyToManyField`
- `Max`
- `Min`
- `OneToOneField`
- `OuterRef`
- `Prefetch`
- `Q`
- `RowRange`
- `SET_NULL`
- `Subquery`
- `Sum`
- `TextField`
- `UniqueConstraint`
- `Value`
- `ValueRange`
- `When`
- `Window`

##### `django.db.models.expressions`
Django’s database expressions for complex query operations and conditional logic. [read more](https://docs.djangoproject.com/en/stable/ref/models/expressions/)
- `Case`
- `Exists`
- `OuterRef`
- `Subquery`
- `Value`
- `When`

##### `django.db.models.functions`
Django’s database functions for common SQL operations and window functions. [read more](https://docs.djangoproject.com/en/stable/ref/models/database-functions/)
- `Coalesce`
- `CumeDist`
- `DenseRank`
- `FirstValue`
- `Lag`
- `LastValue`
- `Lead`
- `Length`
- `NthValue`
- `Ntile`
- `PercentRank`
- `Rank`
- `RowNumber`
- `Trim`

##### `django.db.models.query`
Django’s QuerySet class for database query operations and result handling. [read more](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- `Prefetch`
- `QuerySet`

##### `django.db.transaction`
Django’s transaction management for atomic database operations. [read more](https://docs.djangoproject.com/en/stable/topics/db/transactions/)
- `atomic`
- `on_commit`
- `on_rollback`

##### `django.utils`
Django's utility package. [read more](https://docs.djangoproject.com/en/stable/ref/utils/)
- `timezone`

##### `django.utils.functional`
Django’s functional programming utilities including caching and lazy evaluation tools. [read more](https://docs.djangoproject.com/en/stable/ref/utils/)
- `cached_property`

##### `django.utils.timezone`
Django's helpers for working with time zone aware datetimes. [read more](https://docs.djangoproject.com/en/stable/ref/utils/#module-django.utils.timezone)
- `get_current_timezone`
- `localdate`
- `localtime`
- `make_aware`
- `now`
- `utc`

##### `jwt`
A library for encoding and decoding JSON Web Tokens (JWT) for secure data transmission and authentication. [read more](https://pyjwt.readthedocs.io/en/stable/)
- `decode`
- `encode`
- `ExpiredSignatureError`
- `InvalidTokenError`
- `PyJWKClient`

<!-- source: discussion #796 -->
`encode` can sign tokens with RS256, which some external APIs, such as Google's, require. The `cryptography` package that RS256 relies on is installed, but plugins can't import it directly.

##### `pydantic`
A data validation library using Python type annotations for parsing and validating data structures. [read more](https://docs.pydantic.dev/)
- `BaseModel`
- `ConfigDict`
- `conint`
- `constr`
- `Field`
- `RootModel`
- `ValidationError`

##### `rapidfuzz`
A fast string matching library for fuzzy string comparison and search operations. [read more](https://maxbachmann.github.io/RapidFuzz/)
- `fuzz`
- `process`
- `utils`

##### `rapidfuzz.fuzz`
RapidFuzz's string similarity scorers. [read more](https://rapidfuzz.github.io/RapidFuzz/Usage/fuzz.html)
- `partial_ratio`
- `partial_ratio_alignment`
- `partial_token_ratio`
- `partial_token_set_ratio`
- `partial_token_sort_ratio`
- `QRatio`
- `ratio`
- `token_ratio`
- `token_set_ratio`
- `token_sort_ratio`
- `WRatio`

##### `rapidfuzz.process`
RapidFuzz's functions for comparing a string against a list of choices. [read more](https://rapidfuzz.github.io/RapidFuzz/Usage/process.html)
- `cdist`
- `cpdist`
- `extract`
- `extract_iter`
- `extractOne`

##### `rapidfuzz.utils`
RapidFuzz's string preprocessing utilities. [read more](https://rapidfuzz.github.io/RapidFuzz/Usage/utils.html)
- `default_process`

##### `requests.exceptions`
The exceptions the requests library raises, which the [`Http`](/sdk/utils/) util passes through. [read more](https://requests.readthedocs.io/en/latest/api/#exceptions)
- `ConnectionError`
- `HTTPError`
- `JSONDecodeError`
- `RequestException`
- `Timeout`

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
- `ascii`
- `bytearray`
- `classmethod`
- `delattr`
- `dict`
- `dir`
- `enumerate`
- `extract_exc_frames`
- `filter`
- `format`
- `getattr`
- `hasattr`
- `iter`
- `list`
- `map`
- `max`
- `memoryview`
- `min`
- `next`
- `property`
- `reversed`
- `setattr`
- `staticmethod`
- `sum`
- `super`
- `type`
- `vars`

On top of those, the sandbox inherits RestrictedPython's safe builtins. That covers the basic types (`bool`, `bytes`, `complex`, `float`, `frozenset`, `int`, `set`, `slice`, `str`, `tuple`), the common functions (`abs`, `callable`, `chr`, `divmod`, `hash`, `hex`, `id`, `isinstance`, `issubclass`, `len`, `oct`, `ord`, `pow`, `range`, `repr`, `round`, `sorted`, `zip`), and the `NotImplemented` constant. Every built-in exception and warning class is also available, including the `OSError` family such as `TimeoutError` and `ConnectionError`.

For HTTP calls, catch the exceptions in [`requests.exceptions`](#requestsexceptions). The [`Http`](/sdk/utils/) util passes them through unchanged:

```python
from requests.exceptions import Timeout

from canvas_sdk.utils import Http
from logger import log

client = Http()

try:
    response = client.get("https://example.com/api")
except Timeout:
    log.warning("The request to example.com timed out.")
```

### Builtins that work differently

A few builtins are narrower in the sandbox than in standard Python, so that they can't reach past the [runtime restrictions](#runtime-restrictions):

| Builtin | In the sandbox |
| --- | --- |
| `type` | Takes exactly one argument. `type(x)` returns the same thing as `x.__class__`, so for an object from outside your plugin you get a [proxy that exposes only names](#reading-attributes). The three-argument form raises `TypeError`; declare classes with `class …:` instead. |
| `dir` | Takes exactly one argument, and lists only the names your plugin can read on that object. |
| `setattr`, `delattr` | Follow the same rules as `obj.x = value` and `del obj.x` (see [writing attributes](#writing-attributes)). They also refuse any name starting with `__`, any class defined outside your plugin, and a name starting with `_` on an object defined outside your plugin. |
| `vars` | Requires an argument. For an object or module from outside your plugin it returns a filtered copy, the same as [`__dict__`](#reading-attributes). |

### Builtins that are not available

What you see above is the whole set. The sandbox works from an allow-list rather than a list of banned names, so any builtin not mentioned there raises `NameError` when your plugin runs — including builtins that future Python releases introduce.

These are the ones plugin authors reach for most often:

| Not available | Use instead |
| --- | --- |
| `eval`, `exec`, `compile` | Write the logic directly. The sandbox cannot run code it never reviewed. |
| `open`, `input` | Neither the filesystem nor a console is reachable from a plugin. |
| `print` | `log` from `logger`. `print` is also a [reserved name](#reserved-names). |
| `globals`, `locals` | Nothing. Namespace introspection is a sandbox-escape route. |

## Forbidden Constructs

Beyond the import allow-list above, a few Python constructs compile under RestrictedPython but are rejected when your code runs in the sandbox. `canvas validate` catches these statically before you install, so you don't have to wait for a runtime failure on the instance.

| Construct | Why it's rejected | Use instead |
| --- | --- | --- |
| `type(name, bases, dict)` | The sandbox's `type` takes one argument, so dynamic class creation raises `TypeError` | Declare the class normally with `class …:` |
| `obj.attr += v` | Augmented assignment to an attribute is rejected, including on classes you defined yourself | Explicit reassignment: `obj.attr = obj.attr + v` |
| `d[k] += v` | Augmented assignment to a dict item, list item, or slice is rejected | Explicit reassignment: `d[k] = d[k] + v` |

Augmented assignment to a plain variable is fine — `count += 1`, `total *= 2`, and the rest of the `-=` / `*=` / `//=` / `%=` / `**=` / `&=` / `|=` / `^=` / `<<=` / `>>=` family all work. It is only the attribute and item forms above that are rejected, and both fail when the plugin is compiled, so you find out at install time rather than mid-request.

{% include alert.html type="info" content="<code>@dataclass(frozen=True)</code> and <code>@dataclass(slots=True)</code> load and run fine in the sandbox — they are not forbidden." %}

<!-- source: discussion #844 -->
{% include alert.html type="info" content="<code>match</code> statements are allowed in plugin code." %}

### `extract_exc_frames()`

A sandbox-provided function that extracts frame information from the current exception's traceback. Must be called from within an `except` block. Returns an empty list if no exception is active.

Each frame exposes only safe attributes:
- `filename` — the file path
- `lineno` — the line number
- `name` — the function name

Source code lines and local variables are not accessible.

```python?partial=true
from logger import log 

try:
    raise Exception("some failed operation")
except Exception:
    frames = extract_exc_frames()
    for frame in frames:
        log.info(f"{frame.filename}:{frame.lineno} in {frame.name}")
```

## Runtime Restrictions

The sandbox enforces the rules in this section every time an attribute is read or written, so they surface as an `AttributeError` while your plugin is running. That is what separates them from the [forbidden constructs](#forbidden-constructs), which are rejected when your code is compiled and reported by `canvas validate` before you install. Except for the [helper-module check](#helper-modules) below, nothing described here is caught until the code executes.

Throughout this section, **your plugin's code** means modules inside your own plugin package. **External code** means everything else — the Canvas SDK, the standard library, and third-party modules.

### Helper modules

The rules apply to every module in your plugin, not only the modules your manifest names as handlers. A helper module that a handler imports runs in the sandbox too, so its functions keep the sandbox's rules when a handler calls them.

A function body in a helper module runs only when something calls it. So the plugin runner also reads those bodies when it loads your plugin. If one contains a construct the rules refuse, the runner doesn't load the plugin. Every handler in the plugin then fails with a `PluginInstallationError` that lists each construct with its module and line. `canvas validate` and `canvas install` report the same error. The check looks for:

- an import of a module that isn't on the allow-list
- importing or reading a name that the allow-list doesn't grant from an allowed module, such as `re.Match`
- reading `__dict__`, `raw`, or a [restricted method name](#introspection-attributes) on any object
- a `format` or `format_map` template whose fields read attributes or items (see [string formatting](#string-formatting))
- any call to `vars()`

Fix each listed line, then validate again.

### Reading attributes

Attribute names that begin with an underscore are restricted, and the rule depends on where the object came from:

| Object defined in | `_single_underscore` | `__dunder__` |
| --- | --- | --- |
| Your plugin's code | Readable | Only names on the allow-list below |
| External code | Blocked, except `_meta` on SDK models | Only names on the allow-list below |

The dunder allow-list is the same in both cases:

- `__annotations__`
- `__args__`
- `__ceil__`
- `__class__`
- `__dict__`
- `__doc__`
- `__eq__`
- `__floor__`
- `__init__`
- `__members__`
- `__name__`
- `__origin__`
- `__round__`
- `__traceback__`
- `__trunc__`

Several names return a restricted stand-in rather than the real object:

- **`__class__`** on an object defined outside your plugin, or on any class, returns a read-only proxy that exposes only `__name__` and `__mro__`. On an object your plugin defined, it returns the real class.
- **`__mro__`** on any class returns a tuple of proxies that each expose only `__name__`. You can check a class's ancestry by name, but `__subclasses__()` and the classes themselves can't be reached to get outside the sandbox.
- **`__dict__`** on an object, class, or module from outside your plugin returns a copy without any name that starts with an underscore. For a module, the copy holds only the names its allow-list entry grants. For an object that declares [`__exports__`](#__exports__), it holds only those names. Changing the copy doesn't change the object. `vars()` returns the same copy. On your plugin's own objects and modules, both return the real namespace.
- **`__traceback__`** returns a safe traceback exposing only `tb_frame`, `tb_lineno`, and `tb_next`. Its frame exposes only `f_code` and `f_lineno`, and that code object exposes only `co_filename` and `co_name`. Local and global variables are never reachable. [`extract_exc_frames()`](#extract_exc_frames) is the more convenient way to read a traceback.
- **`_meta`** on an SDK model class or instance returns a read-only view for inspecting the model's fields. It exposes `app_label`, `concrete_fields`, `db_table`, `fields`, `get_field()`, `get_fields()`, `local_fields`, `model_name`, `pk`, `verbose_name`, and `verbose_name_plural`. Each field in it exposes `attname`, `blank`, `choices`, `column`, `concrete`, `default`, `get_internal_type()`, `is_relation`, `many_to_many`, `many_to_one`, `max_length`, `name`, `null`, `one_to_many`, `one_to_one`, and `related_model`. A field's `default` reads as `None` when the default is a callable.

Reading a plain attribute off an external module is also limited to that module's entry in the allow-list at the top of this page. `json.dumps` works because `dumps` is listed under `json`; `json.tool` raises an `AttributeError`.

Modules in your plugin's own package aren't on the allow-list and don't need to be. You can import one of them and read its attributes through the module object, the same as importing those names directly:

```python?partial=true
from my_plugin.lib import store

store.get_latest()  # same as: from my_plugin.lib.store import get_latest
```

### Attributes that don't exist

In the sandbox, reading an attribute that nothing defines returns `None`, where standard Python raises `AttributeError`. This behavior is deprecated, and a future release will raise `AttributeError` instead. Until then, the first time your plugin reads each such name, a warning naming it appears in your [plugin logs](/sdk/plugin-logs/). `canvas validate` also lists the names your handlers read while they load. It can't see names read later, inside a handler method.

To read an attribute that may be absent, pass `getattr` a default. That returns the default without a warning:

```python
class Reading:
    def __init__(self) -> None:
        self.value = 98.6


reading = Reading()

reading.unit                    # None for now, with a warning; AttributeError in a future release
getattr(reading, "unit", None)  # None, with no warning
```

An `AttributeError` raised by an attribute that does exist propagates as it does in standard Python, rather than reading as `None`. Two examples are an error raised inside a property, and Django's `RelatedObjectDoesNotExist` from a one-to-one relation that has no related record. Catch the error, or pass `getattr` a default, where the value may be missing.

A read that the rules on this page refuse, such as an underscore name on an external object, still raises `AttributeError`.

### Reading items

A string key that starts with an underscore can be read from any dictionary, including subclasses such as `defaultdict`, `Counter`, and `OrderedDict`. The same goes for built-in containers and objects from the allowed standard-library and third-party modules. Other objects, including a class in your plugin that implements `__getitem__` without subclassing `dict`, raise an `AttributeError` for that key:

```python
config = {"timeout": 30, "_internal": True}

config["timeout"]    # fine
config["_internal"]  # fine
```

### Writing attributes

You can set attributes on modules that belong to your plugin. Setting an attribute on any other module is blocked.

For objects, whether a write is allowed depends on where the object's class was defined:

- **Class defined in your plugin's code** — writable, including attributes that are not methods.
- **Class defined in external code** — the write is blocked if any of the following is true:
  - the name you are assigning through was brought in by an `import`
  - the attribute currently holds a callable, so the assignment would replace a method

```python
class MyThing:
    """Defined in your plugin, so its instances are writable."""

    def __init__(self) -> None:
        self.count = 0


thing = MyThing()
thing.count = 1       # fine
thing.label = "new"   # fine
```

### Reserved names

These four names cannot be used for a function, variable, class, or argument anywhere in your plugin:

- `print`
- `printed`
- `builtins`
- `breakpoint`

`print` is among them, so use the SDK logger for output:

```python
from logger import log

log.info("plugin started")
```

The sandbox also reserves `__metaclass__` and the names of its own guards: `_apply_`, `_getattr_`, `_getitem_`, `_getiter_`, `_inplacevar_`, `_iter_unpack_sequence_`, `_print`, `_print_`, `_unpack_sequence_`, and `_write_`. Binding one of them in any way, including as an import alias, a loop target, or an `except … as` name, is an error.

Names that start with two underscores can't be bound either, with three exceptions:

- `__all__`
- methods defined directly in a class body, such as `__init__` or `__str__`
- function and lambda argument names

### Introspection attributes

The attributes the `inspect` module relies on are unavailable, because they expose frames, globals, and raw bytecode:

`co_code`, `cr_await`, `cr_code`, `cr_frame`, `cr_origin`, `f_back`, `f_builtins`, `f_code`, `f_generator`, `f_globals`, `f_locals`, `f_trace`, `gi_code`, `gi_frame`, `gi_yieldfrom`, `tb_frame`, `tb_next`

The safe traceback wrappers under [reading attributes](#reading-attributes) are the one exception: they re-expose `tb_frame`, `tb_next`, and `f_code` through an explicit allow-list, stripped down to the fields listed there.

These method names can't be read from any object, including your plugin's own:

`create_module`, `eval`, `exec`, `exec_module`, `find_loader`, `find_module`, `find_spec`, `load_module`, `mro`

To read a class's ancestry, use `__mro__` rather than `mro()`.

### String formatting

`format` and `format_map` work when you call them on a string. Their replacement fields can't read attributes or items of the values they format, so a field such as `{0.name}` or `{0[first_name]}` raises `NotImplementedError`. Read the value out first, then format it. Calling `format` through the `str` type, as in `str.format(template, value)`, also raises `NotImplementedError`.

```python
patient = {"first_name": "Ada"}
name = patient["first_name"]

greeting = "Hello {}".format(name)                 # fine
greeting = "Hello {name}".format(name=name)        # fine
greeting = f"Hello {patient['first_name']}"        # fine
greeting = "Hello {0[first_name]}".format(patient)  # NotImplementedError
greeting = str.format("Hello {}", name)            # NotImplementedError
```

### `__exports__`

Some SDK objects declare an `__exports__` attribute listing exactly which attribute names may be read from them. Where it is present it takes precedence over the other rules in this section: names in the list are readable, and anything else raises an `AttributeError`.

{% include alert.html type="info" content="These rules are enforced by <code>plugin_runner/sandbox.py</code> in the <a href='https://github.com/canvas-medical/canvas-plugins'>Canvas Plugins repository</a>, which is the authoritative reference if you hit a restriction that isn't described here." %}

## Requesting Additional Imports

If there is a library or function not on this list that you wish to import in your plugin, reach out on the [Canvas developer forum](https://github.com/canvas-medical/canvas-plugins/discussions). Additional imports can often be added after a security review.

The allowed imports are defined in the [Canvas Plugins repository](https://github.com/canvas-medical/canvas-plugins/blob/main/plugin_runner/sandbox.py) and are regularly updated to support common development needs while maintaining security.

<!-- source: discussion #1505 -->
### Error monitoring

Error-monitoring SDKs such as `sentry_sdk` are not available in the sandbox. Record errors and diagnostics with [plugin logging](/sdk/plugin-logs/) instead.

## Policy on Vendor-Specific Libraries:

The current policy strongly discourages the inclusion of vendor-specific libraries. Introducing such libraries presents several challenges:

* Vendor Prioritization: It risks implicitly favoring one vendor over others, which can be problematic in a multi-vendor ecosystem.

* Dependency Bloat: Incorporating libraries for each vendor within a specific category (e.g., AI model providers like OpenAI, Anthropic) leads to a significant increase in overall dependencies.

## Technical Implications of Excessive Dependencies:

Adding a multitude of vendor-specific libraries can result in:

* Increased Memory Usage: Each additional library contributes to the application's memory footprint.

* Dependency Conflicts: Different libraries may require different versions of shared dependencies, leading to versioning conflicts and system instability.

Given these considerations, the platform maintains a strict and judicious approach to approving and incorporating external libraries or imports.
