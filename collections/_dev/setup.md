---
title: "Setup"
slug: "setup"
layout: devpage
hidden: false
---

# Getting Started with Canvas Plugins: A Complete Setup Guide

## Prerequisites
- Python 3.11 or 3.12
- Access to a Canvas EHR instance

If you are not a current Canvas user, visit [Developer Sandbox with XPC Support(https://www.canvasmedical.com/emrs/developer-sandbox)] to request access.

The following guide will reference these EHR instance variables as follows:
* `YOUR_CANVAS_EHR_INSTANCE` = the full URL, eg: https://my-clinic.canvasmedical.com
* `your-instance-name` = the subdomain name, eg: `my-clinic`

If you are using the developer sandbox environment, your instance name is `xpc-dev`.
---

## Part 1: Setting Up Authentication

### Step 1: Register Your Application
First, you need to register a third-party application to access Canvas:

1. Navigate to `{YOUR_CANVAS_EHR_INSTANCE}/auth/applications/`
2. Click the link to create a new application
3. Configure your application with these settings:
   - **Name**: Choose a descriptive name for your application
   - **Client type**: Select **Confidential**
   - **Authorization grant type**: Select **client-credentials**
   - **Redirect URIs**: Leave blank (not needed for client credentials)
   - **Algorithm**: Set to **No OIDC support**

4. Save your application and **note your Client ID and Client Secret** - you'll need these in the next step

### Step 2: Obtain Your Access Token
To authenticate using Client Credentials:

```bash
curl --request POST '{YOUR_CANVAS_EHR_INSTANCE}/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id={YOUR_CLIENT_ID}' \
--data-urlencode 'client_secret={YOUR_CLIENT_SECRET}'
```

You'll receive a JSON response containing an `access_token` that's valid for 10 hours.

---

## Part 2: Setting Up the Canvas CLI

### Step 3: Install the Canvas CLI
Install the Canvas CLI using pip:

```bash
pip install canvas
```

### Step 4: Configure Your Credentials
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

### Step 5: Initialize a New Plugin
Use the Canvas CLI to generate a plugin template:

```bash
$ canvas init
[1/1] project_name (My Cool Plugin): My First Plugin
```

The CLI will create a new project directory with all necessary files.

### Step 6: Understand the Plugin Structure
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
    └── test_my_protocol.py
```

**Key files:**
- **CANVAS_MANIFEST.json**: Declares your plugin's components and configuration
- **protocols/my_protocol.py**: Contains your plugin logic
- **README.md**: Documentation for your plugin

### Step 7: Configure Your Protocol
Edit `protocols/my_protocol.py` to respond to Canvas events:

1. **Set the event type** you want to respond to by modifying `RESPONDS_TO`
2. **Implement the `compute()` method** to define what happens when the event fires
3. **Return Effects** to modify workflows or data in Canvas

### Step 8: Deploy Your Plugin
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

### Step 9: Monitor Your Plugin
Tail the logs to view output and catch errors:

```bash
canvas logs --host your-instance-name
```

This will stream logs for all plugins installed on that instance .

---

## Next Steps

Now that you have authentication configured and your first plugin deployed, you can:

* Respond to different Event Types
* Traverse Data objects
* Return various Effect types

Next up: --> [Events](/dev/events)