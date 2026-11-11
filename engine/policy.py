"""Pure IF/THEN/ELSE policy used by the Omnitech1 reconciler."""

from enum import Enum


class Action(str, Enum):
    HOLD = "hold"
    RESTART = "restart"
    ROLLBACK = "rollback"
    ESCALATE = "escalate"


def decide(*, docker_available: bool, active_exists: bool, active_healthy: bool,
           restart_attempted: bool, previous_healthy: bool) -> Action:
    """Choose one safe action; never infer success from missing evidence."""
    if not docker_available:
        return Action.ESCALATE
    if not active_exists:
        return Action.ROLLBACK if previous_healthy else Action.ESCALATE
    if active_healthy:
        return Action.HOLD
    if not restart_attempted:
        return Action.RESTART
    if previous_healthy:
        return Action.ROLLBACK
    return Action.ESCALATE
