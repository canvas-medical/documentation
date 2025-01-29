---
layout: landingpage
title: Canvas Docs
permalink: "/"
---

<div class="hero">
    <div class="left">
        <div class="title">
            <h1>
                Unprecedented Access to Your EMR
            </h1>
            <h2>
                Explore our reference materials, guides, and examples to build and integrate with the Canvas platform.
            </h2>
        </div>
    </div>
    <div class="showcase">
        <div class="titlebar">
            <span class="spacer">&nbsp;</span>
            <span class="window-title">Terminal</span>
            <div class="window-controls">
                <span class="window-button">_</span>
                <span class="window-button">❐</span>
                <span class="window-button">×</span>
            </div>
        </div>
        <div class="terminal-content">
            <span class="user">dev@canvas</span>
            <span>:</span>
            <span class="pwd">/src</span>
            <span>$&nbsp;</span>
            <span class="command">pip install canvas</span>
        </div>
    </div>
</div>

<div class="landingpage_section">
    <h2 class="section-header">The Canvas SDK</h2>
    <div class="section-container">
        <div class="brag-box half-width">
            <h1 style="margin: auto; width: 65%;">
                Your code, hosted and executed directly in your Canvas
                webserver. Access without compromise.
            </h1>
        </div>
        <div class="card-list half-width">
            <a href="/sdk/">
                <div class="card-section-item">
                    <span class="cardHeading">Introduction</span>
                    <p>Your toolkit for customizing workflows natively across the
                    full Canvas platform: scheduling, charting, billing, and more</p>
                </div>
            </a>
            <a href="/guides/your-first-plugin/">
                <div class="card-section-item">
                    <span class="cardHeading">Your First Plugin</span>
                    <p>A step-by-step guide to orient you with the structure of a
                    plugin, and how to get one deployed and running</p>
                </div>
            </a>
            <a href="/sdk/handlers/">
                <div class="card-section-item">
                    <span class="cardHeading">Handlers</span>
                    <p>Components of your extension offering differentiated
                    interfaces that cater to their interaction model</p>
                </div>
            </a>
        </div>
    </div>
    <div class="card-grid">
        <a href="/sdk/events">
            <div class="card-section-item">
                <span class="cardHeading">Events</span>
                <p>Respond in real-time to <strong>650 events</strong><br/>(and counting!)</p>
            </div>
        </a>
        <a href="/sdk/data">
            <div class="card-section-item">
                <span class="cardHeading">Data</span>
                <p>Direct database access to clinical and administrative records</p>
            </div>
        </a>
        <a href="/sdk/effects">
            <div class="card-section-item">
                <span class="cardHeading">Effects</span>
                <p>Take action by modifying data, customizing the
                UI, or automating workflows</p>
            </div>
        </a>
    </div>
</div>

<div class="landingpage_section">
    <h2 class="section-header">Our FHIR API</h2>
    {% assign count_of_fhir_resources = 0 %}
    {% assign count_of_fhir_write_resources = 0 %}
    {% for item in site.menus.api_resources %}
        {% assign count_of_fhir_resources = count_of_fhir_resources | plus: 1 %}
        {% if item.children %}
            {% assign this_resource_supports_write = false %}
            {% for childitem in item.children %}
                {% if childitem.title contains "Create" or childitem.title contains "Update" %}
                    {% assign this_resource_supports_write = true %}
                {% endif %}
            {% endfor %}
            {% if this_resource_supports_write %}
                {% assign count_of_fhir_write_resources = count_of_fhir_write_resources | plus: 1 %}
            {% endif %}
        {% endif %}
    {% endfor %}
    <div class="section-container reverse-order-on-small-widths">
        <div class="card-list half-width">
            <a href="/api/">
                <div class="card-section-item">
                    <span class="cardHeading">Resource List</span>
                    <p>Example requests, responses, and attribute definitions</p>
                </div>
            </a>
            <a href="/api/quickstart">
                <div class="card-section-item">
                    <span class="cardHeading">Quickstart<br/></span>
                    <p>Steps you through authentication and general usage</p>
                </div>
            </a>
            <a href="https://www.postman.com/canvasmedical/workspace/canvas-medical-public-documentation" target="_blank">
                <div class="card-section-item">
                    <span class="cardHeading">Postman Collection</span>
                    <p>Explore our FHIR API with premade requests</p>
                </div>
            </a>
        </div>
        <div class="brag-box half-width">
            <div class="stat">
                <h1 class="stat-number">
                    {{ count_of_fhir_resources }}
                </h1>
                <h2 class="stat-description">
                     FHIR resources supported
                </h2>
            </div>
            <div class="stat">
                <h1 class="stat-number">
                    {{ count_of_fhir_write_resources }}
                </h1>
                <h2 class="stat-description">
                     With write support
                </h2>
            </div>
        </div>
    </div>
</div>

<div class="landingpage_section">
    <h2 class="section-header">Let Us Guide You</h2>
    {% include guides.html %}
</div>

<div class="landingpage_section">
    <div class="section-container">
        <a class="cta-button" href="https://www.canvasmedical.com/emrs/developer-sandbox">
            <h2 class="section-header">Get Instant Access to a Canvas Sandbox</h2>
        </a>
    </div>
</div>

<div class="landingpage_section">
    <h2 class="section-header">User Documentation</h2>
    <div class="card-grid">
        <a href="https://canvas-medical.help.usepylon.com/" target="_blank">
            <div class="card-section-item">
                <span class="cardHeading">Canvas Knowledge Center</span>
                <p>Powered by Pylon</p>
            </div>
        </a>
        <a href="/product-updates/release-notes">
            <div class="card-section-item">
                <span class="cardHeading">Release Notes</span>
                <p>See the latest features and fixes</p>
            </div>
        </a>
    </div>
</div>

<br/>
<br/>
<br/>
