---
title: Example API Docs via Front Matter
sections:
  - type: section
    blocks:
      - type: apidoc
        name: AllergyIntolerance
        description: >-
          At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.
        attributes:
          - name: id
            description: >-
              First Main - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            type: string
            attributes:
              - name: id
                description: >-
                  Second Inner Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna
                  aliqua. 
                type: string              
              - name: id
                description: >-
                  Third InnerLorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna
                  aliqua. 
                type: string
          - name: id
            description: >-
              Outter side Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            type: string
        example_payload: example-payload-code
        endpoints:
          - summary: AllergyIntolerance create
            method: post
            url: '/AllergyIntolerance/{id}'
            description: >-
              The AllergyIntolerance search-type interaction searches a set of
              resources based on some filter criteria.
            parameters:
              - name: id
                description: Logical id of this artifact
                required: true
                type: string
              - name: _format
                description: >-
                  Override the HTTP content negotiation to specify JSON or XML
                  response format
                required: false
                type: string
              - name: _pretty
                description: Ask for a pretty printed response for human convenience
                required: false
                type: string
            responses:
              - response: 201
                description: Successful Claim create
              - response: 400
                description: >-
                  Claim create request could not be parsed or failed basic FHIR
                  validation rules.
            example_request: example-request-one
            example_response: example-response-one
          - summary: AllergyIntolerance read
            method: get
            url: '/AllergyIntolerance/{id}'
            description: >-
              The AllergyIntolerance search-type interaction searches a set of
              resources based on some filter criteria.
            parameters:
              - name: id
                description: Logical id of this artifact
                required: true
                type: string
              - name: _format
                description: >-
                  Override the HTTP content negotiation to specify JSON or XML
                  response format
                required: false
                type: string
              - name: _pretty
                description: Ask for a pretty printed response for human convenience
                required: false
                type: string
            responses:
              - response: 201
                description: Successful Claim create
              - response: 400
                description: >-
                  Claim create request could not be parsed or failed basic FHIR
                  validation rules.
            example_request: example-request-two
            example_response: example-response-two
---
<div id="example-payload-code">

{% tabs log %}

{% tab log php %}
```php
var_dump('hello');
```
{% endtab %}

{% tab log js %}
```javascript
console.log('hello');
```
{% endtab %}

{% tab log ruby %}
```javascript
puts 'hello'
```
{% endtab %}

{% endtabs %}

</div>

<div id="example-request-one">

{% tabs log %}

{% tab log php %}
```php
var_dump('hello');
```
{% endtab %}

{% tab log js %}
```javascript
console.log('hello');
```
{% endtab %}

{% tab log ruby %}
```javascript
puts 'hello'
```
{% endtab %}

{% endtabs %}

</div>

<div id="example-response-one">

{% tabs log %}

{% tab log php %}
```php
var_dump('hello');
```
{% endtab %}

{% tab log js %}
```javascript
console.log('hello');
```
{% endtab %}

{% tab log ruby %}
```javascript
puts 'hello'
```
{% endtab %}

{% endtabs %}

</div>

<div id="example-request-two">

{% tabs log %}

{% tab log php %}
```php
var_dump('hello');
```
{% endtab %}

{% tab log js %}
```javascript
console.log('hello');
```
{% endtab %}

{% tab log ruby %}
```javascript
puts 'hello'
```
{% endtab %}

{% endtabs %}

</div>

<div id="example-response-two">

{% tabs log %}

{% tab log php %}
```php
var_dump('hello');
```
{% endtab %}

{% tab log js %}
```javascript
console.log('hello');
```
{% endtab %}

{% tab log ruby %}
```javascript
puts 'hello'
```
{% endtab %}

{% endtabs %}

</div>

