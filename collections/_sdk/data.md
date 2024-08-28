---
title: "Data"
---

{% include alert.html type="info" content= "<b>Work in progress: </b> We're just getting started here. Check back often for updates!"  %}

# Introduction

The data module provides you with data to compute on. It provides curated,
secure access to both PHI (e.g. patient data) and non-PHI (e.g. staff and
practice-level data), representing the current state of your target Canvas
instance. The module offers convenience methods and operators that
make business logic and clinical logic easy to express with standard
terminologies like ICD-10, SNOMED-CT, CPT, and the like.

Data on your Canvas instance is accessible in plugins through GraphQL. A built-in GraphQL client is included.

A primer on GraphQL can be found here: [https://graphql.org](https://graphql.org)

# Canvas GraphQL schema

An interactive version of Canvas's GraphQL schema is located on your instance: [https://customer-subdomain.canvasmedical.com/graphql-schema](https://customer-subdomain.canvasmedical.com/graphql-schema)

# Example usage

```python
import json

from canvas_sdk.data import GQL_CLIENT
from canvas_sdk.events import EventType
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.protocols import BaseProtocol


class Protocol(BaseProtocol):
    RESPONDS_TO = EventType.Name(EventType.PATIENT_CREATED)

    def compute(self):
        # Define the GraphQL query
        gql_query = """
            query PatientQuery($key: String!) {
                patient(patientKey: $key) {
                    firstAndLastName
                }
            }
        """

        # Execute the query using the provided GQL client
        response = GQL_CLIENT.query(
            gql_query=gql_query,
            variables={
                "key": self.target
            }
        )

        # Pull the patient from the response
        patient = response["patient"]

        ...

        return [
          # Effects
        ]
```

# Crafting GraphQL queries

The most efficient way to craft GraphQL queries is to use an interactive tool like [Postman](https://www.postman.com) or
Canvas's GraphQL schema (referenced above). These tools provide field autocompletion, which makes crafting queries very
easy.

Canvas recommends writing queries that accept variables in order to encourage reuse and consistency. As can be seen in
the example above, variables can be renamed to allow for consistency across different types of queries.

Once you are happy with your query, it can be added to your plugin and executed as shown above in order to obtain data
from your Canvas instance.
