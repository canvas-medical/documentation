------------------------------------------------------------------------

The Events API is responsible for defining, emitting, and handling
events throughout the system.

# Basic Usage

The interface for the `events` module consists of three primary
components:

-   The `Event` class for defining new types of events.
-   The `emit_event` function for emitting events to the rest of the
    system.
-   The `@handle_event` decorator for listening for events and handling
    them.

This pattern is simple, but powerful: it means that you can emit an
event from anywhere, allow handlers to interact with and modify the
event object, and use the result to influence behavior.

Here\'s an example that uses an event to allow other parts of the system
to change an outgoing message.

``` python
from canvas_core import events

# Define an event by subclassing Event.
class BeforeMessageSend(events.Event):
    """An event emitted just before sending a message."""

    message: str

# Listen for the event from anywhere in your code.
@events.handle_event(BeforeMessageSend)
def add_message_watermark(event: BeforeMessageSend) -> None:
    # Print the message as it was received.
    print(f"Original message: {event.message}")

    # Add a watermark to the message.
    event.message = f"{event.message} (sent from Canvas)"

# Emit the event wherever it makes sense.
def send_message(message: str) -> None:
    """Send a message."""
    message_event = events.emit_event(BeforeMessageSend, message=message)
    print(f"Sending message: {message_event.message}")
    # ...

send_message(message="Hello, world!")
# Original message: Hello world!
# Sending message: Hello world! (sent from Canvas)
```

# Defining Events

Events are simply Python classes that extend from `Event`.

The `Event` class is intentionally basic. By default, the `Event` class
simply assigns any keyword arguments received by the constructor to the
matching attribute annotated on the class. If the constructor receives
an argument that does not have a matching annotation on the `Event`
class, a `TypeError` is raised.

The rest is left up to you for maximum design flexibility.

Here\'s a basic recipe for implementing extensible validation (i.e.,
allowing event handlers in other parts of the system to weigh in on a
form submission):

``` python
from typing import Any
from collections import defaultdict
from canvas_core import events
from django import forms

class SignupFormSubmitted(events.Event):
    """An event for validating and cleaning signup data."""

    cleaned_data: dict[str, Any]
    error_messages: defaultdict[str, list[str]]

    def __init__(self, **attrs) -> None:
        super().__init__(**attrs)
        self.error_messages = defaultdict(list)

    def add_error(self, field_name: str, error_message: str) -> None:
        """Add an error to the form submission."""
        self.error_messages[field_name].append(error_message)


class SignupForm(forms.Form):
    """A simple signup form."""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self) -> dict[str, Any]:
        """Clean and validate the form input.

        Returns:
            cleaned_data: A dict fo cleaned form input.

        Raises:
            ValidationError if the form input is invalid.
        """
        cleaned_data = super().clean()

        # Emit the event to allow handlers to weigh in on cleaned data.
        signup_submitted = events.emit_event(SignupFormSubmitted, cleaned_data=cleaned_data)
        cleaned_data = signup_submitted.cleaned_data
        error_messages = signup_submitted.error_messages

        # Add errors to the form.
        for field_name, error_message in error_messages.items():
            self.add_error(field_name, error_message)

        return cleaned_data


# Elsewhere in the codebase, we can handle the SignupFormSubmitted event.
@events.handle_event(SignupFormSubmitted)
def validate_email(event: SignupFormSubmitted) -> None:
    """Validate that the email address is owned by the company."""
    if not event.cleaned_data["email"].endswith("@mycompany.com"):
        event.add_error("email", "Must be a company email.")


@events.handle_event(SignupFormSubmitted)
def validate_password(event: SignupFormSubmitted) -> None:
    """Validate that the password meets the minimum complexity requirements."""
    if len(event.cleaned_data["password"]) < 8:
        event.add_error("password", "Must be at least 8 characters.")
```

# Emitting Events

To emit an event, simply call `emit_event` with the `Event` class as the
first parameter:

``` python
from canvas_core import events

class CustomEvent(events.Event):
    pass

events.emit_event(CustomEvent)
```

If your event has annotations, any additional keyword arguments to
`emit_event` are passed along to the `Event` constructor:

``` python
from canvas_core import events

class CustomEvent(events.Event):
    argument: str

events.emit_event(CustomEvent, argument="hello world!")
```

The `emit_event` function returns an instance of the `Event` after all
handlers have responded, allowing handlers to influence the behavior of
the emitter.

``` python
from canvas_core import events

class CustomEvent(events.Event):
    argument: str

@events.handle_event(CustomEvent)
def handle_custom_event(event: CustomEvent) -> None:
    print(event.argument)
    event.argument = "hello new world!"

custom_event = events.emit_event(CustomEvent, argument="hello world!")
# hello world!
print(custom_event.argument)
# hello new world!
```

# Handling Events

Events can be handled anywhere in the system by using the
`@handle_event` decorator on any function that accepts an `Event`:

