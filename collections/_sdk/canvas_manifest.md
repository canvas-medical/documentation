---
title: "Canvas Manifest"
---

# Canvas Manifest Reference

The Canvas Manifest (`CANVAS_MANIFEST.json`) is the configuration file that defines your Canvas plugin's metadata, components, permissions, and UI integration points. This document provides a comprehensive reference for all manifest fields and configuration options.

## Table of Contents

- [Overview](#overview)
- [Required Fields](#required-fields)
- [Components](#components)
  - [Applications](#applications)
  - [Commands](#commands)
  - [Protocols](#protocols)
  - [Content](#content)
  - [Effects](#effects)
  - [Views](#views)
  - [Questionnaires](#questionnaires)
- [Application Scope and Menu Positioning](#application-scope-and-menu-positioning)
  - [Scope Types](#scope-types)
  - [Menu Position Options](#menu-position-options)
- [Additional Configuration](#additional-configuration)
- [Complete Examples](#complete-examples)

## Overview

The Canvas Manifest is a JSON file located at the root of your plugin directory. It tells Canvas how to load, display, and integrate your plugin with the Canvas platform.

### Basic Structure

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "0.0.1",
  "name": "my_plugin",
  "description": "A description of what this plugin does",
  "components": {
    "commands": [],
    "protocols": [],
    "content": [],
    "effects": [],
    "views": [],
    "applications": [],
    "questionnaires": []
  },
  "tags": {},
  "license": "MIT",
  "readme": "./README.md"
}
```

## Required Fields

All Canvas Manifests must include the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `sdk_version` | string | The version of the Canvas SDK this plugin is compatible with (e.g., "0.1.4") |
| `plugin_version` | string | The version of your plugin (e.g., "0.0.1") |
| `name` | string | Unique identifier for your plugin (snake_case recommended) |
| `description` | string | Human-readable description of your plugin's purpose |
| `components` | object | Contains all component definitions (must have at least one component type) |
| `tags` | object | Categorization tags for your plugin (can be empty `{}`) |
| `license` | string | License identifier (e.g., "MIT", "Apache-2.0") or empty string |
| `readme` | string or boolean | Path to README file (e.g., "./README.md") or `false` |

## Components

The `components` object defines the functional parts of your plugin. Each component type serves a different purpose in the Canvas ecosystem.

### Applications

Applications create interactive UI elements that appear in the Canvas interface. They're used for building custom pages, tools, and interfaces.

**Required Fields:**
- `class` (string): Python path to your application class
- `name` (string): Display name (max 32 characters)
- `description` (string): What the application does (max 256 characters)
- `icon` (string): Path to icon file (e.g., "assets/icon.png")
- `scope` (string): Where and how the application appears (see [Scope Types](#scope-types))

**Optional Fields:**
- `menu_position` (string): "top" or "bottom" - where in the menu to place this item
- `menu_order` (integer): Numeric ordering within the menu position
- `show_in_panel` (boolean): Whether to show in a panel view
- `panel_priority` (integer): Priority order for panel display

```json
{
  "class": "my_plugin.applications.my_app:MyApplication",
  "name": "My App",
  "description": "Does something useful",
  "scope": "patient_specific",
  "icon": "assets/icon.png",
  "menu_position": "top",
  "menu_order": 1
}
```

### Commands

Commands are executable actions that can be triggered by users or other plugins. They're useful for creating tools that perform specific tasks.

**Required Fields:**
- `class` (string): Python path to your command class
- `description` (string): What the command does

**Optional Fields:**
- `meta` (object): Additional metadata about the command
- `data_access` (object): Defines data access permissions

```json
{
  "class": "my_plugin.commands.my_command:MyCommand",
  "description": "Performs a specific action"
}
```

### Protocols

Protocols are event handlers that respond to Canvas events (like patient updates, note creation, etc.) or provide API endpoints for external integrations.

**Required Fields:**
- `class` (string): Python path to your protocol handler class
- `description` (string): What the protocol handles

**Optional Fields:**
- `meta` (object): Additional metadata
- `data_access` (object): Defines what data the protocol can read/write
  - `event` (string): The event type to listen for
  - `read` (array): List of data models the protocol can read
  - `write` (array): List of data models the protocol can modify

```json
{
  "class": "my_plugin.handlers.patient_sync:PatientSync",
  "description": "Syncs patient data with external system",
  "data_access": {
    "event": "patient.updated",
    "read": ["Patient", "Coverage"],
    "write": ["Patient"]
  }
}
```

### Content

Content components inject custom content into specific areas of the Canvas UI.

**Required Fields:**
- `class` (string): Python path to your content provider class
- `description` (string): What content this provides

```json
{
  "class": "my_plugin.content.banner:CustomBanner",
  "description": "Displays custom banner in patient chart"
}
```

### Effects

Effects are side-effect handlers that perform actions in response to events without returning data.

**Required Fields:**
- `class` (string): Python path to your effect handler class
- `description` (string): What effect this produces

```json
{
  "class": "my_plugin.effects.notification:SendNotification",
  "description": "Sends notification when conditions are met"
}
```

### Views

Views provide custom data views or API endpoints that return data without side effects.

**Required Fields:**
- `class` (string): Python path to your view class
- `description` (string): What data this view provides

```json
{
  "class": "my_plugin.views.patient_summary:PatientSummaryView",
  "description": "Returns summarized patient data"
}
```

### Questionnaires

Questionnaires define forms or surveys that can be presented to users.

**Required Fields:**
- `template` (string): Path to the questionnaire template file

```json
{
  "template": "templates/intake_form.json"
}
```

## Application Scope and Menu Positioning

Understanding scope and menu positioning is crucial for creating applications that appear in the right place with the right behavior.

### Scope Types

The `scope` field determines where your application appears and what context it has access to.

#### `patient_specific`

**Description:** Application appears in the patient chart and has access to the currently selected patient's context.

**Use Cases:**
- Custom chart views showing patient-specific data
- Clinical decision support tools that analyze patient information
- Patient-specific calculators or risk assessments
- Custom documentation interfaces tied to a specific patient

**UI Location:** Typically appears in the patient chart navigation

**Example Scenario:** You're building a risk calculator that needs access to a patient's vitals, medications, and lab results to calculate cardiovascular risk. This should use `patient_specific` scope.

```json
{
  "class": "my_plugin.apps.risk_calculator:RiskCalculator",
  "name": "CVD Risk Calculator",
  "description": "Calculate cardiovascular disease risk",
  "scope": "patient_specific",
  "icon": "assets/heart.png"
}
```

#### `global`

**Description:** Application is available organization-wide, not tied to any specific patient context.

**Use Cases:**
- Practice management tools
- Reporting and analytics dashboards
- Administrative utilities
- Organization-wide configuration interfaces
- Population health tools

**UI Location:** Accessible from the main Canvas menu/launcher

**Example Scenario:** You're building a practice dashboard that shows appointment statistics, provider utilization, and quality metrics across all patients. This should use `global` scope.

```json
{
  "class": "my_plugin.apps.practice_dashboard:PracticeDashboard",
  "name": "Practice Dashboard",
  "description": "View practice-wide metrics and analytics",
  "scope": "global",
  "icon": "assets/dashboard.png"
}
```

#### `provider_menu_item`

**Description:** Application appears in the provider's navigation menu, accessible to clinical staff.

**Use Cases:**
- Provider-specific tools and utilities
- Clinical workflow applications
- Provider preference settings
- Care team coordination tools

**UI Location:** Provider navigation menu

**Example Scenario:** You're building a task manager specifically for providers to track their follow-ups and care gaps across all their patients. This should use `provider_menu_item` scope.

```json
{
  "class": "my_plugin.apps.provider_tasks:ProviderTaskManager",
  "name": "My Tasks",
  "description": "Manage follow-ups and care gaps",
  "scope": "provider_menu_item",
  "icon": "assets/tasks.png"
}
```

#### `portal_menu_item`

**Description:** Application appears in the patient portal navigation, accessible to patients.

**Use Cases:**
- Patient-facing educational content
- Self-service tools for patients
- Symptom checkers or triage tools
- Patient engagement features

**UI Location:** Patient portal menu

**Example Scenario:** You're building a symptom tracker that allows patients to log and monitor their symptoms between visits. This should use `portal_menu_item` scope.

```json
{
  "class": "my_plugin.apps.symptom_tracker:SymptomTracker",
  "name": "Symptom Tracker",
  "description": "Track your symptoms over time",
  "scope": "portal_menu_item",
  "icon": "assets/tracker.png"
}
```

#### `provider_companion`

**Description:** Application appears as a persistent companion tool in the provider interface, typically in a sidebar or panel.

**Use Cases:**
- Quick reference tools (drug databases, medical calculators)
- Real-time assistants or copilots
- Communication tools
- Persistent context-aware utilities

**UI Location:** Persistent sidebar or companion panel

**Example Scenario:** You're building an AI assistant that provides real-time suggestions and references while the provider works in any part of Canvas. This should use `provider_companion` scope.

```json
{
  "class": "my_plugin.apps.ai_assistant:AIAssistant",
  "name": "Clinical Assistant",
  "description": "AI-powered clinical decision support",
  "scope": "provider_companion",
  "icon": "assets/assistant.png"
}
```

### Menu Position Options

Fine-tune where your application appears within its scope using menu positioning fields.

#### `menu_position`

Controls whether the item appears at the top or bottom of the menu.

**Options:**
- `"top"` - Item appears at the beginning of the menu
- `"bottom"` - Item appears at the end of the menu

**Default:** If not specified, Canvas determines positioning automatically.

```json
{
  "scope": "global",
  "menu_position": "top"
}
```

#### `menu_order`

Controls the relative order of items within the same menu position (top or bottom).

**Type:** Integer

**Behavior:** Lower numbers appear first. Items with the same `menu_order` are sorted alphabetically by name.

```json
{
  "scope": "global",
  "menu_position": "top",
  "menu_order": 1
}
```

**Example:** Three applications with `menu_position: "top"`:
- App A: `menu_order: 1` → Appears first
- App B: `menu_order: 2` → Appears second
- App C: `menu_order: 1` → Appears after App A (same order, alphabetically sorted)

#### `show_in_panel`

Controls whether the application should be displayed in a panel view.

**Type:** Boolean

**Use Case:** For applications that can be useful in both a full-page and panel context.

```json
{
  "scope": "patient_specific",
  "show_in_panel": true,
  "panel_priority": 5
}
```

#### `panel_priority`

Controls the ordering of panels when multiple panels are shown.

**Type:** Integer

**Behavior:** Lower numbers have higher priority and appear first.

```json
{
  "scope": "patient_specific",
  "show_in_panel": true,
  "panel_priority": 1
}
```

### Screenshot Placeholders

_TODO: Add screenshots showing where each scope type appears in the Canvas UI_

**Planned screenshots:**
1. `patient_specific` - Chart navigation with custom app
2. `global` - Main Canvas launcher with global app
3. `provider_menu_item` - Provider menu with custom item
4. `portal_menu_item` - Patient portal with custom item
5. `provider_companion` - Sidebar companion app
6. Menu positioning examples (top vs. bottom, ordering)

## Additional Configuration

### Secrets

Declare environment variables your plugin needs for API keys, credentials, etc.

```json
{
  "secrets": [
    "OPENAI_API_KEY",
    "EXTERNAL_API_URL",
    "API_SECRET"
  ]
}
```

Canvas will ensure these secrets are available to your plugin at runtime and prompt for configuration during installation.

### URL Permissions

Grant your plugin permission to load specific external URLs (for iframes or embedded content).

**Note:** Use either `url_permissions` OR `origins`, not both.

```json
{
  "url_permissions": [
    {
      "url": "https://example.com",
      "permissions": ["SCRIPTS", "ALLOW_SAME_ORIGIN", "MICROPHONE", "CAMERA"]
    }
  ]
}
```

**Available Permissions:**
- `SCRIPTS` - Allow JavaScript execution
- `ALLOW_SAME_ORIGIN` - Allow same-origin access
- `MICROPHONE` - Allow microphone access
- `CAMERA` - Allow camera access

### Origins (Legacy)

Alternative format for URL permissions (deprecated in favor of `url_permissions`).

```json
{
  "origins": {
    "urls": ["https://example.com"],
    "scripts": ["https://cdn.example.com/script.js"]
  }
}
```

### Tags

Categorize your plugin for discovery and organization.

```json
{
  "tags": {
    "patient_sourcing_and_intake": ["symptom_triage", "coverage_capture"],
    "interaction_modes_and_utilization": ["supply_policies", "demand_policies"],
    "content": ["patient_intake"]
  }
}
```

**Available Tag Categories:**
- `patient_sourcing_and_intake`
- `interaction_modes_and_utilization`
- `diagnostic_range_and_inputs`
- `pricing_and_payments`
- `care_team_composition`
- `interventions_and_safety`
- `content`

### References

List external references, documentation URLs, or related resources.

```json
{
  "references": [
    "https://docs.example.com/api",
    "https://github.com/example/plugin"
  ]
}
```

### Diagram

Path to an architecture or workflow diagram for your plugin.

```json
{
  "diagram": "docs/architecture.png"
}
```

Or disable:

```json
{
  "diagram": false
}
```

### Readme

Path to your plugin's README file.

```json
{
  "readme": "./README.md"
}
```

Or disable:

```json
{
  "readme": false
}
```

## Complete Examples

### Patient-Specific Chart Application

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "1.0.0",
  "name": "patient_risk_calculator",
  "description": "Calculate clinical risk scores for patients",
  "components": {
    "applications": [
      {
        "class": "patient_risk_calculator.apps.calculator:RiskCalculatorApp",
        "name": "Risk Calculator",
        "description": "Calculate cardiovascular and diabetes risk scores",
        "scope": "patient_specific",
        "icon": "assets/calculator.png",
        "menu_position": "top",
        "menu_order": 1
      }
    ],
    "protocols": [
      {
        "class": "patient_risk_calculator.handlers.api:CalculatorAPI",
        "description": "API endpoints for risk calculations"
      }
    ]
  },
  "secrets": [],
  "tags": {
    "interventions_and_safety": []
  },
  "license": "MIT",
  "readme": "./README.md"
}
```

### Global Practice Dashboard

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "1.0.0",
  "name": "practice_analytics",
  "description": "Organization-wide analytics and reporting dashboard",
  "components": {
    "applications": [
      {
        "class": "practice_analytics.apps.dashboard:AnalyticsDashboard",
        "name": "Analytics",
        "description": "View practice metrics and performance data",
        "scope": "global",
        "icon": "assets/chart.png",
        "menu_position": "top",
        "menu_order": 1
      }
    ]
  },
  "secrets": [],
  "tags": {
    "interaction_modes_and_utilization": []
  },
  "license": "MIT",
  "readme": "./README.md"
}
```

### Provider Companion Assistant

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "1.0.0",
  "name": "clinical_assistant",
  "description": "AI-powered clinical decision support companion",
  "components": {
    "applications": [
      {
        "class": "clinical_assistant.apps.assistant:ClinicalAssistant",
        "name": "AI Assistant",
        "description": "Real-time clinical guidance and suggestions",
        "scope": "provider_companion",
        "icon": "assets/ai.png",
        "show_in_panel": true,
        "panel_priority": 1
      }
    ],
    "protocols": [
      {
        "class": "clinical_assistant.handlers.api:AssistantAPI",
        "description": "API for assistant interactions"
      }
    ]
  },
  "secrets": [
    "OPENAI_API_KEY"
  ],
  "tags": {
    "interventions_and_safety": []
  },
  "license": "MIT",
  "readme": "./README.md"
}
```

### Multi-Component Plugin with Event Handlers

```json
{
  "sdk_version": "0.1.4",
  "plugin_version": "2.1.0",
  "name": "patient_engagement_suite",
  "description": "Comprehensive patient engagement and communication tools",
  "components": {
    "applications": [
      {
        "class": "patient_engagement_suite.apps.provider_view:ProviderDashboard",
        "name": "Engagement Dashboard",
        "description": "Monitor patient engagement metrics",
        "scope": "global",
        "icon": "assets/engagement.png",
        "menu_position": "top"
      },
      {
        "class": "patient_engagement_suite.apps.patient_portal:PatientTools",
        "name": "My Health Tools",
        "description": "Access health tracking and education",
        "scope": "portal_menu_item",
        "icon": "assets/tools.png",
        "menu_position": "top"
      }
    ],
    "protocols": [
      {
        "class": "patient_engagement_suite.handlers.messaging:MessageHandler",
        "description": "Handle patient messages and notifications",
        "data_access": {
          "event": "message.created",
          "read": ["Patient", "Message"],
          "write": ["Message"]
        }
      }
    ],
    "commands": [
      {
        "class": "patient_engagement_suite.commands.send_reminder:SendReminder",
        "description": "Send appointment reminders to patients"
      }
    ]
  },
  "secrets": [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN"
  ],
  "tags": {
    "patient_sourcing_and_intake": [],
    "interaction_modes_and_utilization": []
  },
  "license": "Apache-2.0",
  "readme": "./README.md",
  "diagram": "docs/architecture.png",
  "references": [
    "https://docs.twilio.com",
    "https://github.com/example/patient-engagement-suite"
  ]
}
```

---

## Additional Resources

- [Canvas SDK Documentation](/)
- [Plugin Development Guide](/commands-module/)
- [Example Plugins Repository](https://github.com/canvas-medical/canvas-plugins)

## Validation

Use the Canvas CLI to validate your manifest:

```bash
canvas-cli validate-manifest
```

This will check your `CANVAS_MANIFEST.json` for:
- Required fields
- Valid component configurations
- Proper scope values
- Correct field types
- Valid permission combinations
