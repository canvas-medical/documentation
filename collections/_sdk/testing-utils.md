---
title: "Testing Utilities"
slug: "testing-utils"
hidden: false
---

Canvas SDK provides a streamlined testing environment and local database support to help developers test their plugins with real data, without needing to mock or manually configure anything.

This guide covers two key capabilities:

1. [Plugin testing with pytest](#plugin-testing-with-pytest) — `canvas[test-utils]` introduces a set of tools and dependencies for writing database-backed tests.
2. [Database seeding in CLI](#local-db-seeding-via-run-plugin) — populate or reset your local database when running plugins locally.

---

## Project Structure

The recommended layout for plugin development is now scaffolded automatically by the `canvas init` command. This structure ensures compatibility with Canvas testing tools and CLI features, and it's strongly encouraged for all new plugin projects.
We also recommend to use [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for managing dependencies.

```bash
plugin-folder/
├── my_plugin/
│   └── ...
├── tests/
│   ├── __init__.py
│   └── test_example.py
└── pyproject.toml
```

## Plugin Testing with Pytest

Installing the `test-utils` extra provides everything needed to test plugins with pytest. No additional setup is required.

### Features

* `pytest` ready out of the box.
* Each test is wrapped in a transaction and rolled back automatically.
* Use actual models or prebuilt factories to generate test data.
* No need for mocks or fake database layers.

### Installation

Add the following to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "canvas[test-utils]",
    # other dependencies...
]
```

or install directly via `uv`:

```bash
uv install canvas[test-utils]
````

You can now run your test suite using:

```bash
uv run pytest
```

### Using Factories

Factories simplify test data creation and follow the [`factory_boy`](https://factoryboy.readthedocs.io/en/stable/) pattern.

```python
from canvas_sdk.test_utils.factories import PatientFactory

def test_factory() -> None:
    patient = PatientFactory.create()
    assert patient.id is not None
```

### Using Models Directly

You can also create records manually using the model classes:

```python
from canvas_sdk.v1.data.discount import Discount

def test_model() -> None:
    Discount.objects.create(
        name="10%",
        adjustment_group="30",
        adjustment_code="CO",
        discount=0.10,
    )
    assert Discount.objects.first().pk is not None
```

>  Whether using a factory or model directly, your test will run inside a transaction and automatically roll back at the end.

### Available Factories

All factories are available from:

```python
from canvas_sdk.test_utils import factories
```

Developers are encouraged to add new factories for their own models.


## Local DB Seeding via `run-plugin`

You can run plugins locally with full access to the database using the CLI. Two options are available:

| Option           | Description                                                                                                         |
|------------------|---------------------------------------------------------------------------------------------------------------------|
| `--db-seed-file` | Path to a Python file that populates your database. *Warning*: It resets the database before running the seed file. |
| `--reset-db`     | Clears and recreates the database before running the plugin                                                         |

### Seed the Database

To seed your plugin’s database with test data:

```bash
canvas run-plugin my_plugin --db-seed-file ./seed.py
```

Example `seed.py`:

```python
from canvas_sdk.test_utils.factories import PatientFactory
from canvas_sdk.v1.data.discount import Discount

PatientFactory.create(first_name="Seeded", last_name="Patient")

Discount.objects.create(
    name="20%",
    adjustment_group="X",
    adjustment_code="Y",
    discount=0.20
)
```

### Reset the Database

To reset the database before running a plugin:

```bash
canvas run-plugin my_plugin --reset-db
```

This will remove the existing database (if present) and recreate a clean version.


### Simulate Events

After your database is set up, simulate incoming events with:

```bash
canvas emit
```

Run `canvas emit --help` for more info.
