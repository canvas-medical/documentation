---
title: "Conditional Requests"
slug: "conditional-requests"
layout: apipage
---

## If-Unmodified-Since

Endpoints that perform update operations support the conditional header [If-Unmodified-Since](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Unmodified-Since).

If a request includes this header, then updates will be rejected if the stored resource has been modified since the date specified in the header, and a 412 Precondition Failed response will be returned.

The date should be in the format specified by [RFC 2616](https://www.rfc-editor.org/rfc/rfc2616).

```plaintext
If-Unmodified-Since: Wed, 21 Oct 2015 07:28:00 GMT
```