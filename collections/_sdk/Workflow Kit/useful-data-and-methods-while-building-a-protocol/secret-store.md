---
title: "Settings/Secret Store"
slug: "secret-store"
hidden: false
createdAt: "2022-02-17T03:53:13.817Z"
updatedAt: "2022-04-14T22:04:41.481Z"
---
Canvas provides you with a key-value secret store that can be accessed from within your protocols. This can be helpful if you are using notification protocols and want to store any keys or tokens for posting data to your own servers (and don't want those secrets in plaintext in your protocol code). You can also store any other kind of settings or data that would be useful in your protocols. 

To view and edit your instance's protocol secret store, navigate to `Settings` > `Protocol settings` (`/admin/api/protocolsetting/`). This page will list all of the key-value entries in your protocol secret store. To create a new entry, click the grey button in the top right corner that says `Add protocol setting`. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/220a61b-Screen_Shot_2022-02-16_at_7.58.40_PM.png",
        "Screen Shot 2022-02-16 at 7.58.40 PM.png",
        1908,
        478,
        "#e7edf2"
      ]
    }
  ]
}
[/block]
Type in the key and value you wish to store and click Save. 
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/bbb83db-Screen_Shot_2022-02-16_at_8.00.46_PM.png",
        "Screen Shot 2022-02-16 at 8.00.46 PM.png",
        1894,
        850,
        "#eff3f6"
      ]
    }
  ]
}
[/block]
Your new setting key should now be in the list on the main page. To access these values from within your protocol, you can simply do `self.settings` and you will have the entire dictionary of key-value pairs. For example, if I wanted to access the value for the `foo` key that I saved above, I would do `self.settings['foo']` or even `self.settings.foo`