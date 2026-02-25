---
title: "Custom Data"
---

## Overview

The Canvas SDK provides three techniques for storing custom data in your plugins, allowing you to extend existing models, create flexible key-value stores, 
or define fully structured data models with relationships among entities:

1. **[CustomAttributes for SDK Models](/sdk/custom-data-custom-attributes/)** - Augment existing SDK data models (like Patient or Staff) with flexible key-value attributes
2. **[Custom Data Models](/sdk/custom-data-custom-models/)** - Extend the Canvas data model by adding fully structured models with typed fields and relationships
3. **[AttributeHubs](/sdk/custom-data-attribute-hubs/)** - Store arbitrary key-value pairs and JSON data independently of the Canvas data model

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

### Custom Data Models

Use this when you need structured, typed data with relationships and normalized data.

**Best for:**
- Associating new tables to existing Canvas tables
- Creating new associations among Canvas tables
- Complex domain models
- Data requiring validation and normalization
- Relational data with foreign keys
- Performance-critical queries

**Example use cases:**
- Provider specialties and certifications
- Linking `Staff` to `Note` creating a `supervising_provider` association
- Custom workflows and forms
- Integration-specific data structures
- Practice-specific business operation concepts and logic

**CustomModels may build around and be related to core SDK models using proxies.**

[Learn more about Custom Data Models →](/sdk/custom-data-custom-models/)

### AttributeHubs

AttributeHubs provide a key/value and document store free from the burden of defining any schema or linking to Canvas models.
They are for storing irregular or unstructured information that doesn't have a natural home. Whereas CustomAttributes and 
CustomModels build upon the Canvas data model, AttributeHubs allow easy, standalone persistence of information. 
Use this when you need to store data that doesn't naturally belong to any existing or imagined model. 

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


---

## Caching

If your use case represents transient data that should expire via TTL, use the
[Caching API](/sdk/caching) instead of the Custom Data features.

---

## Data Privacy and Plugin Isolation

All custom data created by a plugin—whether using CustomAttributes, AttributeHubs, or Custom Data Models—is scoped to a namespace. 
This isolation ensures that plugins cannot directly access or modify another plugin's data, maintaining security and data integrity 
across the system. 

Plugins may share data in two ways:
* By explicit co-location within a namespace, allowing direct database access
* By publishing [Simple API](/sdk/handlers-simple-api-http) endpoints

[Learn more about data sharing](/sdk/custom-data-sharing-data)

### Data Isolation

**CustomAttributes** attached to SDK models (like Patient or Staff) are scoped to the plugin's namespace. Custom attributes live within
a namespace and are only visible to plugins co-located within the namespace, even when attached to the same core model instance.

```python
# In one plugin and namespace
from my_plugin.models.proxy import StaffProxy
staff = StaffProxy.objects.get(id="abc")
staff.set_attribute("specialty", "Cardiology")  # Only accessible within "my_plugin"
```
```python
# In another plugin and different namespace
from your_plugin.models.proxy import StaffProxy
staff = StaffProxy.objects.get(id="abc")
staff.get_attribute("specialty")  # Returns None - cannot see "my_plugin" data
staff.set_attribute("specialty", "Cardiac")  # Creates separate attribute in "your_plugin"
```

**AttributeHubs** similarly store data within the plugin's namespace and are not accessible to other plugins in other namespaces.

**Custom Data Models** created by a plugin exist within namespaces. Tables and data are completely isolated from other namespaces.

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

## Testing Custom Data

The Canvas SDK provides comprehensive testing utilities for all custom data approaches. 
See the [Testing Custom Data](/sdk/custom-data-testing/) guide for detailed examples and best practices.

---

### Sharing Data

Use APIs to make data available and accessible to and from other plugins and external services. See the
[Sharing Data](/sdk/custom-data-sharing-data/) guide for detailed examples and best practices.

---

## See Also

- [CustomAttributes on SDK Models](/sdk/custom-data-custom-attributes/) - Flexible key-value attributes
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Custom Data Models](/sdk/custom-data-custom-models/) - Structured models with relationships among entities
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data with other plugins and external services
- [Data Models](/sdk/data/) - Core SDK data models
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration
