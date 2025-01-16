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

| Field Name                         | Type                                                  |
|------------------------------------|-------------------------------------------------------|
| id                                 | UUID                                                  |
| dbid                               | Integer                                               |
| created                            | DateTime                                              |
| modified                           | DateTime                                              |
| patient                            | [Patient](/sdk/data-patient/#patient)                 |
| guarantor                          | [Patient](/sdk/data-patient/#patient)                 |
| subscriber                         | [Patient](/sdk/data-patient/#patient)                 |
| patient_relationship_to_subscriber | [CoverageRelationshipCode](#coveragerelationshipcode) |
| issuer                             | [Transactor](#transactor)                             |
| id_number                          | String                                                |
| plan                               | String                                                |
| sub_plan                           | String                                                |
| group                              | String                                                |
| sub_group                          | String                                                |
| employer                           | String                                                |
| coverage_start_date                | Date                                                  |
| coverage_end_date                  | Date                                                  |
| coverage_rank                      | Integer                                               |
| state                              | [CoverageState](#coveragestate)                       |
| plan_type                          | [CoverageType](#coveragetype)                         |
| coverage_type                      | [TransactorCoverageType](#transactorcoveragetype)     |
| issuer_address                     | [TransactorAddress](#transactoraddress)               |
| issuer_phone                       | [TransactorPhone](#transactorphone)                   |
| comments                           | Text                                                  |
| stack                              | [CoverageStack](#coveragestack)                       |

### Transactor

| Field Name                   | Type                                                |
|------------------------------|-----------------------------------------------------|
| dbid                         | Integer                                             |
| payer_id                     | String                                              |
| name                         | String                                              |
| type                         | String                                              |
| transactor_type              | [TransactorType](#transactortype)                   |
| clearinghouse_payer          | Boolean                                             |
| institutional                | Boolean                                             |
| institutional_enrollment_req | Boolean                                             |
| professional                 | Boolean                                             |
| professional_enrollment_req  | Boolean                                             |
| era                          | Boolean                                             |
| era_enrollment_req           | Boolean                                             |
| eligibility                  | Boolean                                             |
| eligibility_enrollment_req   | Boolean                                             |
| workers_comp                 | Boolean                                             |
| secondary_support            | Boolean                                             |
| claim_fee                    | Boolean                                             |
| remit_fee                    | Boolean                                             |
| state                        | String                                              |
| description                  | String                                              |
| active                       | Boolean                                             |
| use_provider_for_eligibility | Boolean                                             |
| use_for_submission           | [Transactor](#transactor)                           |
| used_for_submission_by       | [Transactor](#transactor)[]                         |
| coverage_types               | [[TransactorCoverageType](#transactorcoveragetype)] |
| addresses                    | [TransactorAddress](#transactoraddress)[]           |
| coverages                    | [Coverage](#coverage)[]                             |
| phones                       | [TransactorPhone](#transactorphone)[]               |

### TransactorAddress

| Field Name  | Type                                       |
|-------------|--------------------------------------------|
| id          | UUID                                       |
| dbid        | Integer                                    |
| created     | DateTime                                   |
| modified    | DateTime                                   |
| line1       | String                                     |
| line2       | String                                     |
| city        | String                                     |
| district    | String                                     |
| state_code  | String                                     |
| postal_code | String                                     |
| use         | [AddressUse](#addressuse)                  |
| type        | [AddressType](#addresstype)                |
| longitude   | Float                                      |
| latitude    | Float                                      |
| start       | Date                                       |
| end         | Date                                       |
| country     | String                                     |
| state       | [AddressState](#addressstate)              |
| transactor  | [Transactor](#transactor)                  |
| coverages   | [Coverage](/sdk/data-coverage/#coverage)[] |

### TransactorPhone

| Field Name | Type                                       |
|------------|--------------------------------------------|
| id         | UUIDField                                  |
| dbid       | Integer                                    |
| created    | DateTime                                   |
| modified   | DateTime                                   |
| system     | String                                     |
| value      | String                                     |
| use        | [ContactPointUse](#contactpointuse)        |
| use_notes  | String                                     |
| rank       | Integer                                    |
| state      | [ContactPointState](#contactpointstate)    |
| transactor | [Transactor](#transactor)                  |
| coverages  | [Coverage](/sdk/data-coverage/#coverage)[] |

## Enumeration types

### AddressState

| Value      | Label   |
|------------|---------|
| active     | Active  |
| deleted    | Deleted |

### AddressType

| Value      | Label    |
|------------|----------|
| postal     | Postal   |
| physical   | Physical |
| both       | Both     |

### AddressUse

| Value      | Label |
|------------|-------|
| home       | Home  |
| work       | Work  |
| temp       | Temp  |
| old        | Old   |

### ContactPointState

| Value      | Label   |
|------------|---------|
| active     | Active  |
| deleted    | Deleted |

### ContactPointUse

| Value      | Label      |
|------------|------------|
| home       | Home       |
| work       | Work       |
| temp       | Temp       |
| old        | Old        |
| other      | Other      |
| mobile     | Mobile     |
| automation | Automation |

### CoverageStack

| Value   | Label   |
|---------|---------|
| IN_USE  | In use  |
| OTHER   | Other   |
| REMOVED | Removed |

### CoverageState

| Value      | Label   |
|------------|---------|
| active     | Active  |
| deleted    | Deleted |

### CoverageType

| Value        | Label                     |
|--------------|---------------------------|
| commercial   | Commercial                |
| workerscomp  | Workers Comp              |
| bcbs         | Blue Cross Blue Shield    |
| champus      | Tricare/Champus           |
| medicaid     | Medicaid                  |
| medicare     | Medicare                  |
| other        | Other                     |
| tpa          | Third Party Administrator |
| motorvehicle | Motor Vehicle             |
| lien         | Attorney/Lien             |
| pip          | Personal Injury           |

### CoverageRelationshipCode

| Value | Label                                                         |
|-------|---------------------------------------------------------------|
| 18    | Self                                                          |
| 01    | Spouse                                                        |
| 19    | Natural Child, insured has financial responsibility           |
| 43    | Natural Child, insured does not have financial responsibility |
| 17    | Step Child                                                    |
| 10    | Foster Child                                                  |
| 15    | Ward of the Court                                             |
| 20    | Employee                                                      |
| 21    | Unknown                                                       |
| 22    | Handicapped Dependent                                         |
| 39    | Organ donor                                                   |
| 40    | Cadaver donor                                                 |
| 05    | Grandchild                                                    |
| 07    | Niece/Nephew                                                  |
| 41    | Injured Plaintiff                                             |
| 23    | Sponsored Dependent                                           |
| 24    | Minor Dependent of a Minor Dependent                          |
| 32    | Mother                                                        |
| 33    | Father                                                        |
| 04    | Grandparent                                                   |
| 53    | Life Partner                                                  |
| 29    | Significant Other                                             |
| G8    | Other                                                         |

### TransactorCoverageType

| Value      | Label                                  |
|------------|----------------------------------------|
| ANNU       | annuity policy                         |
| AUTOPOL    | automobile                             |
| CHAR       | charity program                        |
| COL        | collision coverage policy              |
| CRIME      | crime victim program                   |
| DENTAL     | dental care policy                     |
| DENTPRG    | dental program                         |
| DIS        | disability insurance policy            |
| DISEASE    | disease specific policy                |
| DRUGPOL    | drug policy                            |
| EAP        | employee assistance program            |
| EWB        | employee welfare benefit plan policy   |
| ENDRENAL   | end renal program                      |
| EHCPOL     | extended healthcare                    |
| FLEXP      | flexible benefit plan policy           |
| GOVEMP     | government employee health program     |
| HIP        | health insurance plan policy           |
| HMO        | health maintenance organization policy |
| HSAPOL     | health spending account                |
| HIRISK     | high risk pool program                 |
| HIVAIDS    | HIV-AIDS program                       |
| IND        | indigenous peoples health program      |
| LIFE       | life insurance policy                  |
| LTC        | long term care policy                  |
| MCPOL      | managed care policy                    |
| MANDPOL    | mandatory health program               |
| MENTPOL    | mental health policy                   |
| MENTPRG    | mental health program                  |
| MILITARY   | military health program                |
| pay        | Pay                                    |
| POS        | point of service policy                |
| PPO        | preferred provider organization policy |
| PNC        | property and casualty insurance policy |
| DISEASEPRG | public health program                  |
| PUBLICPOL  | public healthcare                      |
| REI        | reinsurance policy                     |
| RETIRE     | retiree health program                 |
| SAFNET     | safety net clinic program              |
| SOCIAL     | social service program                 |
| SUBSIDIZ   | subsidized health program              |
| SUBSIDMC   | subsidized managed care program        |
| SUBSUPP    | subsidized supplemental health program |
| SUBPOL     | substance use policy                   |
| SUBPRG     | substance use program                  |
| SURPL      | surplus line insurance policy          |
| TLIFE      | term life insurance policy             |
| UMBRL      | umbrella liability insurance policy    |
| UNINSMOT   | uninsured motorist policy              |
| ULIFE      | universal life insurance policy        |
| VET        | veteran health program                 |
| VISPOL     | vision care policy                     |
| CANPRG     | women's cancer detection program       |
| WCBPOL     | worker's compensation                  |

### TransactorType

| Value              | Label                  |
|--------------------|------------------------|
| commercial         | Commercial             |
| workerscomp        | Workers Comp           |
| champus            | Tricare/Champus        |
| medicaid           | Medicaid               |
| medicare           | Medicare               |
| medicare_advantage | Medicare Advantage     |
| CHIP               | CHIP                   |
| automobile         | Automobile             |
| employer           | Employer               |
| direct_care        | Direct Care            |
| bcbs               | Blue Cross Blue Shield |
