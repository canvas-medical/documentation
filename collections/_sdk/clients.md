---
title: "Clients"
disable_anchorlist: true
---

The clients module provides pre-built integrations with popular third-party services, letting your plugins send emails, SMS messages, interact with AI models, process documents, and manage cloud storage. Each client handles authentication, request formatting, and response parsing so you can focus on your plugin's logic.

All clients follow a consistent pattern: configure credentials via [plugin secrets](/sdk/secrets/), instantiate a client, and call methods. Error handling is standardized with a `RequestFailed` exception across most clients.

<div class="sdk-card-list">
{% for item in site.menus.clients_module %}
    <a href="{{ item.url }}">
        <div class="sdk-card">
            <span class="cardHeading">{{ item.title }}</span>
            <p>{{ item.description }}</p>
        </div>
    </a>
{% endfor %}
</div>

<br/>
<br/>
<br/>
