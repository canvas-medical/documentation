---
title: Questionnaire Conditional Logic (Question Enablement)
layout: documentation
---

# Questionnaire Conditional Logic Changes

## Overview

This document describes the conditional logic functionality added to the Canvas questionnaire system. These changes enable questions to be conditionally displayed based on responses to previous questions in a questionnaire, following the FHIR Questionnaire.item.enableWhen pattern.

## File Modified

**Path**: `/canvas/home-app/api/models/questionnaire.py`

## Changes Summary

The implementation adds three main components:

1. **Enable Behavior Constants** (Lines 114-120)
2. **Enable Behavior Field** (Lines 140-148)  
3. **Question Enablement Condition Model** (Lines 445-447 onwards)

---

## 1. Enable Behavior Constants

**Location**: Lines 114-120 in the `Question` model

### Code

```python
ENABLE_BEHAVIOR_ALL = "all"
ENABLE_BEHAVIOR_ANY = "any"
ENABLE_BEHAVIOR_CHOICES = (
    (ENABLE_BEHAVIOR_ALL, "All conditions (AND)"),
    (ENABLE_BEHAVIOR_ANY, "Any condition (OR)"),
)
```

### Purpose

These constants define how multiple enablement conditions should be evaluated:

- **`ENABLE_BEHAVIOR_ALL`**: All conditions must be true (AND logic) for the question to be displayed
- **`ENABLE_BEHAVIOR_ANY`**: At least one condition must be true (OR logic) for the question to be displayed

---

## 2. Enable Behavior Field

**Location**: Lines 140-148 in the `Question` model

### Code

```python
enable_behavior = models.CharField(
    max_length=4,
    choices=ENABLE_BEHAVIOR_CHOICES,
    default=ENABLE_BEHAVIOR_ALL,
    blank=True,
    null=True,
    help_text="Determines whether all or any question enablement conditions must be true",
)
```

### Purpose

This field is added to the `Question` model to specify how multiple enablement conditions should be evaluated when determining if a question should be shown.

### Field Attributes

- **Type**: CharField (max 4 characters)
- **Choices**: `ENABLE_BEHAVIOR_ALL` or `ENABLE_BEHAVIOR_ANY`
- **Default**: `ENABLE_BEHAVIOR_ALL` (AND logic)
- **Nullable**: Yes (can be blank or null)
- **Description**: Controls the logical operator used when evaluating multiple enablement conditions

### Usage Example

If a question has multiple `QuestionEnablementCondition` objects:
- With `enable_behavior="all"`: ALL conditions must be satisfied
- With `enable_behavior="any"`: ANY ONE condition being satisfied is enough

---

## 3. Question Enablement Condition Model

**Location**: Lines 445-447 onwards

### Model Definition

```python
class QuestionEnablementCondition(TimestampedStatusModel):
    """
    Model for storing conditional logic to determine when a question should be displayed
    based on responses to other questions in the questionnaire.
    This follows the FHIR Questionnaire.item.enableWhen pattern.
    """

    OPERATOR_EQUALS = "="
    OPERATOR_NOT_EQUALS = "!="
    OPERATOR_EXISTS = "exists"
    OPERATOR_NOT_EXISTS = "not_exists"

    OPERATOR_CHOICES = (
        (OPERATOR_EQUALS, "Equals"),
        (OPERATOR_NOT_EQUALS, "Not Equals"),
        (OPERATOR_EXISTS, "Exists"),
        (OPERATOR_NOT_EXISTS, "Does Not Exist"),
    )

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="dependent_conditions"
    )
    dependent_on = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="triggers_condition"
    )
    operator = models.CharField(max_length=10, choices=OPERATOR_CHOICES)
    answer_option = models.ForeignKey(
        ResponseOption, null=True, blank=True, on_delete=models.CASCADE
    )
    answer_value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
```

### Purpose

This model stores conditional logic rules that determine when a question should be displayed based on responses to other questions in the same questionnaire. It implements the FHIR standard's `enableWhen` pattern.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `question` | ForeignKey | The question that depends on this condition (will be shown/hidden) |
| `dependent_on` | ForeignKey | The question whose answer this condition checks |
| `operator` | CharField | The comparison operator to use (`=`, `!=`, `exists`, `not_exists`) |
| `answer_option` | ForeignKey | The specific response option to check (for single/multi-select questions) |
| `answer_value` | CharField | The value to compare against (for text/integer questions) |

### Operators

