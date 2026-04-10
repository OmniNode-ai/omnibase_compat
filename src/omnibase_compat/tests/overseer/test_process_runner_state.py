# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.enum_process_runner_state import EnumProcessRunnerState
from omnibase_compat.overseer.model_process_runner_state_transition import (
    ModelProcessRunnerStateTransition,
)


@pytest.mark.unit
def test_enum_has_exactly_10_states() -> None:
    """EnumProcessRunnerState must have exactly 10 members."""
    expected = {
        "idle",
        "planning",
        "executing",
        "verifying",
        "retrying",
        "waiting_dependency",
        "escalating",
        "recovering",
        "completed",
        "failed_terminal",
    }
    assert len(EnumProcessRunnerState) == 10
    assert {s.value for s in EnumProcessRunnerState} == expected


@pytest.mark.unit
def test_transition_requires_from_state_and_to_state() -> None:
    """ModelProcessRunnerStateTransition requires both from_state and to_state."""
    with pytest.raises(ValidationError):
        ModelProcessRunnerStateTransition(from_state=EnumProcessRunnerState.IDLE)  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        ModelProcessRunnerStateTransition(to_state=EnumProcessRunnerState.PLANNING)  # type: ignore[call-arg]

    # Valid construction
    transition = ModelProcessRunnerStateTransition(
        from_state=EnumProcessRunnerState.IDLE,
        to_state=EnumProcessRunnerState.PLANNING,
    )
    assert transition.from_state == EnumProcessRunnerState.IDLE
    assert transition.to_state == EnumProcessRunnerState.PLANNING


@pytest.mark.unit
def test_transition_frozen() -> None:
    """ModelProcessRunnerStateTransition is immutable after construction."""
    transition = ModelProcessRunnerStateTransition(
        from_state=EnumProcessRunnerState.EXECUTING,
        to_state=EnumProcessRunnerState.VERIFYING,
    )
    with pytest.raises((ValidationError, TypeError)):
        transition.from_state = EnumProcessRunnerState.IDLE  # type: ignore[misc]
