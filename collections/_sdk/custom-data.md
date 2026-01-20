---
title: "Custom Data"
---

## Overview

The Canvas SDK provides three techniques for storing custom data in your plugins, allowing you to extend existing models, create flexible key-value stores, 
or define fully structured data models with relationships among entities:

1. **[CustomAttributes on Proxy Models](/sdk/custom-data-custom-attributes/)** - Extend existing SDK data models (like Patient or Staff) with flexible key-value attributes
2. **[AttributeHubs](/sdk/custom-data-attribute-hub/)** - Store arbitrary key-value data that doesn't belong to existing models
3. **[Custom Data Models](/sdk/custom-data-custom-models/)** - Define fully structured models with typed fields and relationships

Each technique serves different use cases and provides different levels of structure and type safety. All three techniques may be used together.

---

## When to Use Each Technique

### CustomAttributes for SDK Models

Use this when you need to add flexible data to existing SDK models without defining a schema.

**Best for:**
- Storing variable or configuration data on existing models
- Rapid prototyping
- Data that doesn't require strict typing
- Simple key-value associations with core models

**Example use cases:**
- Adding practice-specific flags or identifiers to patients
- Storing provider preferences
- Temporary or experimental data fields

[Learn more about CustomAttributes →](/sdk/custom-data-custom-attributes/)

### AttributeHubs

Use this when you need to store data that doesn't naturally belong to any existing model.

**Best for:**
- Cross-cutting concerns that span multiple models
- Temporary data storage
- External system state tracking
- Plugin-specific configuration

**Example use cases:**
- API synchronization state
- External system identifiers
- Plugin session data
- Feature flags

[Learn more about AttributeHubs →](/sdk/custom-data-attribute-hubs/)

### Custom Data Models

Use this when you need structured, typed data with relationships and normalized data.

**Best for:**
- Complex domain models
- Data requiring validation and normalization
- Relational data with foreign keys
- Performance-critical queries

**Example use cases:**
- Provider specialties and certifications
- Custom workflows and forms
- Integration-specific data structures
- Practice-specific business operation concepts and logic

**CustomModels may build around and be related to core SDK models using proxies.**

[Learn more about Custom Data Models →](/sdk/custom-data-custom-models/)

---

## Data Privacy and Plugin Isolation

All custom data created by a plugin—whether using CustomAttributes, AttributeHubs, or Custom Data Models—is **scoped to that plugin**. 
This isolation ensures that plugins cannot directly access or modify another plugin's data, maintaining security and data integrity across the system.

### Data Isolation

**CustomAttributes** attached to SDK models (like Patient or Staff) are scoped by plugin. Each plugin maintains its own separate namespace for custom attributes, even when attached to the same core model instance.

```python
# In one plugin
from my_plugin.models.proxy import StaffProxy
staff = StaffProxy.objects.get(id="abc")
staff.set_attribute("specialty", "Cardiology")  # Only accessible within "my_plugin"
```
```python
# In another plugin
from your_plugin.models.proxy import StaffProxy
staff = StaffProxy.objects.get(id="abc")
staff.get_attribute("specialty")  # Returns None - cannot see "my_plugin" data
staff.set_attribute("specialty", "Cardiac")  # Creates separate attribute in "your_plugin"
```

**AttributeHubs** similarly store data within the plugin's namespace and are not accessible to other plugins.

**Custom Data Models** created by a plugin exist in a plugin-specific namespace. Tables and data are completely isolated from other plugins.

```python
# In a plugin named "my_plugin": Creates a table "specialty" in the "my_plugin" namespace
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import TextField
class Specialty(CustomModel):
    name = TextField()
```

```python
# In a plugin named "your_plugin": Creates a table "specialty" in the "your_plugin" namespace
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import TextField
class Specialty(CustomModel):
    name = TextField()

# In "your_plugin": Cannot access the "my_plugin" Specialty model or data
```

### Sharing Data Between Plugins

To share data across plugins, a plugin must **explicitly expose an API** with appropriate authorization and access controls. 
This is done using the [Simple API](/sdk/canvas_cli/#simple-api-endpoints) feature.

This limitation exists to ensure data provenance, and reduce chance of dependency conflicts among plugins.

#### Example: Exposing Provider Profile Data

```python
from canvas_sdk.handlers.simple_api import SimpleAPI, APIKeyCredentials, api
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.v1.data import Staff, CustomAttributeMixin, CustomAttributeAwareManager


class StaffProxy(Staff, CustomAttributeMixin):
    class Meta:
        proxy = True
    objects = CustomAttributeAwareManager()


class ProfileAPI(SimpleAPI):
    """API to share staff profile data with authorized plugins."""

    PREFIX = "/staff-profiles"

    def authenticate(self, credentials: APIKeyCredentials) -> bool:
        """Validate API key from requesting plugin."""
        from hmac import compare_digest

        provided_key = credentials.key
        expected_key = self.secrets["profile_api_key"]

        return compare_digest(provided_key.encode(), expected_key.encode())

    @api.get("/<staff_id>")
    def get_profile(self):
        """Return staff profile data."""
        staff_id = self.request.path_params["staff_id"]
        staff = StaffProxy.objects.get(id=staff_id)

        # Explicitly choose what data to expose
        profile = {
            "staff_id": staff.id,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "specialty": staff.get_attribute("specialty"),
            "accepting_patients": staff.get_attribute("accepting_patients")
        }

        return [JSONResponse(profile)]
```

#### Consuming Shared Data from Another Plugin

```python
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.effects.simple_api import Response, JSONResponse
from canvas_sdk.handlers.simple_api import SimpleAPI, APIKeyCredentials, api
from canvas_sdk.utils import Http

class MyAPI(SimpleAPI):
    PREFIX = "/profile"

@api.get("/api/<staff_id>")
def get_single_profile_api(self) -> list[Response | Effect]:
    staff_id = self.request.path_params["staff_id"]
    canvas_host = "demo.canvasmedical.com"
    token = 'abcd1234'

    other_plugin_api = f"https://{canvas_host}/plugin-io/api/other_plugin/staff_profile/{staff_id}"
    http = Http()
    response = http.get(other_plugin_api,
             headers={"Authorization": f"{token}"})
    return [JSONResponse(response.json())]

```

### Data Sharing Best Practices

1. **Explicit Authorization** - Always require authentication for APIs that expose plugin data
2. **Minimal Exposure** - Only expose the specific data fields that are necessary
3. **Validate Requests** - Check permissions and validate that the requester should have access
4. **Document APIs** - Provide clear documentation for plugins that will consume your API
5. **Version APIs** - Use versioning (e.g., `/v1/profiles`) to allow API evolution
6. **Audit Access** - Log API access for security and debugging purposes
7. **Rate Limiting** - Consider implementing rate limits to prevent abuse

### Security Considerations

- **Never bypass plugin isolation** by attempting to access another plugin's database schema directly
- **Use API keys or tokens** stored in secrets, never hardcoded in plugin code
- **Implement proper error handling** that doesn't leak sensitive information
- **Consider PHI implications** when exposing patient-related data via APIs
- **Follow least privilege** principle - grant minimum necessary access

---

## Testing Custom Data

The Canvas SDK provides comprehensive testing utilities for all custom data approaches. See the [Testing Custom Data](/sdk/custom-data-testing/) guide for detailed examples and best practices.

---

## See Also

- [CustomAttributes on Proxy Models](/sdk/custom-data-custom-attributes/) - Flexible key-value attributes
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Custom Data Models](/sdk/custom-data-custom-models/) - Structured models with relationships among entities
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Data Models](/sdk/data/) - Core SDK data models
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration
