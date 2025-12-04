---
title: "Sandboxing and Allowed Imports"
slug: "sandboxing-and-allowed-imports"
hidden: false
createdAt: "2022-08-10T04:28:55.830Z"
updatedAt: "2022-11-08T19:48:39.467Z"
---
The custom protocols that you upload to your Canvas EHR using the Workflow Kit execute safely and securely in a sandbox that restricts access to the host operating system, filesystem, and database. We take this precaution in order to reduce likelihood of accidents or malicious use of the platform that might put patient data at risk.

The following are the Python libraries that you are allowed to import to your protocols:
- arrow
- cached_property
- canvas_workflow_kit
- contextlib
- datetime
- dateutil
- enum
- functools
- hashlib
- hmac
- http
- json
- math
- operator
- pickletools
- random
- re
- requests
- string
- time (Coming on 11/16/2022)
- traceback
- typing
- urllib
- uuid
- workflow_sdk_loader.builtin_cqms

The following are the Python builtin functions that are currently available within the sandbox:
- None
- False
- True
- abs
- all
- any
- bool
- bytes
- callable
- chr
- classmethod
- complex
- dict
- divmod
- filter
- float
- frozenset
- hash
- hex
- id
- int
- hasattr
- isinstance
- issubclass
- iter
- len
- list
- max
- min
- next
- oct
- ord
- pow
- property
- random
- range
- repr
- round
- set
- slice
- sorted
- staticmethod
- str
- super
- tuple
- zip

If there is a library or function not on this list that you wish to import to your protocol, reach out to your Canvas support team with the request and it can be added after a security review.