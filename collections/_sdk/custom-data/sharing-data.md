---
title: "Sharing Data"
slug: "custom-data-sharing-data"
---

To share data across plugins or to external services, a plugin must **explicitly expose an API** with appropriate 
authorization and access controls. This is done using the [Simple API](/sdk/canvas_cli/#simple-api-endpoints) feature.

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
        staff = StaffProxy.objects.with_only(attribute_names=["specialty", "accepting_patients"]).get(id=staff_id)

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
    PREFIX = "/retrieve"

@api.get("/profile_for_staff/<staff_id>")
def get_single_profile_via_api(self) -> list[Response | Effect]:
    staff_id = self.request.path_params["staff_id"]
    canvas_host = "demo.canvasmedical.com"
    token = 'abcd1234'

    other_plugin_api = f"https://{canvas_host}/plugin-io/api/other_plugin/staff_profile/{staff_id}"
    http = Http()
    response = http.get(other_plugin_api, headers={"Authorization": f"{token}"})
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

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Introduction to custom data storage
- [CustomAttributes](/sdk/custom-data-custom-attributes/) - Flexible key-value storage
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Custom Models](/sdk/custom-data-custom-models/) - Django models for structured data
- [Testing Utils](/sdk/testing-utils/) - Factories for testing custom data
- [Effects](/sdk/effects/) - Effects for manipulating data
