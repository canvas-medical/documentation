---
title: "Example Front Matter Blocks"
sections:
  - type: "section"
    blocks:
      - type: "api_parameters"
        summary: "AllergyIntolerance read"
        method: "post"
        url: "/AllergyIntolerance/{id}"
        description: "The AllergyIntolerance search-type interaction searches a set of resources based on some filter criteria."
        parameters:
        - name: "id"
          description: "Logical id of this artifact"
          required: true
          type: "string"
        - name: "_format"
          description: "Override the HTTP content negotiation to specify JSON or XML response format"
          required: false
          type: "string"
        - name: "_pretty"
          description: "Ask for a pretty printed response for human convenience"
          required: false
          type: "string"
        responses:
        - response: 201
          description: "Successful Claim create"
        - response: 400
          description: "Claim create request could not be parsed or failed basic FHIR validation rules."
        attributes:
          - name: "id"
            description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            type: "string"
            attributes:
              - name: "id"
                description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                type: "string"
              - name: "id"
                description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
                type: "string"
          - name: "id"
            description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            type: "string"
        example_request:
          format: "javascript"
          example: >
              const request = await fetch("https://api.flexpa.com/link/exchange", {
                method: "POST",
                headers: {
                  "content-type": "application/json",
                },
                body: JSON.stringify({
                  public_token: "public_token...",
                  secret_key: "sk_test...",
                }),
              });

              const { access_token: accessToken, expires_in: expiresIn } = await request.json();
        example_response:
          format: "json"
          example:  >
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

