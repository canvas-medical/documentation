---
title: "Data"
disable_anchorlist: true
---

The data module provides you with data to compute on. It provides curated,
secure access to both PHI (e.g. patient data) and non-PHI (e.g. staff and
practice-level data), representing the current state of your target Canvas
instance. The module's classes offer convenience methods and operators that
make business logic and clinical logic easy to express with standard
terminologies like ICD-10, SNOMED-CT, CPT, and the like.

Data module classes are Django ORM models, which allow easy retrieval of data
at runtime through Django's expressive [QuerySet API](https://docs.djangoproject.com/en/5.1/ref/models/querysets/).

The pages below provide listings of the models, their attributes, and examples of usage.

<div class="sdk-card-list">
{% for item in site.menus.data_module %}
    <a href="{{ item.url }}">
        <div class="sdk-card">
            <span class="cardHeading">{{ item.title }}</span>
            <p>{{ item.description }}</p>
        </div>
    </a>
{% endfor %}
</div>

<br/>
<br/>
<br/>
