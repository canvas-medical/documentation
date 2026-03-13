---
title: "Design Considerations"
slug: "custom-data-design-considerations"
---

Choosing the right storage technique prevents performance problems, data inconsistencies, and unnecessary code complexity
down the road. This page describes common anti-patterns for each technique and recommends alternatives.

For an overview of available techniques, see the [Custom Data Overview](/sdk/custom-data/).

## Extending SDK Models with Custom Data

To attach custom fields to existing SDK models (Patient, Staff, etc.), use a
[CustomModel](/sdk/custom-data-custom-models/) with a `OneToOneField` pointing at the SDK model.
This gives you typed, indexed columns with full ORM support — `select_related`, reverse lookups
via `related_name`, and compound filtering in a single query.

```python
from canvas_sdk.v1.data import Patient, ModelExtension
from canvas_sdk.v1.data.base import CustomModel
from django.db.models import BooleanField, DO_NOTHING, IntegerField, OneToOneField, TextField


class CustomPatient(Patient, ModelExtension):
    pass

class PatientProfile(CustomModel):
    patient = OneToOneField(
        CustomPatient, to_field="dbid", on_delete=DO_NOTHING,
        related_name="profile"
    )
    preferred_language = TextField()
    risk_score = IntegerField()
    is_vip = BooleanField()
```

CustomModels with `OneToOneField` are preferred because they offer typed columns, indexing, compound queries,
and a schema that is visible and self-documenting. See [Extending SDK Models](/sdk/custom-data-extending-sdk-models/)
for details on proxy models and `related_name` namespacing.

For truly simple, one-off metadata that doesn't justify a table (e.g., a single configuration flag),
an [AttributeHub](/sdk/custom-data-attribute-hubs/) can be a lighter-weight alternative.

## AttributeHubs — When to Reconsider

AttributeHubs use EAV (entity-attribute-value) storage and are standalone — not attached to any Canvas model.
They are convenient for one-off state and configuration, but the same EAV limitations apply when used at scale.

### Modeling entities with relationships

If you have "departments" and need to assign staff to them, encoding `staff_id` as a string attribute means no
JOINs, no referential integrity, and no cascade behavior. The plugin must manually maintain consistency.

**Use instead:** [CustomModels](/sdk/custom-data-custom-models/) with `ForeignKey` fields and junction tables
handle relationships naturally, with ORM-level traversal and `prefetch_related` support.

### Large homogeneous collections

Storing thousands of hubs of `type="patient_visit"` where you need to filter, sort, or paginate across them
becomes expensive. Each filter condition requires a JOIN to the attribute table.

**Use instead:** A [CustomModel](/sdk/custom-data-custom-models/) with typed, indexed columns. Filtering, sorting, and pagination use
standard SQL operations.

### Data requiring aggregation

Trying to SUM, AVG, or COUNT across AttributeHub attributes requires joining to the attribute table and selecting
the correct typed column (`int_value`, `decimal_value`, etc.) per attribute name. This is fragile and slow.

**Use instead:** [CustomModel](/sdk/custom-data-custom-models/) columns make Django ORM aggregation
(`annotate`, `aggregate`) straightforward.

### Data with a consistent schema

If every hub of a given `type` has the same set of attributes, you've designed a schema — just without enforcement
or indexes. You're paying the cost of EAV without the benefit of flexibility.

**Use instead:** A [CustomModel](/sdk/custom-data-custom-models/) gives you type safety, column-level indexes,
and cleaner queries.

## CustomModels — When to Reconsider

CustomModels create real database tables with typed columns. They are the most powerful option but carry a
commitment: tables can be added but never dropped via the SDK, and fields can be added but never altered or
removed.

### Simple metadata on existing models

For a small number of independent metadata fields on an SDK model (e.g., a single `is_vip` flag on
Patient), a full CustomModel with `OneToOneField` is the recommended approach — it gives you typed
columns, indexing, and compound queries. However, if the overhead of a table feels excessive for
truly one-off data, an [AttributeHub](/sdk/custom-data-attribute-hubs/) keyed by entity type and ID
can serve as a lightweight alternative.

### Highly dynamic or schemaless data

If every record has different fields — for example, caching responses from external APIs where the payload
varies per endpoint — a CustomModel forces a rigid schema. You'll accumulate nullable columns for each
variation, and fields can never be dropped.

**Use instead:** [AttributeHubs](/sdk/custom-data-attribute-hubs/) for truly schemaless data, or a CustomModel
with a single `JSONField` if you still want a table but need flexible contents.

### Ephemeral data

CustomModel tables are permanent. Once created, they cannot be dropped via the SDK. For short-lived data
like session tokens, rate-limit windows, or temporary processing state, a persistent table is the wrong tool.

**Use instead:** The [Caching API](/sdk/caching) for data with a natural TTL. For semi-persistent unstructured
state, [AttributeHubs](/sdk/custom-data-attribute-hubs/) are lighter weight.

### Premature normalization

Don't create five interrelated CustomModels with foreign keys when the data is simple and queried infrequently.
Over-engineering the schema early is costly because tables cannot be dropped if you change your mind.

**Use instead:** Start with fewer models. A single `JSONField` column or an [AttributeHub](/sdk/custom-data-attribute-hubs/)
can hold loosely structured data until access patterns stabilize and justify a richer schema.

## Quick Reference

| Situation | Recommended Approach |
|-----------|---------------------|
| Custom fields on Patient, Staff, or other SDK models | CustomModel with `OneToOneField` |
| Provider preferences (notification settings, display options) | CustomModel with `OneToOneField` |
| API sync cursors, external system state | AttributeHub |
| Plugin configuration or feature flags | AttributeHub |
| One-off key-value data unrelated to a Canvas model | AttributeHub |
| Rapid prototyping before committing to a schema | AttributeHub |
| Structured entities with a stable, known schema | CustomModel |
| Relationships between entities (foreign keys, join tables) | CustomModel |
| Data requiring compound filtering, sorting, or aggregation | CustomModel |
| Data consumed by reports or analytics | CustomModel |
| High-write-frequency counters or accumulators | CustomModel |
| Short-lived data that should auto-expire | [Caching API](/sdk/caching) |

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Introduction to custom data storage
- [Extending SDK Models](/sdk/custom-data-extending-sdk-models/) - Proxy models and referencing SDK models
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [CustomModels](/sdk/custom-data-custom-models/) - Django models for structured data
- [Caching API](/sdk/caching) - Auto-expiring transient data

<br/>
<br/>
<br/>