- **`=` (Equals)**: Shows the question if the answer matches the specified value/option
- **`!=` (Not Equals)**: Shows the question if the answer does NOT match the specified value/option
- **`exists`**: Shows the question if any answer exists for the dependent question
- **`not_exists`**: Shows the question if no answer exists for the dependent question

### Validation

The model includes a `clean()` method that validates:
- When an `answer_option` is selected, it must belong to the `response_option_set` of the `dependent_on` question
- Prevents misconfiguration where an answer option from a different question is selected

---

## Use Cases

### Example 1: Simple Conditional Question

**Scenario**: Show "How many cigarettes per day?" only if user answers "Yes" to "Do you smoke?"

```python
# Question 1: "Do you smoke?"
smoke_question = Question.objects.get(name="Do you smoke?")

# Question 2: "How many cigarettes per day?" (conditionally shown)
cigarettes_question = Question.objects.get(name="How many cigarettes per day?")

# Get the "Yes" response option
yes_option = ResponseOption.objects.get(
    response_option_set=smoke_question.response_option_set,
    name="Yes"
)

# Create the enablement condition
QuestionEnablementCondition.objects.create(
    question=cigarettes_question,
    dependent_on=smoke_question,
    operator=QuestionEnablementCondition.OPERATOR_EQUALS,
    answer_option=yes_option
)
```

### Example 2: Multiple Conditions with AND Logic

**Scenario**: Show "Describe your symptoms" only if user has both fever AND cough

```python
symptoms_question = Question.objects.get(name="Describe your symptoms")
symptoms_question.enable_behavior = Question.ENABLE_BEHAVIOR_ALL  # AND logic

# Condition 1: Has fever
QuestionEnablementCondition.objects.create(
    question=symptoms_question,
    dependent_on=fever_question,
    operator=QuestionEnablementCondition.OPERATOR_EQUALS,
    answer_option=yes_option
)

# Condition 2: Has cough  
QuestionEnablementCondition.objects.create(
    question=symptoms_question,
    dependent_on=cough_question,
    operator=QuestionEnablementCondition.OPERATOR_EQUALS,
    answer_option=yes_option
)
```

### Example 3: Multiple Conditions with OR Logic

**Scenario**: Show "Emergency contact" if any symptom is severe

```python
emergency_question = Question.objects.get(name="Emergency contact")
emergency_question.enable_behavior = Question.ENABLE_BEHAVIOR_ANY  # OR logic

# Show if severe pain OR severe fever OR severe bleeding
for symptom in [pain_question, fever_question, bleeding_question]:
    severe_option = ResponseOption.objects.get(
        response_option_set=symptom.response_option_set,
        name="Severe"
    )
    QuestionEnablementCondition.objects.create(
        question=emergency_question,
        dependent_on=symptom,
        operator=QuestionEnablementCondition.OPERATOR_EQUALS,
        answer_option=severe_option
    )
```

---

## FHIR Compliance

These changes implement the FHIR R4 [Questionnaire.item.enableWhen](http://hl7.org/fhir/R4/questionnaire-definitions.html#Questionnaire.item.enableWhen) pattern, which specifies:

- **enableWhen**: Conditions that determine whether the item is enabled
- **enableBehavior**: Specifies the behavior when multiple enableWhen conditions are present (all vs any)
- **Operators**: Supports standard FHIR operators for value comparison

This ensures Canvas questionnaires can be mapped to and from FHIR-compliant formats.

---

## Database Schema Impact

### New Model
- **Table**: `question_enablement_condition`
- **Relationships**: 
  - Links to `Question` (question being controlled)
  - Links to `Question` (question being monitored)
  - Links to `ResponseOption` (specific answer being checked)

### Modified Model
- **Table**: `question`
- **New Field**: `enable_behavior` (VARCHAR(4), nullable)

---

## Related Models

- **Question**: Contains the `enable_behavior` field and `dependent_conditions` relationship
- **ResponseOption**: Referenced by enablement conditions for single/multi-select questions
- **ResponseOptionSet**: Determines the type of question and available response options
- **Interview/InterviewQuestionResponse**: Runtime data that conditions are evaluated against

---

## Implementation Notes

1. **Backwards Compatibility**: The `enable_behavior` field is nullable and defaults to `ENABLE_BEHAVIOR_ALL`, maintaining existing behavior
2. **Validation**: Model-level validation ensures answer options match their parent questions
3. **Cascading Deletes**: Enablement conditions are deleted when their related questions are deleted
4. **Status Tracking**: Inherits from `TimestampedStatusModel` for audit trail

---
