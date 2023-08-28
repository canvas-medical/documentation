# Goals

The Goals API is responsible for managing goals. The API provides events
so you can react to creating, updating, and closing a Goal

## Events

The following events are emitted:

::: {.automodule members=""}
canvas_core.goals.events
:::

## Examples

``` python
from typing import Any

from canvas_core import events, logging
from canvas_core.goals.events import PostGoalCreate, PostGoalUpdate, PreGoalClose, PostGoalClose

logger = logging.get_logger(__name__)


@events.handle_event(PostGoalCreate)
def handle_new_goal(event: PostGoalCreate) -> None:
    logger.info("Goal created!", externally_exposable_id=event.externally_exposable_id,
                lifecycle_status=event.lifecycle_status,
                achievement_status=event.achievement_status,
                progress=event.progress)


@events.handle_event(PostGoalUpdate)
def handle_goal_updated(event: PostGoalUpdate) -> None:
    logger.info("Goal updated!", externally_exposable_id=event.externally_exposable_id,
                lifecycle_status=event.lifecycle_status,
                new_lifecycle_status=event.new_lifecycle_status,
                old_achievement_status=event.achievement_status,
                new_achievement_status=event.new_achievement_status,
                progress=event.progress,
                new_progress=event.new_progress,
                )


@events.handle_event(PreGoalClose)
def handle_before_goal_close(event: PreGoalClose) -> None:
    logger.info("Goal will be closed!", externally_exposable_id=event.externally_exposable_id,
                lifecycle_status=event.lifecycle_status,
                new_lifecycle_status=event.new_lifecycle_status,
                old_achievement_status=event.achievement_status,
                new_achievement_status=event.new_achievement_status,
                progress=event.progress,
                new_progress=event.new_progress,
                )


@events.handle_event(PostGoalClose)
def handle_goal_close(event: PostGoalClose) -> None:
    logger.info("Goal closed!", externally_exposable_id=event.externally_exposable_id,
                lifecycle_status=event.lifecycle_status,
                new_lifecycle_status=event.new_lifecycle_status,
                old_achievement_status=event.achievement_status,
                new_achievement_status=event.new_achievement_status,
                progress=event.progress,
                new_progress=event.new_progress,
                )
```

## API Reference

::: {.automodule members="Goal, UpdateGoal"}
canvas_core.goals.models
:::