``` python
from canvas_core import events

class MyEvent(events.Event):
    pass

@events.handle_event(CustomEvent)
def handle_my_event(event: CustomEvent) -> None:
    print("MyEvent fired!")
```

## Performance Considerations

Event handling is synchronous, and therefore it\'s recommended to write
event handlers with performance top-of-mind.

If you have a long-running or particularly resource-intensive task that
you need to perform in response to an event, it\'s recommended to use
the Background Jobs API to execute it asynchronously.

## Execution Order

It\'s important to note that execution order of event handlers is not
guaranteed, and you should not rely on the order even if it seems
predictable.

More concretely, it\'s important to avoid writing handlers in an
interdependent way. If you have multiple things that need to happen in
sequence, it\'s best to either:

1.  Write a single handler to execute your steps in sequence, or
2.  Emit custom events for each step, and write handlers to respond
    appropriately.

Keep in mind, however, that handlers can be written for any event in the
system (including your custom events!) and so it\'s possible for the
latter approach to cause issues if you\'re not expecting interaction
from other parts of the system.

## Error Handling

Exceptions raised in event handlers are handled robustly, meaning that
raising an exception in a handler will not prevent the execution of
other event handlers listening for the same event(s).

Exceptions raised by handlers are logged as errors (including a
traceback), reported to internal error reporting systems, but it is
ultimately left up to the author to handle and resolve errors properly!

# The `origin` Keyword

Finally, there is one special argument to `emit_event`, which is
`origin`.

The `origin` allows the emitter to specify *where* an event was emitted
from.

When emitting the same event from several places, it\'s recommended to
specify the `origin` so that handlers can scope their listening
appropriately:

``` python
from canvas_core import events

class CustomEvent(events.Event):
    argument: str

def custom_action_one() -> None:
    custom_event = events.emit_event(
        CustomEvent, origin=custom_action_one, argument="hello world!"
    )
    print(custom_event.argument)

def custom_action_two() -> None:
    custom_event = events.emit_event(
        CustomEvent, origin=custom_action_two, argument="hello world!"
    )
    print(custom_event.argument)

@events.handle_event(CustomEvent, origin=custom_action_one)
def handle_custom_action_one(event: CustomEvent) -> None:
    print(event.argument)
    event.argument = "hello new world!"

custom_action_one()
# hello world!
# hello new world!

custom_action_two()
# hello world!
# hello world!
```

# Tips & Best Practices

1.  Keep it simple! Not everything needs to emit an event. It\'s
    recommended to emit events only when you expect other parts of the
    system (that you may or may not control) to influence the behavior
    of whatever you\'re building.
2.  Instrumentation is king. Event-based systems can become complex and
    non-linear, so it\'s important that your event code is outfitted
    with appropriate logging and telemetry so that you can easily debug
    issues when they arise. See the Logging API and the Instrumentation
    API for more details.

# Events

The Events API emits a number of system-level events that can be used to
customize behavior.

## Record Lifecycle Events

The following events are emitted in response to database object
lifecycle events.

1.  `canvas_core.events.PreRecordCreate`{.interpreted-text
    role="py:class"}: emitted just before a new database object is
    created.
2.  `canvas_core.events.PostRecordCreate`{.interpreted-text
    role="py:class"}: emitted just after a new database object is
    created.
3.  `canvas_core.events.PreRecordUpdate`{.interpreted-text
    role="py:class"}: emitted just before an existing database object is
    updated. Contains a `diff` property with the change details.
4.  `canvas_core.events.PostRecordUpdate`{.interpreted-text
    role="py:class"}: emitted just after an existing database object is
    updated. Contains a `diff` property with the change details.
5.  `canvas_core.events.PreRecordDelete`{.interpreted-text
    role="py:class"}: emitted just before an existing database object is
    deleted.
6.  `canvas_core.events.PostRecordDelete`{.interpreted-text
    role="py:class"}: emitted just after an existing database object is
    deleted.

These records are emitted with the class of their database model as the
origin.

Note also that these events are generic, and can be parameterized with
their record type for stronger typing.

Here\'s an example of using the `PostRecordUpdate` event to log a
message when settings change.

``` python
from canvas_core import config, events, logging

logger = logging.get_logger(__name__)

Setting = config.get_setting_model()

@events.handle_event(events.PostRecordUpdate, origin=Setting)
def handle_setting_change(event: events.PostRecordUpdate[Setting]) -> None:
    """Log a message when a setting changes."""
    setting = event.record
    diff = event.diff

    # If the value wasn't changed, noop.
    if "value" not in diff:
        return

    # Get the old and new values from the diff.
    old_value, new_value = diff["value"]

    # Redact sensitive values.
    if setting.sensitive:
        old_value, new_value = "[REDACTED]", "[REDACTED]"

    # Log a message with the change details.
    logger.info("A setting was changed.", setting=setting.key, old_value=old_value, new_value=new_value)
```

# API Reference

::: {.automodule members=""}
canvas_core.events
:::
