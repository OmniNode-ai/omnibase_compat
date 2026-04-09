# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.enum_capability_tier import EnumCapabilityTier
from omnibase_compat.overseer.enum_context_bundle_level import EnumContextBundleLevel
from omnibase_compat.overseer.enum_failure_class import EnumFailureClass
from omnibase_compat.overseer.model_completion_report import (
    EnumCompletionOutcome,
    ModelCompletionReport,
)
from omnibase_compat.overseer.model_escalation_request import ModelEscalationRequest


@pytest.mark.unit
def test_escalation_request_requires_failure_class() -> None:
    """Assert ValidationError when failure_class is missing."""
    with pytest.raises(ValidationError):
        ModelEscalationRequest(  # type: ignore[call-arg]
            task_id="task-001",
            domain="ingestion",
            node_id="node-abc",
            # failure_class omitted
        )


@pytest.mark.unit
def test_escalation_request_roundtrip() -> None:
    """Construct with all fields, serialize to dict, re-validate."""
    req = ModelEscalationRequest(
        task_id="task-001",
        domain="ingestion",
        node_id="node-abc",
        failure_class=EnumFailureClass.TRANSIENT,
        capability_tier=EnumCapabilityTier.C3,
        context_bundle_level=EnumContextBundleLevel.L3,
        attempt=2,
        max_attempts_exhausted=5,
        error_message="Connection timed out",
        error_detail={"host": "kafka-1", "port": 9092},
    )
    serialized = req.model_dump(mode="json")
    restored = ModelEscalationRequest.model_validate(serialized)
    assert restored.task_id == "task-001"
    assert restored.failure_class == EnumFailureClass.TRANSIENT
    assert restored.capability_tier == EnumCapabilityTier.C3
    assert restored.context_bundle_level == EnumContextBundleLevel.L3
    assert restored.attempt == 2
    assert restored.max_attempts_exhausted == 5
    assert restored.error_message == "Connection timed out"
    assert restored.error_detail == {"host": "kafka-1", "port": 9092}


@pytest.mark.unit
def test_escalation_request_frozen() -> None:
    """Assert assigning to a field raises."""
    req = ModelEscalationRequest(
        task_id="task-002",
        domain="routing",
        node_id="node-xyz",
        failure_class=EnumFailureClass.PERMANENT,
    )
    with pytest.raises((ValidationError, TypeError)):
        req.failure_class = EnumFailureClass.TRANSIENT  # type: ignore[misc]


@pytest.mark.unit
def test_escalation_request_extra_forbid() -> None:
    """Assert extra fields are rejected."""
    with pytest.raises(ValidationError):
        ModelEscalationRequest(
            task_id="task-003",
            domain="routing",
            node_id="node-xyz",
            failure_class=EnumFailureClass.UNKNOWN,
            bogus_field="should fail",  # type: ignore[call-arg]
        )


@pytest.mark.unit
def test_completion_report_total_cost_non_negative() -> None:
    """Assert ge=0.0 on total_cost."""
    with pytest.raises(ValidationError):
        ModelCompletionReport(
            task_id="task-010",
            domain="ingestion",
            node_id="node-abc",
            outcome=EnumCompletionOutcome.SUCCESS,
            total_cost=-1.0,
        )


@pytest.mark.unit
def test_completion_report_roundtrip() -> None:
    """Full field round-trip."""
    report = ModelCompletionReport(
        task_id="task-010",
        domain="ingestion",
        node_id="node-abc",
        outcome=EnumCompletionOutcome.SUCCESS,
        total_cost=0.42,
        total_duration_seconds=12.5,
        attempts_used=2,
        runner_id="runner-1",
        error_message=None,
        metadata={"model": "gpt-4", "tokens": 1500},
    )
    serialized = report.model_dump(mode="json")
    restored = ModelCompletionReport.model_validate(serialized)
    assert restored.task_id == "task-010"
    assert restored.outcome == EnumCompletionOutcome.SUCCESS
    assert restored.total_cost == pytest.approx(0.42)
    assert restored.total_duration_seconds == pytest.approx(12.5)
    assert restored.attempts_used == 2
    assert restored.runner_id == "runner-1"
    assert restored.metadata == {"model": "gpt-4", "tokens": 1500}


@pytest.mark.unit
def test_completion_report_frozen() -> None:
    """Assert assigning to a field raises."""
    report = ModelCompletionReport(
        task_id="task-011",
        domain="routing",
        node_id="node-xyz",
        outcome=EnumCompletionOutcome.FAILURE,
    )
    with pytest.raises((ValidationError, TypeError)):
        report.outcome = EnumCompletionOutcome.SUCCESS  # type: ignore[misc]


@pytest.mark.unit
def test_completion_report_extra_forbid() -> None:
    """Assert extra fields are rejected."""
    with pytest.raises(ValidationError):
        ModelCompletionReport(
            task_id="task-012",
            domain="routing",
            node_id="node-xyz",
            outcome=EnumCompletionOutcome.CANCELLED,
            bogus_field="should fail",  # type: ignore[call-arg]
        )


@pytest.mark.unit
def test_completion_report_duration_non_negative() -> None:
    """Assert ge=0.0 on total_duration_seconds."""
    with pytest.raises(ValidationError):
        ModelCompletionReport(
            task_id="task-013",
            domain="ingestion",
            node_id="node-abc",
            outcome=EnumCompletionOutcome.TIMEOUT,
            total_duration_seconds=-0.5,
        )


@pytest.mark.unit
def test_completion_outcome_enum_values() -> None:
    """Assert EnumCompletionOutcome has exactly 6 members."""
    assert len(EnumCompletionOutcome) == 6
    expected = {"success", "failure", "partial", "timeout", "cancelled", "skipped"}
    assert {m.value for m in EnumCompletionOutcome} == expected
