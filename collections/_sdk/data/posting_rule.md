---
title: "PostingRule"
slug: "data-posting-rule"
excerpt: "Canvas SDK PostingRule"
hidden: false
---

## Introduction

The `PostingRule` model represents an ERA (electronic remittance advice) posting rule. Each rule maps a claim adjustment group and code to what Canvas does with a matching adjustment when it posts a remittance: write it off, post it without writing it off, or transfer it to the next payer. A rule with no `transactor` applies to every insurer, and a rule with a blank `adjustment_code` matches every code in its group.

To create, update, or delete posting rules, use the [PostingRule effect](/sdk/effect-instance-configuration/#posting-rules).

## Basic usage

**List the rules that write off contractual obligation adjustments**

```python
from canvas_sdk.v1.data import PostingRule
from canvas_sdk.v1.data.posting_rule import PostingRuleBehavior

write_offs = PostingRule.objects.filter(
    adjustment_group="CO", behavior=PostingRuleBehavior.WRITE_OFF
)
for rule in write_offs:
    print(rule.adjustment_code or "(all codes)", rule.description)
```

**List the rules for one insurer**

```python
from canvas_sdk.v1.data import PostingRule
from canvas_sdk.v1.data.coverage import Transactor

insurer = Transactor.objects.get(payer_id="AVA03")
insurer_rules = PostingRule.objects.filter(transactor=insurer)
```

## Attributes

### PostingRule

| Field Name              | Type                                                    |
| ----------------------- | ------------------------------------------------------- |
| dbid                    | Integer                                                 |
| created                 | DateTime                                                |
| modified                | DateTime                                                |
| description             | String                                                  |
| adjustment_group        | String                                                  |
| adjustment_code         | String                                                  |
| behavior                | [PostingRuleBehavior](#postingrulebehavior)             |
| payer_order             | [PostingRulePayerOrder](#postingrulepayerorder)         |
| transactor              | [Transactor](/sdk/data-coverage/#transactor)            |
| automated_action_review | Boolean                                                 |
| is_preset               | Boolean                                                 |

## Enumeration types

### PostingRuleBehavior

| Value         | Label                             |
| ------------- | --------------------------------- |
| write_off     | Write off adjustment              |
| non_write_off | Non write off adjustment          |
| transfer      | Transfer adjustment to next payer |

### PostingRulePayerOrder

| Value         | Label         |
| ------------- | ------------- |
| primary       | Primary       |
| supplementary | Supplementary |
