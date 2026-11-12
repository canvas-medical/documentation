import json
from typing import Any

from fhir_service_base_urls import organize_orgs, render_bundle

SLUG_TO_TYPE = {
    "acme": "prod",
    "acme-staging": "staging",
    "globex": "prod",
    "initech": "prod",
}


def row(instance: str, org_id: int, name: str, line1: str) -> dict[str, Any]:
    return {
        "_instance": instance,
        "id": org_id,
        "full_name": name,
        "line1": line1,
        "line2": "",
        "city": "Springfield",
        "state_code": "OR",
        "postal_code": "97477",
    }


ROWS = [
    row("acme", 1, "Acme", "1 Main St"),
    row("acme-staging", 7, "Acme", "1 Main St"),
    row("globex", 3, "Globex", "2 Oak Ave"),
]


def bundles(rows: list[dict[str, Any]]) -> dict[str, str]:
    orgs = organize_orgs(SLUG_TO_TYPE, rows)
    return {mode: render_bundle(orgs, mode) for mode in ("prod", "nonprod")}


def entries_by_id(bundle_json: str) -> dict[str, dict[str, Any]]:
    return {e["resource"]["id"]: e for e in json.loads(bundle_json)["entry"]}


def test_same_input_generates_identical_bundles() -> None:
    assert bundles(ROWS) == bundles(list(ROWS))


def test_row_order_does_not_change_output() -> None:
    assert bundles(ROWS) == bundles(list(reversed(ROWS)))


def test_adding_an_instance_changes_only_its_entries() -> None:
    before = entries_by_id(bundles(ROWS)["prod"])
    after = entries_by_id(bundles([*ROWS, row("initech", 9, "Initech", "3 Elm Rd")])["prod"])

    added = {i: e for i, e in after.items() if i not in before}
    assert sorted(e["resource"]["resourceType"] for e in added.values()) == [
        "Endpoint",
        "Organization",
    ]
    assert {i: after[i] for i in before} == before


def test_nonprod_unaffected_by_prod_change() -> None:
    before = bundles(ROWS)["nonprod"]
    after = bundles([*ROWS, row("initech", 9, "Initech", "3 Elm Rd")])["nonprod"]
    assert before == after


def test_references_resolve_within_bundle() -> None:
    for bundle_json in bundles(ROWS).values():
        entries = json.loads(bundle_json)["entry"]
        endpoint_ids = set()
        for entry in entries:
            resource = entry["resource"]
            assert entry["fullUrl"] == f"urn:uuid:{resource['id']}"
            if resource["resourceType"] == "Endpoint":
                endpoint_ids.add(resource["id"])
        references = [
            ref["reference"]
            for entry in entries
            if entry["resource"]["resourceType"] == "Organization"
            for ref in entry["resource"]["endpoint"]
        ]
        assert references
        assert {r.removeprefix("Endpoint/") for r in references} == endpoint_ids
