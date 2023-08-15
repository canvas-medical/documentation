---
title: "Canvas CLI Additional Commands"
slug: "canvas-cli"
hidden: false
createdAt: "2021-09-14T20:01:57.004Z"
updatedAt: "2022-02-18T20:26:01.371Z"
---
The canvas-cli tool provides convenience methods that simplify working with canvas instances and the SDK. 

### list-versions

List the available versions on the server.

**Usage:**

    $ canvas-cli list-versions MODULE_NAME
  
### set-active / set-inactive
	
**Usage:**
	
	$ canvas-cli set-active MODULE_NAME
	$ canvas-cli set-inactive MODULE_NAME

### set-version

  Set a protocol's active version on the server.  The protocol upload may
  still need to be made active after changing the version.  Version numbers can be obtained with the `list-versions` command.

	
**Usage:**
	
	$ canvas-cli set-version MODULE_NAME VERSION

Versions cannot be overwritten, and must be updated to a new version number before it can be uploaded again