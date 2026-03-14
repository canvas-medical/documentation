---
title: "Custom Data"
---

## Overview

The Canvas SDK provides two techniques for storing custom data in your plugins, allowing you to define fully structured
data models with relationships among entities, or create flexible key-value stores:

1. **[CustomModels](/sdk/custom-data-custom-models/)** - Build your own data model or expand the Canvas data model by adding fully structured models with typed fields and relationships
2. **[AttributeHubs](/sdk/custom-data-attribute-hubs/)** - Store arbitrary key-value pairs and JSON data independently of the Canvas data model

Each technique serves different use cases and provides different levels of structure and type safety. Both techniques may be used together.

## When to Use Each Technique

### CustomModels

Use this when you need structured, typed data with relationships and normalized data. CustomModels can also
extend existing SDK models (like Patient or Staff) with custom fields via `OneToOneField`.

**Best for:**
- Structured data with a stable, known schema
- Custom fields on existing SDK models (e.g., provider preferences, patient flags)
- Relationships between entities (foreign keys, join tables)
- Data requiring compound filtering, sorting, or aggregation
- Data consumed by reports or analytics

**Example use cases:**
- Provider specialties and certifications
- Adding practice-specific fields to patients or staff
- Linking `Staff` to `Note` creating a `supervising_provider` association
- Custom workflows and forms
- Integration-specific data structures
- Practice-specific business operation concepts and logic

[Learn more about CustomModels →](/sdk/custom-data-custom-models/)

### AttributeHubs

AttributeHubs provide a key/value and document store free from the burden of defining any schema or linking to Canvas models.
They are for storing irregular or unstructured information that doesn't have a natural home. Whereas
CustomModels build upon the Canvas data model, AttributeHubs allow easy, standalone persistence of information.
Use this when you need to store data that doesn't naturally belong to any existing or imagined model.

**Best for:**
- Cross-cutting state that spans multiple models (sync cursors, external IDs)
- One-off or small-collection configuration and state
- Data with no natural schema (varying fields per record)
- External system state tracking

**Example use cases:**
- API synchronization state
- External system identifiers
- Plugin configuration and feature flags

[Learn more about AttributeHubs →](/sdk/custom-data-attribute-hubs/)

For help choosing between these techniques, see [Design Considerations](/sdk/custom-data-design-considerations/).
For details on how multiple plugins can share a namespace using these keys, see the [Sharing Data](/sdk/custom-data-sharing-data/) guide.
For managing API tokens and other sensitive configuration, see [Managing Secrets](/sdk/secrets/).

## Caching

If your use case represents transient data that should expire via TTL, use the
[Caching API](/sdk/caching) instead of the Custom Data features.

## Data Privacy and Plugin Isolation

All custom data created by a plugin — whether using CustomModels or AttributeHubs — is scoped to a namespace.
This isolation ensures that plugins cannot directly access or modify another plugin's data, maintaining security and data integrity
across the system.

Plugins may share data in two ways:
* By explicit co-location within a namespace, allowing direct database access
* By publishing [Simple API](/sdk/handlers-simple-api-http) endpoints

[Learn more about data sharing](/sdk/custom-data-sharing-data)

### Data Isolation

**CustomModels** created by a plugin exist within namespaces. Tables and data are completely isolated from other namespaces.

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

**AttributeHubs** similarly store data within the plugin's namespace and are not accessible to plugins in other namespaces.

## Testing Custom Data

The Canvas SDK provides comprehensive testing utilities for all custom data approaches. 
See the [Testing Custom Data](/sdk/custom-data-testing/) guide for detailed examples and best practices.

## Sharing Data

Use APIs to make data available and accessible to and from other plugins and external services. See the
[Sharing Data](/sdk/custom-data-sharing-data/) guide for detailed examples and best practices.

## Read Replica Databases

All the data managed by plugin is available via the database read replica. To access it, alter the PostgreSQL
[search_path](https://www.postgresql.org/docs/18/ddl-schemas.html#DDL-SCHEMAS-PATH) to include the namespaces that you 
intend to query.

## See Also

- [CustomModels](/sdk/custom-data-custom-models/) - Structured models with relationships among entities
- [Extending SDK Models](/sdk/custom-data-extending-sdk-models/) - Proxy models, `related_name` namespacing, and referencing SDK models
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [Design Considerations](/sdk/custom-data-design-considerations/) - Choosing the right technique and avoiding anti-patterns
- [Transactions](/sdk/custom-data-transactions/) - All-or-nothing writes with `transaction.atomic()`
- [Testing Custom Data](/sdk/custom-data-testing/) - Testing utilities and examples
- [Sharing Data](/sdk/custom-data-sharing-data/) - Sharing data with other plugins and external services
- [Data Models](/sdk/data/) - Core SDK data models
- [Caching API](/sdk/caching) - Auto-expiring transient data
- [Canvas CLI](/sdk/canvas_cli/#simple-api-endpoints) - Simple API for sharing data between plugins
- [Secrets](/sdk/secrets/) - Managing API keys and sensitive configuration

<br/>
<br/>
<br/>
