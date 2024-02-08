---
title: Search Parameters
block:
  attributes:
    - name: resourceType
      description: The FHIR Resource name.
      type: string
    - name: type
      description: This element and value designate that the bundle is a search response. Search result bundles will always have the Bundle.type of searchset .
      type: string
    - name: total
      description: The number of resources that match the search parameter.
      type: integer
    - name: link
      description: Attributes relevant to pagination, see our [Pagination page](/api/pagination) for more detail.
      type: array[json]
      attributes:
        - name: relation
          description: The relation of the page search
          enum_options: 
            - value: self
            - value: first
            - value: next
            - value: last
        - name: url
          description: The search url for the specific relation
    - name: entry
      description: The results bundle that lists out each object returned in the search
      type: array[json]
      attributes: 
        - name: resource
          description: The attributes specific to the resource type, see the Attributes section below
          type: json
---
