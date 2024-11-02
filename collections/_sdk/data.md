---
title: "Data"
---

The data module provides you with data to compute on. It provides curated,
secure access to both PHI (e.g. patient data) and non-PHI (e.g. staff and
practice-level data), representing the current state of your target Canvas
instance. The module's classes offer convenience methods and operators that
make business logic and clinical logic easy to express with standard
terminologies like ICD-10, SNOMED-CT, CPT, and the like.

For more detail, choose one of the data types below:

<ul>
    {% for item in site.menus.data_module %}
        <li><a href="{{ item.url }}">{{ item.title }}</a></li>
    {% endfor %}
</ul>
