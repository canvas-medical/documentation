# Configuration Management

The Configuration Management API (\"config\", for short) provides a
simple interface for efficiently managing and retrieving key-value
settings, optionally related to arbitrary database entities.

## Basic Usage

``` python
>>> from canvas_core import config

# Create a global setting.
>>> config.set_setting("feature.enabled", "true")

# Retrieve a global setting.
>>> config.get_setting("feature.enabled")
"true"

# Create a subject-specific setting (i.e., a setting that applies to a
# specific database entity).
>>> user = get_current_user()
>>> config.set_setting("feature.enabled", "false", subject=user)

# Retrieve a subject-specific setting.
>>> config.get_setting("feature.enabled", subject=user)
"false"

# Retrieving a setting that does not exist will raise an error.
>>> config.get_setting("does.not.exist")
SettingDoesNotExist: Unable to find a value for 'does.not.exist' for subject None, and no global setting was found. Set a global value, or provide a default.

# If a setting may or may not exist, you can pass a default to avoid the error.
>>> config.get_setting("might.exist", default="default_value")
"default_value"

# Settings are always stored as strings, but they can be coerced by passing a callable.
>>> config.set_setting("feature.config_json", '{"hello": "world"}')
>>> config.get_setting("feature.config_json")
'{"hello": "world"}'
>>> import json
>>> config.get_setting("feature.config_json", coerce=json.loads)
{'hello': 'world'}

# Note, however, that default values are _not_ coerced.
>>> config.get_setting("feature.maybe_config_json", default='{"unchanged": "default"}', coerce=json.loads)
'{"unchanged": "default"}'

# Retrieve a setting in a cascading fashion based on subject relevance.
#
# For example, if a setting can apply to multiple subjects (and/or types of
# subjects), the most relevant value can be retrieved by proviving a lookup
# order.
#
# This is useful for creating cascading hierarchies of settings, e.g.
# user-specific settings that fall back to group-specific settings, which
# fall back to organization-specific settings, and finally to the global
# setting.
>>> organization = get_organization(1)
>>> group = get_group(1)
>>> user = get_user(1)
>>> config.set_setting("feature.setting", "organization_value", subject=organization)
# This will look for the value of "feature.setting" for the user, then for
# the group, then for the organization, ultimately returning the
# organization setting, since the other subjects did not have that setting
# defined for them.
>>> config.coalesce_setting("feature.setting", subjects=(user, group, organization))
```

## Caching

The settings cache is populated and invalidated for you automatically
(and optimally!), and it is not recommended to cache settings yourself.

## Best Practices

1.  Always namespace your settings! It\'s important to namespace your
    settings to avoid collisions with other module settings. For
    example, instead of `user_config`, use `feature_name.user_config`.
2.  Use purpose-built abstractions instead of this API directly. It\'s
    best to wrap the Configuration Management API in your own
    abstractions to provide the best configuration experience for your
    needs.

## API Reference

::: {.automodule members=""}
canvas_core.config
:::
