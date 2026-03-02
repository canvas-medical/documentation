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

The lifecycle of a namespace depends on whether a plugin is creating a new namespace or joining an existing one.

#### Installation Flow

[//]: # (COMMENTED OUT SINCE JEKYLL DOESN'T SUPPORT MERMAID)
[//]: # (```mermaid)
[//]: # (flowchart TD)
[//]: # (    A[Plugin Installation Begins] --> B{Access level?})
[//]: # ()
[//]: # (    B -->|read_write| C{Namespace exists?})
[//]: # (    B -->|read| D{Namespace exists?})
[//]: # ()
[//]: # (    C -->|No| E[Create PostgreSQL Schema])
[//]: # (    E --> F[Generate Authentication Keys])
[//]: # (    F --> G[Store Keys as Plugin Secrets])
[//]: # (    G --> H[Create Custom Tables])
[//]: # (    H --> I[✅ Plugin Installed Successfully])
[//]: # ()
[//]: # (    C -->|Yes| J{Has valid read_write key?})
[//]: # (    J -->|Yes| K[Create Custom Tables])
[//]: # (    J -->|No| L[❌ Installation Fails])
[//]: # (    K --> I)
[//]: # ()
[//]: # (    D -->|No| M[❌ Installation Fails])
[//]: # (    D -->|Yes| N{Has valid access key?})
[//]: # (    N -->|Yes| O[Ready for Read Access])
[//]: # (    N -->|No| P[❌ Installation Fails])
[//]: # (    O --> I)
[//]: # (```)

<img src="/assets/images/sdk/custom-data/installation_flowchart.svg" width="80%">

#### Creating a New Namespace

The **first plugin** installed with a given namespace name automatically creates it. This happens when:

1. The manifest declares a `custom_data.namespace` that doesn't yet exist
2. The plugin declares `"access": "read_write"`

When the namespace is created:

1. **Schema Creation** - A PostgreSQL schema is created with the namespace name
2. **Key Generation** - Two authentication keys are generated:
   - `read_access_key` - Grants read-only access to the namespace
   - `read_write_access_key` - Grants full read/write access
3. **Secret Storage** - The keys are automatically stored as secrets in the creating plugin
4. **Table Creation** - Any CustomModel tables defined by the plugin are created

> **Note:** The creating plugin does not need to provide an access key—it generates the keys and is inherently trusted.

#### Joining an Existing Namespace

Subsequent plugins that want to access an existing namespace must:

1. **Obtain the access key** from the namespace creator (see [Discovering Access Keys](#discovering-access-keys))
2. **Declare the namespace** in their manifest with the appropriate access level
2. **Configure the secret** in using the `--secret` parameter during installation via the CLI.

The installation process validates the access key:

| Declared Access | Namespace Exists | Key Provided | Result |
|-----------------|------------------|--------------|--------|
| `read` | No | N/A | ❌ Installation fails |
| `read` | Yes | Valid `read_access_key` | ✅ Plugin installed with read access |
| `read` | Yes | Invalid or missing | ❌ Installation fails |
| `read_write` | No | N/A | ✅ Creates namespace and tables |
| `read_write` | Yes | Valid `read_write_access_key` | ✅ Plugin installed, tables created |
| `read_write` | Yes | Invalid or missing | ❌ Installation fails |

#### Discovering Access Keys

After the namespace is created, you can find the generated keys in the **Canvas admin UI**:

1. Navigate to **Settings → Plugins**
2. Find the plugin that created the namespace
3. Click to view plugin details
4. The `read_access_key` and `read_write_access_key` appear in the **Secrets** section

Share these keys securely with developers of other plugins that need access:

- Share `read_access_key` with plugins that only need to read data
- Share `read_write_access_key` with plugins that need to modify data

> **Important:** Store these keys in a secure location outside of Canvas. If the keys are accidentally removed from the manifest's `secrets` array, they will be deleted upon the next installation.

#### Configuring Plugin Access

Each plugin that joins a namespace must:

1. **Declare the namespace** in `CANVAS_MANIFEST.json`
2. **Include the secret name** in the manifest's `secrets` array
3. **Provide the access key** during installation

```json
{
  "secrets": ["namespace_read_write_access_key"],
  "custom_data": {
    "namespace": "acme_corp__shared_data",
    "access": "read_write"
  }
}
```

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
  "secrets": ["namespace_read_write_access_key"],
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
| Query CustomAttributes                   | ✅      | ✅            |
| Query AttributeHubs                      | ✅      | ✅            |
| Query CustomModels                       | ✅      | ✅            |
| Set/delete CustomAttributes              | ❌      | ✅            |
| Create/update/delete AttributeHubs       | ❌      | ✅            |
| Create/update/delete CustomModel records | ❌      | ✅            |
| Create/update custom database tables     | ❌      | ✅            |

### Example: Sharing CustomAttributes

CustomAttributes attach key-value data to existing Canvas models (Patient, Staff, etc.).

**Plugin A (write access) - Sets patient attributes:**

```python
# CANVAS_MANIFEST.json: "access": "read_write"
from canvas_sdk.v1.data import Patient, ModelExtension

class CustomPatient(Patient, ModelExtension):
    pass

patient_id = 123
patient = CustomPatient.objects.get(id=patient_id)
patient.set_attribute("risk_score", 85)
patient.set_attribute("care_program", "diabetes_management")
```

**Plugin B (read access) - Reads patient attributes:**

```python
# CANVAS_MANIFEST.json: "access": "read"
from canvas_sdk.v1.data import Patient, ModelExtension

class CustomPatient(Patient, ModelExtension):
    pass

patient_id = 123
patient = CustomPatient.objects.with_only(
    attribute_names=["risk_score", "care_program"]
).get(id=patient_id)

risk_score = patient.get_attribute("risk_score")  # 85
care_program = patient.get_attribute("care_program")  # "diabetes_management"
```

### Example: Sharing AttributeHubs

AttributeHubs store standalone key-value data not attached to Canvas models.

**Plugin A (write access) - Creates configuration hub:**

```python
# CANVAS_MANIFEST.json: "access": "read_write"
from canvas_sdk.v1.data import AttributeHub

# Create a configuration hub
config = AttributeHub.objects.create(type="clinic_config", id="main")
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

```python
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

```python
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

```python
from canvas_sdk.v1.data.base import NamespaceWriteDenied

try:
    hub.set_attribute("key", "value")
except NamespaceWriteDenied as e:
    # "Write operation denied: namespace 'acme_corp__shared_data' is read-only.
    #  Plugin must declare 'read_write' access to perform write operations."
    log.error(f"Cannot write to shared namespace: {e}")
```

### Troubleshooting

**"NamespaceAccessError: secret 'read_access_key' is not configured"**
- Add the secret name to the `secrets` array in your manifest
- Ensure the secret has a value set in the Canvas UI

**"NamespaceAccessError: the key value is not a valid access key"**
- Verify you're using the correct key from the namespace owner
- Check that the key hasn't been regenerated

**"NamespaceAccessError: requests 'read_write' access but key only grants 'read'"**
- You're using `read_access_key` but declared `"access": "read_write"`
- Either change to `read_write_access_key` or change access to `"read"`

**"NamespaceWriteDenied: namespace is read-only"**
- Your plugin has `"access": "read"` but is attempting a write operation
- Change to `"access": "read_write"` and use `read_write_access_key`

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


class CustomStaff(Staff, ModelExtension):
    pass


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
        staff = CustomStaff.objects.with_only(
            attribute_names=["specialty", "accepting_patients"]
        ).get(id=staff_id)

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
- [CustomAttributes](/sdk/custom-data-custom-attributes/) - Flexible key-value storage
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [CustomModels](/sdk/custom-data-custom-models/) - Django models for structured data
- [Testing Utils](/sdk/testing-utils/) - Factories for testing custom data
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Simple API](/sdk/handlers-simple-api-http) - HTTP API handlers
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration

<br/>
<br/>
<br/>
