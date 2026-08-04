---
title: "Sharing Data"
slug: "custom-data-sharing-data"
---

Plugins can share data in two ways, depending on the relationship between the plugins:

| Approach | Use Case | Coupling |
|----------|----------|----------|
| **[Namespace Sharing](#namespace-sharing)** | Plugins owned by the same organization that need direct database access | Tight |
| **[API Sharing](#api-sharing)** | Plugins owned by different organizations, or when loose coupling is preferred | Loose |

## Namespace Sharing

Namespace sharing allows multiple plugins to read from and write to the same database tables. This is ideal for organizations that want to build smaller, focused plugins instead of a single monolithic plugin.
A plugin may reside within one namespace only. If it needs to access data from multiple namespaces,
then it must do so via API calls.

### When to Use Namespace Sharing

- Your organization owns multiple plugins that need to share data
- You want to break a large plugin into smaller, maintainable pieces
- You need direct database access for performance
- You want to avoid the overhead of API calls between plugins

### Namespace Lifecycle

For a full overview of how namespaces are created, managed, and cleaned up during development, see [Namespace Lifecycle](/sdk/custom-data-namespace-lifecycle/).

### Discovering Access Keys

After the namespace is created, you can find the generated keys in the **Canvas admin UI**:

1. Navigate to **Settings → Plugins**
2. Find the plugin that created the namespace
3. Click to view plugin details
4. The `namespace_read_access_key` and `namespace_read_write_access_key` appear in the **Secrets** section

Share these keys securely with developers of other plugins that need access:

- Share `namespace_read_access_key` with plugins that only need to read data
- Share `namespace_read_write_access_key` with plugins that need to modify data

> **Important:** Store these keys in a secure location outside of Canvas, such as 1Password. Removing a key from the manifest's `secrets` array does **not** delete the stored value — it is preserved. However, **uninstalling the plugin deletes its secrets**, including the namespace keys. Because the namespace itself survives an uninstall, a later reinstall will not regenerate the keys, so a copy kept outside Canvas is the only way to restore access. See [Uninstalling and Reinstalling a Plugin](/sdk/custom-data-namespace-lifecycle/#uninstalling-and-reinstalling-a-plugin).

### Pre-Supplying Keys at Creation

By default, Canvas auto-generates the two access keys the first time a `read_write` plugin creates a namespace. You can also **supply both keys yourself** at that first install — pass them through the same `--secret` mechanism used for joins:

```bash
canvas install my_plugin \
  --host demo.canvasmedical.com \
  --secret namespace_read_access_key=<your-read-key> \
  --secret namespace_read_write_access_key=<your-read-write-key>
```

When both keys are present at the install that creates the namespace, those plaintext values are what get hashed into the namespace's authentication table — Canvas does **not** generate fresh UUIDs.

Rules:

- Supply **both** keys for your values to take effect. If you provide only one — or leave either value empty — Canvas silently ignores the supplied keys and auto-generates both instead. The install still succeeds; it does not fail.
- Format is not enforced, but UUID4s are conventional.
- This only applies to the install that **creates** the namespace. Subsequent joins validate against whatever was written at creation time.
- If you supply neither key, behavior is unchanged: Canvas generates both for you.

When to use this:

- You want the keys to be known and persisted outside Canvas before the namespace exists (for example, a deployment system that needs to seed sibling plugins with the same key without round-tripping through the Admin UI).
- You're restoring access to a previously-dropped namespace and want to reuse known key values.
- You want deterministic key values across test runs in CI.

### Configuring Plugin Access

Each plugin that joins a namespace must:

1. **Declare the namespace** in `CANVAS_MANIFEST.json`
2. **Include the access key name** in the manifest's `variables` array
3. **Provide the access key** during installation

```json
{
  "variables": [
    {"name": "namespace_read_write_access_key", "sensitive": false}
  ],
  "custom_data": {
    "namespace": "acme_corp__shared_data",
    "access": "read_write"
  }
}
```

> Namespace access keys are declared with `"sensitive": false` so the value remains readable in the Admin UI's Secrets inline — that's the surface developers use to copy a key into a sibling plugin that joins the same namespace.

**Installing with the Canvas CLI (recommended):**

Provide the access key using the `--secret` flag:

```bash
canvas install my_plugin \
  --host demo.canvasmedical.com \
  --secret namespace_read_write_access_key=3b35fad9-6462-4e83-83f5-c0e4bde49b71
```

**Alternative: Setting secrets via Admin UI:**

If you've already installed the plugin without the secret:

1. Go to **Settings → Plugins → Your Plugin → Secrets**
2. Set the `namespace_read_access_key` or `namespace_read_write_access_key` value
3. **Reinstall the plugin** to pick up the secret

### Manifest Configuration

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "1.0.0",
  "name": "my_plugin",
  "variables": [
    {"name": "namespace_read_write_access_key", "sensitive": false}
  ],
  "custom_data": {
    "namespace": "acme_corp__shared_data",
    "access": "read_write"
  }
}
```

**Namespace naming requirements:**
- Must contain `__` (double underscore) to separate organization from name
- Cannot use reserved PostgreSQL names (`public`, `pg_catalog`, etc.)
- Organizations and names must start with a letter

**Access levels:**
- `read` - Can only read data from the namespace
- `read_write` - Can read and write data, and create custom tables

### Permissions and Restrictions

| Permission                               | `read` | `read_write` |
|------------------------------------------|--------|--------------|
| Query AttributeHubs                      | ✅      | ✅            |
| Query CustomModels                       | ✅      | ✅            |
| Create/update/delete AttributeHubs       | ❌      | ✅            |
| Create/update/delete CustomModel records | ❌      | ✅            |
| Create/update custom database tables     | ❌      | ✅            |

### Example: Sharing AttributeHubs

AttributeHubs store standalone key-value data not attached to Canvas models.

**Plugin A (write access) - Creates configuration hub:**

```python
# CANVAS_MANIFEST.json: "access": "read_write"
from canvas_sdk.v1.data import AttributeHub

# Create or retrieve a configuration hub
config, created = AttributeHub.objects.get_or_create(type="clinic_config", id="main")
config.set_attribute("max_daily_appointments", 50)
config.set_attribute("appointment_duration_minutes", 30)
config.set_attribute("accepting_new_patients", True)
```

**Plugin B (read access) - Reads configuration:**

```python
# CANVAS_MANIFEST.json: "access": "read"
from canvas_sdk.v1.data import AttributeHub

config = AttributeHub.objects.with_only(
    attribute_names=["max_daily_appointments", "appointment_duration_minutes"]
).get(type="clinic_config", id="main")

max_appointments = config.get_attribute("max_daily_appointments")  # 50
duration = config.get_attribute("appointment_duration_minutes")  # 30
```

### Example: Sharing CustomModels

CustomModels allow you to define your own database tables with full ORM support.

**Important:** If multiple plugins need to share the same custom tables, each plugin must declare identical model definitions. The `read_write` plugin creates the tables; `read` plugins can query but not modify them.

**Shared model definition (must be identical in both plugins):**

```python
# models/specialty.py
from django.db import models
from canvas_sdk.v1.data.base import CustomModel

class Specialty(CustomModel):
    """A medical specialty that can be assigned to staff members."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    requires_referral = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
```

**Plugin A (write access) - Creates and manages specialties:**

```python?partial=true
# CANVAS_MANIFEST.json: "access": "read_write"
from .models.specialty import Specialty

# Create specialties
cardiology = Specialty(
    name="Cardiology",
    description="Heart and cardiovascular system",
    requires_referral=True
)
cardiology.save()

dermatology = Specialty(
    name="Dermatology",
    description="Skin conditions",
    requires_referral=False
)
dermatology.save()
```

**Plugin B (read access) - Queries specialties:**

```python?partial=true
# CANVAS_MANIFEST.json: "access": "read"
from .models.specialty import Specialty

# Query specialties (read operations work)
referral_specialties = Specialty.objects.filter(requires_referral=True)

for specialty in referral_specialties:
    print(f"{specialty.name}: {specialty.description}")

# Write operations raise NamespaceWriteDenied
specialty = Specialty.objects.first()
specialty.description = "Updated"
specialty.save()  # Raises NamespaceWriteDenied!
```

### Error Handling

When a plugin with `read` access attempts a write operation, a `NamespaceWriteDenied` exception is raised:

```python?partial=true
from canvas_sdk.v1.data.base import NamespaceWriteDenied

try:
    hub.set_attribute("key", "value")
except NamespaceWriteDenied as e:
    # "Write operation denied: namespace 'acme_corp__shared_data' is read-only.
    #  Plugin must declare 'read_write' access to perform write operations."
    log.error(f"Cannot write to shared namespace: {e}")
```

### Troubleshooting

**"NamespaceAccessError: secret 'namespace_read_access_key' is not configured"**
- Add the secret name to the `secrets` array in your manifest
- Ensure the secret has a value set in the Canvas UI

**"NamespaceAccessError: the key value is not a valid access key"**
- Verify you're using the correct key from the namespace owner
- Check that the key hasn't been regenerated

**"NamespaceAccessError: requests 'read_write' access but key only grants 'read'"**
- You're using `namespace_read_access_key` but declared `"access": "read_write"`
- Either change to `namespace_read_write_access_key` or change access to `"read"`

**"NamespaceWriteDenied: namespace is read-only"**
- Your plugin has `"access": "read"` but is attempting a write operation
- Change to `"access": "read_write"` and use `namespace_read_write_access_key`

## API Sharing

API sharing is the recommended approach when:

- Plugins are owned by different organizations
- You want loose coupling between plugins
- You need fine-grained control over what data is exposed
- You want to version your data interface independently

### Example: Exposing Provider Profile Data

```python
from canvas_sdk.handlers.simple_api import SimpleAPI, APIKeyCredentials, api
from canvas_sdk.effects.simple_api import JSONResponse
from canvas_sdk.v1.data import Staff, ModelExtension
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import BooleanField, DO_NOTHING, OneToOneField, TextField


class CustomStaff(Staff, ModelExtension):
    pass


class StaffProfile(CustomModel):
    staff = OneToOneField(
        CustomStaff, to_field="dbid", on_delete=DO_NOTHING,
        related_name="profile"
    )
    specialty = TextField()
    accepting_patients = BooleanField(default=True)


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
        staff = CustomStaff.objects.select_related("profile").get(id=staff_id)

        # Explicitly choose what data to expose
        profile = {
            "staff_id": staff.id,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "specialty": staff.profile.specialty,
            "accepting_patients": staff.profile.accepting_patients
        }

        return [JSONResponse(profile)]
```

### Consuming Shared Data from Another Plugin

```python
from canvas_sdk.effects import Effect
from canvas_sdk.effects.simple_api import Response, JSONResponse
from canvas_sdk.handlers.simple_api import SimpleAPI, api
from canvas_sdk.utils import Http


class MyAPI(SimpleAPI):
    PREFIX = "/retrieve"

    @api.get("/profile_for_staff/<staff_id>")
    def get_single_profile_via_api(self) -> list[Response | Effect]:
        staff_id = self.request.path_params["staff_id"]
        canvas_host = f"{self.environment['CUSTOMER_IDENTIFIER']}.canvasmedical.com"
        token = self.secrets["profile_api_token"]

        other_plugin_api = f"https://{canvas_host}/plugin-io/api/other_plugin/staff-profiles/{staff_id}"
        http = Http()
        response = http.get(other_plugin_api, headers={"Authorization": token})
        return [JSONResponse(response.json())]
```

### API Sharing Best Practices

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

## Choosing Between Namespace and API Sharing

| Factor               | Namespace Sharing        | API Sharing             |
|----------------------|--------------------------|-------------------------|
| **Ownership**        | Same organization        | Different organizations |
| **Coupling**         | Tight                    | Loose                   |
| **Performance**      | Direct DB access         | HTTP overhead           |
| **Schema Evolution** | Coordinated updates      | Independent versioning  |
| **Access Control**   | Binary (read/read_write) | Fine-grained            |
| **Setup Complexity** | Lower                    | Higher                  |

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Introduction to custom data storage
- [Namespace Lifecycle](/sdk/custom-data-namespace-lifecycle/) - Managing namespaces during development
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [CustomModels](/sdk/custom-data-custom-models/) - Django models for structured data
- [Testing Utils](/sdk/testing-utils/) - Factories for testing custom data
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Simple API](/sdk/handlers-simple-api-http) - HTTP API handlers
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration

<br/>
<br/>
<br/>
