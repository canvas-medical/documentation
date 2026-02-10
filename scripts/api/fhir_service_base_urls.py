"""
Script that creates FHIR service base URL JSON files for all customer instances.

This script has inline dependencies specified, so it does not require a pyproject.toml file to use
with uv. The only prerequisite is that uv is installed.

This script queries the Canvas Console API to get instance and organization data, then generates
FHIR Bundle JSON files for non-production and production environments.

Steps for updating the FHIR service base URLs in the documentation repository:

1. Create a branch in the documentation repository.
2. Set the CONSOLE_AUTH_TOKEN environment variable to your Canvas Console auth token.
3. Run the script: uv run fhir_service_base_urls.py
4. Create a PR from your branch and merge it.
"""

# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "fhir-resources==8.2.0",
#   "httpx==0.28.1",
# ]
# ///

import argparse
import os
import uuid
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

import httpx
from fhir.resources.R4B.bundle import Bundle, BundleEntry
from fhir.resources.R4B.endpoint import Endpoint
from fhir.resources.R4B.organization import Organization

CONSOLE_BASE_URL = "https://console.canvasmedical.com/api/v1/provisioning"
CONSOLE_API_TIMEOUT = 600
CONSOLE_TAG_TO_TYPE = {
    "customer_dev": "dev",
    "customer_staging": "staging",
    "customer_prod": "prod",
}
CONSOLE_SQL_QUERY = (
    "SELECT org.id, org.full_name, address.line1, address.line2, address.city,"
    " address.state_code, address.postal_code"
    " FROM api_organizationaddress as address"
    " INNER JOIN api_organization as org ON address.organization_id = org.id;"
)

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "_static"
DEFAULT_NONPROD_FILENAME = "fhir-service-base-urls-nonproduction.json"
DEFAULT_PROD_FILENAME = "fhir-service-base-urls-production.json"


def fetch_instance_types(client: httpx.Client) -> dict[str, str]:
    """Fetch instance type (dev/staging/prod) for each customer slug."""
    response = client.post(f"{CONSOLE_BASE_URL}/instances")
    response.raise_for_status()

    slug_to_type: dict[str, str] = {}
    for instance in response.json():
        slug = instance["slug"]
        for tag in instance["tags"]:
            if tag in CONSOLE_TAG_TO_TYPE:
                slug_to_type[slug] = CONSOLE_TAG_TO_TYPE[tag]
                break

    return slug_to_type


def fetch_org_data(client: httpx.Client) -> list[dict[str, Any]]:
    """Fetch organization and address data from the Console query API."""
    response = client.post(
        f"{CONSOLE_BASE_URL}/instances/query/",
        json={"sql": CONSOLE_SQL_QUERY},
    )
    response.raise_for_status()
    return cast(list[dict[str, Any]], response.json())


def load_orgs(auth_token: str) -> dict[str, dict[str, Any]]:
    """Fetch data from the Console API and organize into a dict keyed by org_name."""
    orgs: dict[str, dict[str, Any]] = {}
    customer_org_ids: dict[str, str] = {}

    with httpx.Client(
        headers={"Authorization": f"Token {auth_token}"},
        timeout=CONSOLE_API_TIMEOUT,
        follow_redirects=True,
    ) as client:
        slug_to_type = fetch_instance_types(client)
        rows = fetch_org_data(client)

    for row in rows:
        if row.get("_error"):
            continue

        customer_identifier = row["_instance"]
        org_id = str(row["id"])
        org_name = row["full_name"].strip()

        org_type = slug_to_type.get(customer_identifier)
        if org_type is None:
            continue

        address = {
            "line1": row["line1"].strip(),
            "line2": row["line2"].strip(),
            "city": row["city"].strip(),
            "state": row["state_code"].strip(),
            "postal_code": row["postal_code"].strip(),
        }

        if customer_identifier in customer_org_ids:
            if customer_org_ids[customer_identifier] != org_id:
                raise RuntimeError(
                    f"Customer identifier '{customer_identifier}' is associated with "
                    f"multiple org_ids: '{customer_org_ids[customer_identifier]}' and '{org_id}'"
                )
        else:
            customer_org_ids[customer_identifier] = org_id

        if org_name not in orgs:
            orgs[org_name] = {
                "id": str(uuid.uuid4()),
                "addresses": [],
                "customer_identifiers": [],
            }

        if address not in orgs[org_name]["addresses"]:
            orgs[org_name]["addresses"].append(address)

        customer = {"value": customer_identifier, "type": org_type}
        if customer not in orgs[org_name]["customer_identifiers"]:
            orgs[org_name]["customer_identifiers"].append(customer)

    org_identifier_value_counter = 1
    for org_name, org_data in sorted(orgs.items()):
        org_data["identifier_value"] = str(org_identifier_value_counter)
        org_identifier_value_counter += 1

    return orgs


