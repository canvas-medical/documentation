---
title: "Coverage"
slug: "data-coverage"
excerpt: "Canvas SDK Coverage"
hidden: false
---

## Introduction

The `Coverage` model represents insurance coverage linked to [Patients](/sdk/data-patient/#patient). Coverages are linked to [Patient](/sdk/data-patient/#patient) instances, as well as `Transactor` instances, which represent the issuer for the corresponding coverage.

## Usage

The `Coverage` model can be used to find all of the coverages defined in a Canvas instance, whether overall or for a particular patient. For example, to find all of the current coverages for a patient, the `Patient.coverages` method can be used:

```python
>>> import arrow
>>> from canvas_sdk.v1.data.patient import Patient
>>> patient_1 = Patient.objects.get(id="a74592ae8a6c4d0ebe0799d3fb3713d1")
>>> patient_1_current_coverages = patient_1.coverages.filter(coverage_end_date__gt=arrow.now().date().isoformat())
>>> print([coverage.issuer.name for coverage in patient_1_current_coverages])
['AVALON HEALTHCARE SOLUTIONS CAPITAL BLUE CROSS']
```

Alternatively, to find all of the `Coverage` instances issed by a particular issuer/transactor, the `Transactor` model can be queried:

```python
>>> from canvas_sdk.v1.data.coverage import Coverage, Transactor
>>> transactor_1 = Transactor.objects.get(payer_id="AVA03")
transactor_coverages = Coverage.objects.filter(issuer=transactor_1)
>>> print(transactor_coverages)
<QuerySet [<Coverage: id=89793979-dbff-4a53-b928-75db973c2bdc>, <Coverage: id=423c0f77-8083-4cc1-8e29-2c7d348281e4>]>
>>>
```

## Filtering

The `filter` method can be used to filter by desired attributes. The following examples show commonly used operations to filter coverage data:

__Show a Patient's Coverages in order of Rank (Primary, Secondary, etc.)__

```python
>>> from canvas_sdk.v1.data.patient import Patient
>>> patient_1 = Patient.objects.get(id="aebe4d3f5d18410388dc69c4b5169fc3")
>>> patient_coverages = patient_1.coverages.all().order_by("coverage_rank")
>>> print([(coverage.issuer.name, coverage.coverage_rank,) for coverage in patient_coverages])
[('AVALON HEALTHCARE SOLUTIONS CAPITAL BLUE CROSS', 1), ('Blue Cross Blue Shield of Arizona Advantage', 2)]
```

__Find All Expired Coverages__

```python
>>> import arrow
>>> from canvas_sdk.v1.data.coverage import Coverage
>>> expired_coverages = Coverage.objects.filter(coverage_end_date__lt=arrow.now().date().isoformat())
>>> print([f"{coverage.issuer.name} expired {coverage.coverage_end_date.isoformat()}" for coverage in expired_coverages])
['Blue Cross Blue Shield of Arizona Advantage expired 2025-01-10']
```

## Attributes

### Coverage

### Transactor

### TransactorAddress

### TransactorPhone


## Enumeration types
