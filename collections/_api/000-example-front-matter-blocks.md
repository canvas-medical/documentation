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
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            type: string
            attributes:
              - name: id
                description: >-
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna
                  aliqua. 
                type: string
              - name: id
                description: >-
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna
                  aliqua. 
                type: string
          - name: id
            description: >-
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            type: string
        example_payload:
          format: json
          example: |
            {
              "access_token": "eyJhbGciOiJFUzI1NiJ9.eyJqdGkiOiI5NmQ5Njgw...",
              "expires_in": 3600,
              "refresh_expires_in": 86400,
              "endpoint": {
                "id": "d39433b7-0fbd-4bc2-bdae-fb276799979f",
                "label": ["Humana"],
                "name": "humana-sandbox",
                "refreshable": true,
                "resources": [
                  "Coverage",
                  "ExplanationOfBenefit",
                  "Patient"
                ]
              }
            }
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
            example_request:
              format: javascript
              example: >
                const request = await
                fetch("https://api.flexpa.com/link/exchange", {
                  method: "POST",
                  headers: {
                    "content-type": "application/json",
                  },
                  body: JSON.stringify({
                    public_token: "public_token...",
                    secret_key: "sk_test...",
                  }),
                });

                const { access_token: accessToken, expires_in: expiresIn } =
                await request.json();
            example_response:
              format: json
              example: |
                {
                  "access_token": "eyJhbGciOiJFUzI1NiJ9.eyJqdGkiOiI5NmQ5Njgw...",
                  "expires_in": 3600,
                  "refresh_expires_in": 86400,
                  "endpoint": {
                    "id": "d39433b7-0fbd-4bc2-bdae-fb276799979f",
                    "label": ["Humana"],
                    "name": "humana-sandbox",
                    "refreshable": true,
                    "resources": [
                      "Coverage",
                      "ExplanationOfBenefit",
                      "Patient"
                    ]
                  }
                }
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
            example_request:
              format: javascript
              example: >
                const request = await
                fetch("https://api.flexpa.com/link/exchange", {
                  method: "POST",
                  headers: {
                    "content-type": "application/json",
                  },
                  body: JSON.stringify({
                    public_token: "public_token...",
                    secret_key: "sk_test...",
                  }),
                });

                const { access_token: accessToken, expires_in: expiresIn } =
                await request.json();
            example_response:
              format: json
              example: |
                {
                  "access_token": "eyJhbGciOiJFUzI1NiJ9.eyJqdGkiOiI5NmQ5Njgw...",
                  "expires_in": 3600,
                  "refresh_expires_in": 86400,
                  "endpoint": {
                    "id": "d39433b7-0fbd-4bc2-bdae-fb276799979f",
                    "label": ["Humana"],
                    "name": "humana-sandbox",
                    "refreshable": true,
                    "resources": [
                      "Coverage",
                      "ExplanationOfBenefit",
                      "Patient"
                    ]
                  }
                }
---

