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
Provides functions for escaping and unescaping HTML entities. [read more](https://docs.python.org/3/library/html.html)
- `escape`
- `HTML`
- `unescape`

##### `http`
Provides HTTP status codes and related constants for web API development and HTTP response handling. [read more](https://docs.python.org/3/library/http.html)
- `HTTPStatus`

##### `json`
Provides functions for parsing and generating JSON data, essential for API communication and data serialization. [read more](https://docs.python.org/3/library/json.html)
- `dumps`
- `JSONDecodeError`
- `loads`

##### `operator`
Provides function equivalents of operators for functional programming and complex data operations. [read more](https://docs.python.org/3/library/operator.html)
- `and_`

##### `random`
Provides functions for generating random numbers and making random selections, useful for sampling and testing scenarios. [read more](https://docs.python.org/3/library/random.html)
- `choices`
- `randint`
- `uniform`

##### `re`
Provides regular expression matching operations for pattern matching and text processing. [read more](https://docs.python.org/3/library/re.html)
- `compile`
- `DOTALL`
- `findall`
- `fullmatch`
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
- `sleep`
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

##### `django.contrib.postgres.indexes`
Django’s PostgreSQL-specific index types for advanced indexing strategies. [read more](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/indexes/)
- `GinIndex`

##### `django.db`
Django’s database module providing core database exceptions. [read more](https://docs.djangoproject.com/en/stable/ref/exceptions/#database-exceptions)
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

##### `django.utils.functional`
Django’s functional programming utilities including caching and lazy evaluation tools. [read more](https://docs.djangoproject.com/en/stable/ref/utils/)
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
- `extract_exc_frames`
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

On top of those, the sandbox inherits RestrictedPython's safe builtins. That covers the basic types (`bool`, `bytes`, `complex`, `float`, `frozenset`, `int`, `set`, `slice`, `str`, `tuple`), the common functions (`abs`, `callable`, `chr`, `divmod`, `hash`, `hex`, `id`, `isinstance`, `issubclass`, `len`, `oct`, `ord`, `pow`, `range`, `repr`, `round`, `sorted`, `zip`), and most of the standard exception classes.

### Builtins that are not available

What you see above is the whole set. The sandbox works from an allow-list rather than a list of banned names, so any builtin not mentioned there raises `NameError` when your plugin runs — including builtins that future Python releases introduce.

These are the ones plugin authors reach for most often:

| Not available | Use instead |
| --- | --- |
| `eval`, `exec`, `compile` | Write the logic directly. The sandbox cannot run code it never reviewed. |
| `open`, `input` | Neither the filesystem nor a console is reachable from a plugin. |
| `print` | `log` from `logger`. `print` is also a [reserved name](#reserved-names). |
| `type` | `isinstance(x, SomeClass)` to test a type, `x.__class__.__name__` to read its name. |
| `dir`, `globals`, `locals` | Nothing. Namespace introspection is a sandbox-escape route. |
| `bytearray` | `bytes` for binary data. |

One group is easy to miss: the `OSError` subclasses, including `TimeoutError`, `ConnectionError`, `FileNotFoundError`, and `PermissionError`. Writing `except TimeoutError:` around an HTTP call raises `NameError`. Catch `OSError` instead — it is available, and it matches every one of them:

```python
from canvas_sdk.utils import Http

client = Http()

try:
    response = client.get("https://example.com/api")
except OSError:
    # OSError is the shared base class, so this catches TimeoutError,
    # ConnectionError, and the rest of the family.
    pass
```

## Forbidden Constructs

Beyond the import allow-list above, a few Python constructs compile under RestrictedPython but are rejected when your code runs in the sandbox. `canvas validate` catches these statically before you install, so you don't have to wait for a runtime failure on the instance.

| Construct | Why it's rejected | Use instead |
| --- | --- | --- |
| `setattr(obj, "x", value)` | Dynamic attribute assignment is blocked | Direct assignment: `obj.x = value` |
| `delattr(obj, "x")` | Dynamic attribute deletion is blocked | `del obj.x` |
| `bytearray(...)` | Not available in the sandbox | `bytes` for binary data |
| `type(name, bases, dict)` | Dynamic class creation (3-argument `type`) is not available | Declare the class normally with `class …:` |
| `obj.attr += v` | Augmented assignment to an attribute is rejected, including on classes you defined yourself | Explicit reassignment: `obj.attr = obj.attr + v` |
| `d[k] += v` | Augmented assignment to a dict item, list item, or slice is rejected | Explicit reassignment: `d[k] = d[k] + v` |

Augmented assignment to a plain variable is fine — `count += 1`, `total *= 2`, and the rest of the `-=` / `*=` / `//=` / `%=` / `**=` / `&=` / `|=` / `^=` / `<<=` / `>>=` family all work. It is only the attribute and item forms above that are rejected, and both fail when the plugin is compiled, so you find out at install time rather than mid-request.

{% include alert.html type="warning" content="<code>type</code> is not available in the sandbox <em>at all</em>, including the one-argument <code>type(x)</code> form used to check an object's type — it raises <code>NameError: name 'type' is not defined</code>. Use <code>isinstance(x, SomeClass)</code> to test a type, or <code>x.__class__.__name__</code> to read its name." %}

{% include alert.html type="info" content="<code>@dataclass(frozen=True)</code> and <code>@dataclass(slots=True)</code> load and run fine in the sandbox — they are not forbidden." %}

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

The sandbox enforces the rules in this section every time an attribute is read or written, so they surface as an `AttributeError` while your plugin is running. That is what separates them from the [forbidden constructs](#forbidden-constructs), which are rejected when your code is compiled and reported by `canvas validate` before you install. Nothing described here is caught until the code executes.

Throughout this section, **your plugin's code** means modules inside your own plugin package. **External code** means everything else — the Canvas SDK, the standard library, and third-party modules.

### Reading attributes

Attribute names that begin with an underscore are restricted, and the rule depends on where the object came from:

| Object defined in | `_single_underscore` | `__dunder__` |
| --- | --- | --- |
| Your plugin's code | Readable | Only names on the allow-list below |
| External code | Blocked | Only names on the allow-list below |

The dunder allow-list is the same in both cases:

- `__annotations__`
- `__args__`
- `__class__`
- `__dict__`
- `__eq__`
- `__init__`
- `__members__`
- `__name__`
- `__origin__`
- `__traceback__`

Two of those return a restricted stand-in rather than the real object:

- **`__class__`** on an object defined outside your plugin returns a read-only proxy that exposes only `__name__`. This is what prevents `__class__.__mro__` and `__class__.__subclasses__()` from being used to reach code outside the sandbox.
- **`__traceback__`** returns a safe traceback exposing only `tb_frame`, `tb_lineno`, and `tb_next`. Its frame exposes only `f_code`, and that code object exposes only `co_filename` and `co_name`. Local and global variables are never reachable. [`extract_exc_frames()`](#extract_exc_frames) is the more convenient way to read a traceback.

Reading a plain attribute off an imported module is also limited to that module's entry in the allow-list at the top of this page. `json.dumps` works because `dumps` is listed under `json`; `json.tool` raises an `AttributeError`.

### Reading items

Subscripting with a string key that starts with an underscore is blocked on every object, including dictionaries you created yourself:

```python
config = {"timeout": 30, "_internal": True}

config["timeout"]    # fine
config["_internal"]  # AttributeError
```

### Writing attributes

You can set attributes on modules that belong to your plugin. Setting an attribute on any other module is blocked.

For objects, whether a write is allowed depends on where the object's class was defined:

- **Class defined in your plugin's code** — writable, including attributes that are not methods.
- **Class defined in external code** — the write is blocked if any of the following is true:
  - the name you are assigning through was brought in by an `import`
  - the attribute currently holds a callable, so the assignment would replace a method
  - the target is a dictionary and the key is a string starting with an underscore

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

### Introspection attributes

The attributes the `inspect` module relies on are unavailable, because they expose frames, globals, and raw bytecode:

`co_code`, `cr_await`, `cr_code`, `cr_frame`, `cr_origin`, `f_back`, `f_builtins`, `f_code`, `f_generator`, `f_globals`, `f_locals`, `f_trace`, `gi_code`, `gi_frame`, `gi_yieldfrom`, `tb_frame`, `tb_next`

The safe traceback wrappers under [reading attributes](#reading-attributes) are the one exception: they re-expose `tb_frame`, `tb_next`, and `f_code` through an explicit allow-list, stripped down to the fields listed there.

### String formatting

The `format` and `format_map` methods of `str` are not available. Use an f-string or the `%` operator instead:

```python
name = "Canvas"

greeting = f"Hello {name}"       # fine
greeting = "Hello %s" % name     # fine
greeting = "Hello {}".format(name)  # NotImplementedError
```

### `__exports__`

Some SDK objects declare an `__exports__` attribute listing exactly which attribute names may be read from them. Where it is present it takes precedence over the other rules in this section: names in the list are readable, and anything else raises an `AttributeError`.

{% include alert.html type="info" content="These rules are enforced by <code>plugin_runner/sandbox.py</code> in the <a href='https://github.com/canvas-medical/canvas-plugins'>Canvas Plugins repository</a>, which is the authoritative reference if you hit a restriction that isn't described here." %}

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
