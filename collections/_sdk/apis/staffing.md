---
title: Staffing
---

# Staffing

The Staffing API is responsible for managing staffing-related resources.
It provides a simple interface for managing staff and teams.

## Basic Usage

``` python
>>> from canvas_core import staffing

# Create a Staff user.
>>> staff, generated_password = staffing.create_staff(
...     username="staffuser",
...     email="staff-user@example.com",
...     first_name="Staff",
...     last_name="User",
... )

# Retrieve a staff user by its key.
>>> staff = staffing.get_staff_by_key(key=staff.key)

# Retrieve the service user (useful for automations that require a staff reference).
>>> service_staff = staffing.get_service_user_staff()

# List all active staff.
>>> active_staff = staffing.list_staff()

# Create a team.
>>> my_team = staffing.create_team(name="My Team")

# List staff belonging to a particular team.
>>> my_team_staff = staffing.list_staff(team=my_team)
# Or:
>>> my_team_staff = team.list_members()

# Add a staff member to a team.
>>> staffing.add_staff_to_team(staff=staff, team=my_team)
# Or:
>>> my_team.add_member(staff)

# Remove a staff member from a team.
>>> staffing.remove_staff_from_team(staff=staff, team=my_team)
# Or:
>>> my_team.remove_member(staff)

# Create a team with one or more specific responsibilities.
>>> Team = staffing.get_team_model()
>>> prescriptions_team = staffing.create_team(
...    name="Prescription Management Team",
...    responsibilities=(
...        Team.Responsibility.PROCESS_REFILL_REQUESTS,
...        Team.Responsibility.PROCESS_CHANGE_REQUESTS,
...        # Specify your own custom responsibility strings, if needed.
...        "REVIEW_PRESCRIPTIONS",
...    )
... )

# Retrieve a team by name.
>>> team = staffing.get_team_by_name(name="My Team")

# List all teams.
>>> all_teams = staffing.list_teams()

# List teams with a specific responsibility.
>>> specimen_teams = staffing.list_teams(
...     responsibility=Team.Responsibility.COLLECT_SPECIMENS_FROM_PATIENT
... )
```

## API Reference

::: {.automodule members=""}
canvas_core.staffing
:::

::: {.automodule members="Staff, Team"}
canvas_core.staffing.models
:::
