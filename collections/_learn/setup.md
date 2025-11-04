---
title: "Setup"
slug: "setup"
layout: education
hidden: false
---

# Getting Started with Canvas Plugins: A Complete Setup Guide

## Prerequisites
- Python 3.11 or 3.12
- Developer access to a Canvas EHR instance

If you are not a current Canvas user, visit the [Developer Sandbox](https://www.canvasmedical.com/emrs/developer-sandbox) to obtain a login.

The following guide will reference these EHR instance variables as follows:
- `YOUR_CANVAS_EHR_INSTANCE` = the full URL, eg: https://my-clinic.canvasmedical.com
- `your-instance-name` = the subdomain name, eg: `my-clinic`

If you are using the developer sandbox environment, your instance name is `xpc-dev`.

## Part 1: Setting Up Authentication

### Step 1: Register Your Application
First, you need to register a third-party application to access the Canvas CLI tools:

1. Navigate to `{YOUR_CANVAS_EHR_INSTANCE}/auth/applications/`
2. Click the link to create a new application
3. Configure your application with these settings:
   - **Name**: This is the name associated with this set of credentials. Can be your name or a descriptive functional name.
   - **Client type**: Select **Confidential**
   - **Authorization grant type**: Select **client-credentials**
   - **Redirect URIs**: Leave blank (not needed for client credentials)
   - **Algorithm**: Set to **No OIDC support**

4. Save your application and **note your Client ID and Client Secret** - you'll need these in the next step

## Part 2: Setting Up the Canvas CLI

### Step 2: Install the Canvas CLI
Install the Canvas CLI using pip:

```bash
pip install canvas
```

### Step 3: Configure Your Credentials
Create a credentials file for the Canvas CLI:

1. Create a file at `~/.canvas/credentials.ini`
2. Add your credentials in the following format:

```ini
[your-instance-name]
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
is_default=true
```

**Note**: You can configure multiple Canvas instances by adding additional sections. Most Canvas users have a production and a development domain. Optionally: set `is_default=true` for your primary instance.

```ini
[my-clinic-dev]
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
is_default=true

[my-clinic]
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
```
---

## Part 3: Creating Your First Plugin

### Step 4: Initialize a New Plugin
Use the Canvas CLI to generate a plugin template:

```bash
$ canvas init
[1/1] project_name (My Cool Plugin): My First Plugin
```

The CLI will create a new project directory with all necessary files.

### Step 5: Understand the Plugin Structure
Your generated plugin will have this structure:

```sh
my-first-plugin/
├── my_first_plugin/
│   ├── CANVAS_MANIFEST.json
│   ├── README.md
│   └── protocols/
│       ├── __init__.py
│       └── my_protocol.py
├── pyproject.toml
└── tests/
    ├── __init__.py
    └── test_models.py
```

**Key files and folders:**
- **CANVAS_MANIFEST.json**: Declares your plugin's components and configuration
- **protocols/my_protocol.py**: Contains your plugin logic
- **README.md**: Documentation for your plugin
- **tests/**: Alongside `pyproject.toml`, lays the foundation for pytest in your plugin

### Step 6: Customize Your Protocol
Edit `protocols/my_protocol.py` to respond to Canvas events:

#### Choose the Event Type
1. Set the event type you want to respond to by modifying `RESPONDS_TO`.

**TRY IT**: `PATIENT_CREATED` is an easy event to trigger through the Canvas UI. Update the generically named class "Protocol" to something more descriptive, and change the event.

```python
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.events import EventType

class PatientWelcomeBanner(BaseProtocol):
    """Adds a Welcome message to new patient records"""

    RESPONDS_TO = EventType.Name(EventType.PATIENT_CREATED)
```

#### Make Stuff Happen
2. Implement the `compute()` method to define what happens when the event fires

**TRY IT**: Let's build on what we started and get the patient key for the newly created patient. We can log the event to confirm its context and target, and use the patient ID to set up an Alert Banner.

```python
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.effects import Effect
from canvas_sdk.events import EventType
from logger import log

class PatientWelcomeBanner(BaseProtocol):
    """Adds a Welcome message to new patient records"""

    RESPONDS_TO = EventType.Name(EventType.PATIENT_CREATED)

    def compute(self) -> list[Effect]:
        """Listens for patient creation and returns an alert banner"""
        log.info(self.context) # empty
        log.info(self.target) # 7887caeed0484c368b21f0108fd03cf9
```

3. Return Effects to modify workflows or data in Canvas

**TRY IT**: Add a banner alert to the patient profile. You can remove your logger if no longer needed.

```python
from canvas_sdk.protocols import BaseProtocol
from canvas_sdk.events import EventType
from canvas_sdk.effects import Effect
from canvas_sdk.effects.banner_alert import AddBannerAlert
from canvas_sdk.v1.data.patient import Patient

class PatientWelcomeBanner(BaseProtocol):
    """Adds a Welcome message to new patient records"""

    RESPONDS_TO = EventType.Name(EventType.PATIENT_CREATED)

    def compute(self) -> list[Effect]:
        """Listens for patient creation and returns an alert banner"""
        # Load the patient object
        patient = Patient.objects.get(id=self.target)
        patient_name = patient.first_name

        banner = AddBannerAlert(
            patient_id=self.target,
            key="welcome",
            narrative=f"{patient_name} is a new patient.",
            placement=[
                AddBannerAlert.Placement.CHART
            ],
            intent= AddBannerAlert.Intent.INFO,
            href="https://docs.canvasmedical.com"
        )

        return [banner.apply()]
```

### Step 7: Deploy Your Plugin
If you changed the class name in Step 6, you'll need to update the class name in CANVAS_MANIFEST.json:

```json
    "components": {
        "protocols": [
            {
                "class": "my_first_plugin.protocols.my_protocol:PatientWelcomeBanner",
                "description": "A protocol that adds a welcome banner for new patients."
            }
        ],
```

From your plugin's root directory, install it to your Canvas instance:

```bash
canvas install <path/to/plugin_package>
```

For example:
```bash
canvas install my_first_plugin
```

This command packages, uploads, installs, and enables your plugin. Run the same command whenever you make updates. The `install` command takes an optional environment host:
```bash
canvas install my_first_plugin --host your-instance-name
```

### Step 8: Monitor Your Plugin
Tail the logs to view output and catch errors:

```bash
canvas logs --host your-instance-name
```

This will stream logs for all plugins installed on that instance.

You can confirm your plugin is working by creating a new patient in your test EHR instance, and you should see a welcome banner!

![Patient Chart](/assets/images/new-patient-banner.png)

---

## Next Steps

Now that you have authentication configured and your first plugin deployed, you can:

* Respond to different Event Types
* Traverse Data objects
* Return various Effect types

Next up: --> [Events](/learn/events)