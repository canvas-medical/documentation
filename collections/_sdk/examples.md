---
title: "Example Plugins"
disable_anchorlist: true
---

The pages below showcase example plugins written with the Canvas SDK. All
pages describe the file structure, the functionality, and link to GitHub where
you can grab the code yourself and start iterating.

<div class="sdk-card-list">
{% for item in site.menus.example_plugins %}
    <a href="{{ item.url }}">
        <div class="sdk-card">
            <span class="cardHeading">{{ item.title }}</span>
        </div>
    </a>
{% endfor %}
</div>

<br/>
<br/>
<br/>
