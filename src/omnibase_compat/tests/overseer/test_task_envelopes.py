# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.model_task_delta_envelope import ModelTaskDeltaEnvelope
from omnibase_compat.overseer.model_task_state_envelope import (
    EnumTaskStatus,
    ModelTaskStateEnvelope,
)


@pytest.mark.unit
def test_task_state_envelope_roundtrip() -> None:
    """Construct with all fields, serialize to dict, re-validate."""
    envelope = ModelTaskStateEnvelope(
        task_id="task-001",
        status=EnumTaskStatus.RUNNING,
        domain="ingestion",
        node_id="node-abc",
        runner_id="runner-1",
        attempt=2,
        payload={"input": "data"},
        error=None,
    )
    serialized = envelope.model_dump(mode="json")
    restored = ModelTaskStateEnvelope.model_validate(serialized)
    assert restored.task_id == "task-001"
    assert restored.status == EnumTaskStatus.RUNNING
    assert restored.domain == "ingestion"
    assert restored.node_id == "node-abc"
    assert restored.runner_id == "runner-1"
    assert restored.attempt == 2
    assert restored.payload == {"input": "data"}


@pytest.mark.unit
def test_task_delta_envelope_requires_task_id() -> None:
    """Assert ValidationError when task_id missing."""
    with pytest.raises(ValidationError):
        ModelTaskDeltaEnvelope()  # type: ignore[call-arg]


@pytest.mark.unit
def test_task_state_envelope_frozen() -> None:
    """Assert assigning to .status raises."""
    envelope = ModelTaskStateEnvelope(
        task_id="task-002",
        status=EnumTaskStatus.PENDING,
        domain="routing",
        node_id="node-xyz",
    )
    with pytest.raises((ValidationError, TypeError)):
        envelope.status = EnumTaskStatus.RUNNING  # type: ignore[misc]


@pytest.mark.unit
def test_task_status_enum_values_exact() -> None:
    """Assert EnumTaskStatus has exactly 10 members."""
    assert len(EnumTaskStatus) == 10
    expected = {
        "pending",
        "queued",
        "dispatched",
        "running",
        "paused",
        "completed",
        "failed",
        "cancelled",
        "timeout",
        "skipped",
    }
    assert {s.value for s in EnumTaskStatus} == expected


@pytest.mark.unit
def test_task_delta_envelope_partial_update() -> None:
    """Delta envelope allows partial fields (only task_id required)."""
    delta = ModelTaskDeltaEnvelope(
        task_id="task-003",
        status=EnumTaskStatus.FAILED,
        error="timeout exceeded",
    )
    assert delta.task_id == "task-003"
    assert delta.status == EnumTaskStatus.FAILED
    assert delta.error == "timeout exceeded"
    assert delta.runner_id is None
    assert delta.attempt is None
    assert delta.payload is None


@pytest.mark.unit
def test_task_state_envelope_forbids_extra() -> None:
    """Extra fields are rejected."""
    with pytest.raises(ValidationError):
        ModelTaskStateEnvelope(
            task_id="task-004",
            status=EnumTaskStatus.PENDING,
            domain="routing",
            node_id="node-xyz",
            unknown_field="bad",  # type: ignore[call-arg]
        )


@pytest.mark.unit
def test_task_delta_envelope_frozen() -> None:
    """Delta envelope is also frozen."""
    delta = ModelTaskDeltaEnvelope(task_id="task-005")
    with pytest.raises((ValidationError, TypeError)):
        delta.task_id = "mutated"  # type: ignore[misc]
