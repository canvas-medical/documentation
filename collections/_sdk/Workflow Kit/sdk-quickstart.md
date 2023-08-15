---
title: "Quickstart"
slug: "sdk-quickstart"
excerpt: "Canvas Workflow Kit SDK Installation Quickstart"
hidden: false
createdAt: "2022-02-08T17:38:02.138Z"
updatedAt: "2022-02-16T22:42:57.253Z"
---
## Introduction

The Canvas Workflow Kit is a Software Development Kit (SDK) that makes it possible to extend the functionality of a Canvas instance. By providing a built-in command-line interface, skeleton code and test commands, developers can use the the SDK to customize Protocols.

## Installation

The SDK can either be [downloaded directly from PyPI](https://pypi.org/project/canvas-workflow-kit/) or can be installed using the Python Package Manager `pip`. Python 3.8 or above is required.

If you are new to Python, it is recommended to install packages used for development into a Python Virtual Environment rather than your system-wide installation. Instructions for setting up and activating a Virtual Environment can be [found here](https://docs.python.org/3/tutorial/venv.html).

Once your virtual environment is set up and activated, open a terminal and type the following command to install the SDK:

```
(env) $ pip install canvas-workflow-kit
```

Once the installation is complete, the `canvas-cli` command will automatically be available in the terminal. You can test this by using the `which` command:

```
(env) $ which canvas-cli
```

You should see the output location like so (the directory structure will differ based on your Python installation):

```
(env) $ which canvas-cli
/Users/{username}/Environments/env/bin/canvas-cli
```

## Initial Setup

Now it's time to set up your local environment to be able to interact with your Canvas development instance. Run the following command in the terminal:

```sh
(env) $ canvas-cli create-default-settings
```

This will create a `.canvas` folder in your home directory that contains a file named `config.ini`.

Open and edit the `~/.canvas/config.ini` file in your editor of choice, and add the *url* of your canvas instance, as well as your Canvas API key.

If you are working on a Canvas preview instance, your Canvas API key is the Bearer Token on your dashboard page. If you are on a Canvas-created dev, staging or production instance, you will need to request your API token from your Canvas Implementation Manager.

After adding your *url* and *api-key* data, your `config.ini` file should look something like this:

```
[canvas_cli]
url=https://yourcanvasinstance.canvasmedical.com/
api-key=abcdef123ccaef41d4381afdd86562de8accc999
```

Finally, create a directory in the location of your choice to store your project. For the purposes of this guide, we have created a directory called `canvas_protocols` to store our code:

```sh
(env) $ mkdir canvas_protocols
(env) $ cd canvas_protocols
(env) $ pwd
/Users/{username}/Projects/canvas_protocols
```

## Next Steps

Now that your local environment is set up, the next step is to [fetch patient data to work with](doc:sdk-fetching-and-viewing-patient-data).