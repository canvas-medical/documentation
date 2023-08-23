---
title: "Notification Protocol"
slug: "notification-protocol"
excerpt: "A protocol that computes only in response to database events, similar to a webhook"
hidden: false
createdAt: "2022-01-24T23:23:09.890Z"
updatedAt: "2023-02-08T18:27:49.668Z"
---
If you're looking to implement some webhook-style functionality in your Canvas instance that responds to database events, look no further than Notification Protocols! These protocols are similar to regular ones, with two major differences:
* there need not be a UI card presented in the UI (there optionally can be)
* they only compute in response to database events defined in `compute_on_change_types` - they never compute on upload

Some examples of Notification Protocols, and common use-cases for them, can be found [here](https://docs.canvasmedical.com/docs/appointment-notification), [here](https://docs.canvasmedical.com/docs/appointment-task-creator), and [here](https://docs.canvasmedical.com/docs/appointment-updater) 

To make your protocol behave as a Notification Protocol, all you need to do to is add `notification_only = True` to the Meta attributes of the protocol class. You'll also want to make sure you have at least one change_type defined in `compute_on_change_types` - otherwise the protocol will never compute at all! 

As a convenience, we offer a utility function called `send_notification` that many of our users find helpful to use in their Notification Protocols. You just need to pass in the url you want to send data to, a payload, and some headers and it will send a POST request for you. 

Check out the examples linked above, or the code below which just highlights the necessary pieces you'll need to get the notification party started.
[block:code]
{
  "codes": [
    {
      "code": "from canvas_workflow_kit.utils import send_notification\n\nclass MyNotificationProtocol(ClinicalQualityMeasure):\n\n    class Meta:\n        ...\n        compute_on_change_types = [CHANGE_TYPE.APPOINTMENT]\n        notification_only = True\n\n    def compute_results(self):\n        result = ProtocolResult()\n        result.status = STATUS_NOT_APPLICABLE\n        ...\n        send_notification('https://my-url.com', my_payload, my_headers)\n\n        return result",
      "language": "python"
    }
  ]
}
[/block]