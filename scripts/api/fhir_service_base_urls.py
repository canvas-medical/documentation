"""
Script that creates FHIR service base URL JSON files for all customer instances.

This script has inline dependencies specified, so it does not require a pyproject.toml file to use
with uv. The only prerequisite is that uv is installed.

This script queries the Canvas Console API to get instance and organization data, then generates
FHIR Bundle JSON files for non-production and production environments.

Steps for updating the FHIR service base URLs in the documentation repository:

1. Create a branch in the documentation repository.
2. Set the CONSOLE_BASE_URL environment variable to the correct value
   (see https://www.notion.so/canvasmedical/REST-API-3040bd9e403380a8ba1ac0b4a498ac5b).
3. Set the CONSOLE_AUTH_TOKEN environment variable to your Canvas Console auth token.
4. Run the script: uv run fhir_service_base_urls.py
5. Create a PR from your branch and merge it.

The script exits with an error before contacting Console if CONSOLE_BASE_URL or
CONSOLE_AUTH_TOKEN is unset.

Output is deterministic: every Endpoint and Organization id is a UUIDv5 derived from a stable
key (the Endpoint's service base URL, the Organization's name), and entries are sorted. The same
instance list therefore produces byte-identical bundles, and a change to one instance changes
only the entries for that instance and its Organization.

The .github/workflows/refresh-fhir-service-base-urls.yml GitHub Actions workflow runs this
script quarterly (and on demand). When the regenerated bundles differ from the published ones it
opens a PR for engineering review; when they match, no PR is opened and the workflow run summary
records the review as "reviewed, no changes".
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

CONSOLE_API_BASE_URL = os.environ.get("CONSOLE_BASE_URL", "")
CONSOLE_AUTH_TOKEN = os.environ.get("CONSOLE_AUTH_TOKEN", "")
CONSOLE_API_TIMEOUT = int(os.environ.get("CONSOLE_API_TIMEOUT", "600"))

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

# Fixed namespace for the UUIDv5 resource ids. Changing it changes every published id.
RESOURCE_ID_NAMESPACE = uuid.uuid5(
    uuid.NAMESPACE_URL, "https://docs.canvasmedical.com/_static/fhir-service-base-urls"
)

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "_static"
DEFAULT_NONPROD_FILENAME = "fhir-service-base-urls-nonproduction.json"
DEFAULT_PROD_FILENAME = "fhir-service-base-urls-production.json"


def fetch_instance_types(client: httpx.Client) -> dict[str, str]:
    """Fetch instance type (dev/staging/prod) for each customer slug."""
    response = client.post(f"{CONSOLE_API_BASE_URL}/instances")
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
        f"{CONSOLE_API_BASE_URL}/instances/query/",
        json={"sql": CONSOLE_SQL_QUERY},
    )
    response.raise_for_status()
    return cast(list[dict[str, Any]], response.json())


def resource_id(resource_type: str, key: str) -> str:
    """Return a stable UUIDv5 id for a resource, derived from its type and a stable key."""
    return str(uuid.uuid5(RESOURCE_ID_NAMESPACE, f"{resource_type}:{key}"))


def endpoint_address(customer_identifier: str) -> str:
    """Return the FHIR service base URL for a customer instance."""
    return f"https://fumage-{customer_identifier}.canvasmedical.com"


def load_orgs() -> dict[str, dict[str, Any]]:
    """Fetch data from the Console API and organize into a dict keyed by org_name."""
    with httpx.Client(
        headers={"Authorization": f"Token {CONSOLE_AUTH_TOKEN}"},
        timeout=CONSOLE_API_TIMEOUT,
        follow_redirects=True,
    ) as client:
        slug_to_type = fetch_instance_types(client)
        rows = fetch_org_data(client)

    return organize_orgs(slug_to_type, rows)


def organize_orgs(
    slug_to_type: Mapping[str, str],
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Organize Console query rows into a dict keyed by org_name, in a stable order."""
    orgs: dict[str, dict[str, Any]] = {}
    customer_org_ids: dict[str, str] = {}

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
                "id": resource_id("Organization", org_name),
                "addresses": [],
                "customer_identifiers": [],
            }

        if address not in orgs[org_name]["addresses"]:
            orgs[org_name]["addresses"].append(address)

        customer = {"value": customer_identifier, "type": org_type}
        if customer not in orgs[org_name]["customer_identifiers"]:
            orgs[org_name]["customer_identifiers"].append(customer)

    # Console returns rows in no guaranteed order, so sort everything that ends up in the output.
    for org_data in orgs.values():
        org_data["addresses"].sort(
            key=lambda a: (a["line1"], a["line2"], a["city"], a["state"], a["postal_code"])
        )
        org_data["customer_identifiers"].sort(key=lambda c: (c["value"], c["type"]))

    return dict(sorted(orgs.items()))


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
            base_url = endpoint_address(customer["value"])
            endpoint = Endpoint.model_validate(
                {
                    "id": resource_id("Endpoint", base_url),
                    "status": "active",
                    "connectionType": {
                        "system": "http://terminology.hl7.org/CodeSystem/endpoint-connection-type",
                        "code": "hl7-fhir-rest",
                        "display": "HL7 FHIR",
                    },
                    "payloadType": [{"text": "Canvas FHIR Service Base URL"}],
                    "address": base_url,
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
                        "value": org_data["id"],
                    }
                ],
                "name": org_name,
                "address": [
                    {
                        "line": [line for line in (address["line1"], address["line2"]) if line],
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


def render_bundle(orgs: Mapping[str, Mapping[str, Any]], mode: str) -> str:
    """Render the bundle for a mode as the JSON text that gets published."""
    return build_bundle(orgs, mode).model_dump_json(indent=2, exclude_none=True)


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

    missing = [
        name
        for name, value in (
            ("CONSOLE_BASE_URL", CONSOLE_API_BASE_URL),
            ("CONSOLE_AUTH_TOKEN", CONSOLE_AUTH_TOKEN),
        )
        if not value
    ]
    if missing:
        raise SystemExit(f"Missing required environment variable(s): {', '.join(missing)}")

    orgs = load_orgs()

    for mode, output_file in [
        ("nonprod", args.nonprod_output_file),
        ("prod", args.prod_output_file),
    ]:
        with open(output_file, "w") as f:
            f.write(render_bundle(orgs, mode))


if __name__ == "__main__":
    main()
