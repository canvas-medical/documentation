---
title: "Design Considerations"
slug: "custom-data-design-considerations"
---

Choosing the right storage technique prevents performance problems, data inconsistencies, and unnecessary code complexity
down the road. This page describes common anti-patterns for each technique and recommends alternatives.

For an overview of all three techniques, see the [Custom Data Overview](/sdk/custom-data/).

## CustomAttributes — When to Reconsider

CustomAttributes store key-value pairs in an [EAV](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model)
table. Each attribute is a separate row joined to the parent model. This is lightweight for a handful of independent
metadata fields but breaks down when used beyond that scope.

### Building a shadow schema

If you find yourself setting 5+ related attributes on the same model instance — for example, `street`, `city`,
`state`, `zip`, and `country` on a Patient — you are recreating a table row across separate EAV entries. Compound
queries like "patients where `risk_score > 80 AND care_program = 'diabetes' AND language = 'Spanish'`" require a
separate JOIN per condition, and performance degrades linearly with each additional filter.

**Use instead:** A [CustomModel](/sdk/custom-data-custom-models/) with typed, indexed columns handles compound
queries in a single table scan.

### Encoding relationships as strings

Storing `patient.set_attribute("referring_provider_id", "abc123")` loses JOINs, reverse lookups, `select_related`,
and referential integrity. You can't traverse the relationship with Django's ORM — every lookup requires manual
code to resolve the string ID.

**Use instead:** A [CustomModel](/sdk/custom-data-custom-models/) with a `ForeignKey` gives you ORM relationship
traversal, reverse lookups via `related_name`, and `select_related`/`prefetch_related` for efficient loading.

### High-write-frequency counters

Each `set_attribute` call performs a full `INSERT ... ON CONFLICT DO UPDATE`. For a counter incremented on every
event, this is heavier than necessary.

**Use instead:** A [CustomModel](/sdk/custom-data-custom-models/) with an integer field supports atomic
increments via `Model.objects.filter(...).update(counter=F('counter') + 1)` — a single SQL statement with no
read required.

### Data consumed by reports or analytics

CustomAttributes live in an EAV table. Extracting a "flat" view for analytics requires pivoting rows into columns,
which is awkward and slow in SQL. Downstream systems expecting conventional table structures will struggle.

**Use instead:** [CustomModel](/sdk/custom-data-custom-models/) columns map directly to report columns with no
transformation needed.

---

## AttributeHubs — When to Reconsider

AttributeHubs use the same EAV storage as CustomAttributes but are standalone — not attached to any Canvas model.
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

---

## CustomModels — When to Reconsider

CustomModels create real database tables with typed columns. They are the most powerful option but carry a
commitment: tables can be added but never dropped via the SDK, and fields can be added but never altered or
removed.

### Simple metadata on existing models

Don't create a `PatientFlags` CustomModel with a `OneToOneField` to Patient just to store
`is_vip = BooleanField()`. The table, foreign key, and model definition are overhead for what a single
`patient.set_attribute("is_vip", True)` accomplishes with no schema.

**Use instead:** [CustomAttributes](/sdk/custom-data-custom-attributes/) for a small number of independent
metadata fields on existing SDK models.

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

---

## Quick Reference

| Situation | Recommended Approach |
|-----------|---------------------|
| A few metadata flags on Patient or Staff | CustomAttributes |
| Provider preferences (notification settings, display options) | CustomAttributes |
| Rapid prototyping before committing to a schema | CustomAttributes |
| API sync cursors, external system state | AttributeHub |
| Plugin configuration or feature flags | AttributeHub |
| One-off or small-collection key-value data unrelated to a Canvas model | AttributeHub |
| Structured entities with a stable, known schema | CustomModel |
| Relationships between entities (foreign keys, join tables) | CustomModel |
| Data requiring compound filtering, sorting, or aggregation | CustomModel |
| Data consumed by reports or analytics | CustomModel |
| High-write-frequency counters or accumulators | CustomModel |
| Short-lived data that should auto-expire | [Caching API](/sdk/caching) |

## See Also

- [Custom Data Overview](/sdk/custom-data/) - Introduction to custom data storage
- [CustomAttributes](/sdk/custom-data-custom-attributes/) - Flexible key-value storage
- [AttributeHubs](/sdk/custom-data-attribute-hubs/) - Standalone key-value storage
- [CustomModels](/sdk/custom-data-custom-models/) - Django models for structured data
- [Caching API](/sdk/caching) - Auto-expiring transient data

<br/>
<br/>
<br/>