def build_bundle(orgs: Mapping[str, Mapping[str, Any]], mode: str) -> Bundle:
    """Build a FHIR Bundle with Endpoint and Organization resources."""
    entries: list[BundleEntry] = []

    for org_name, org_data in sorted(orgs.items()):
        matching_customers = [
            c
            for c in org_data["customer_identifiers"]
            if (mode == "prod" and c["type"] == "prod")
            or (mode == "nonprod" and c["type"] in ("dev", "staging"))
        ]

        if not matching_customers:
            continue

        endpoint_ids = []
        for customer in matching_customers:
            endpoint = Endpoint.model_validate(
                {
                    "id": str(uuid.uuid4()),
                    "status": "active",
                    "connectionType": {
                        "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
                        "code": "hl7-fhir-rest",
                        "display": "HL7 FHIR",
                    },
                    "payloadType": [{"text": "Canvas FHIR Service Base URL"}],
                    "address": f"https://fumage-{customer['value']}.canvasmedical.com",
                }
            )
            entries.append(
                BundleEntry.model_validate(
                    {"resource": endpoint, "fullUrl": f"urn:uuid:{endpoint.id}"}
                )
            )
            endpoint_ids.append(endpoint.id)

        organization = Organization.model_validate(
            {
                "id": org_data["id"],
                "identifier": [
                    {
                        "system": "http://canvasmedical.com",
                        "value": org_data["identifier_value"],
                    }
                ],
                "name": org_name,
                "address": [
                    {
                        "line": [l for l in (address["line1"], address["line2"]) if l],
                        "city": address["city"],
                        "state": address["state"],
                        "postalCode": address["postal_code"],
                    }
                    for address in org_data["addresses"]
                ],
                "endpoint": [{"reference": f"Endpoint/{e}"} for e in endpoint_ids],
            }
        )
        entries.append(
            BundleEntry.model_validate(
                {"resource": organization, "fullUrl": f"urn:uuid:{organization.id}"}
            )
        )

    return Bundle(type="collection", entry=entries)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create FHIR service base URLs for all customer instances"
    )
    parser.add_argument(
        "nonprod_output_file",
        nargs="?",
        default=str(STATIC_DIR / DEFAULT_NONPROD_FILENAME),
        help="Output file for nonprod bundle",
    )
    parser.add_argument(
        "prod_output_file",
        nargs="?",
        default=str(STATIC_DIR / DEFAULT_PROD_FILENAME),
        help="Output file for prod bundle",
    )
    args = parser.parse_args()

    auth_token = os.environ.get("CONSOLE_AUTH_TOKEN")
    if not auth_token:
        raise RuntimeError("CONSOLE_AUTH_TOKEN environment variable is required")

    orgs = load_orgs(auth_token)

    for mode, output_file in [
        ("nonprod", args.nonprod_output_file),
        ("prod", args.prod_output_file),
    ]:
        bundle = build_bundle(orgs, mode)
        with open(output_file, "w") as f:
            f.write(bundle.model_dump_json(indent=2, exclude_none=True))


if __name__ == "__main__":
    main()
