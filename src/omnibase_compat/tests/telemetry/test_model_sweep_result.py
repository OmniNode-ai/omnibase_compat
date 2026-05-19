# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from omnibase_compat.telemetry import ModelSweepResult


def _valid_sweep_result_kwargs() -> dict[str, object]:
    return {
        "sweep_type": "contract",
        "session_id": "session-123",
        "correlation_id": "correlation-123",
        "ran_at": datetime(2026, 5, 18, tzinfo=UTC),
        "duration_seconds": 1.25,
        "passed": True,
        "summary": "contract sweep completed",
    }


@pytest.mark.unit
def test_sweep_result_accepts_non_negative_duration_and_counts() -> None:
    result = ModelSweepResult(
        sweep_type="contract",
        session_id="session-123",
        correlation_id="correlation-123",
        ran_at=datetime(2026, 5, 18, tzinfo=UTC),
        duration_seconds=1.25,
        passed=True,
        finding_count=0,
        critical_count=1,
        warning_count=2,
        summary="contract sweep completed",
    )

    assert result.duration_seconds == 1.25
    assert result.finding_count == 0
    assert result.critical_count == 1
    assert result.warning_count == 2


@pytest.mark.unit
@pytest.mark.parametrize(
    ("field_name", "value"),
    (
        ("duration_seconds", -0.01),
        ("finding_count", -1),
        ("critical_count", -1),
        ("warning_count", -1),
    ),
)
def test_sweep_result_rejects_negative_numeric_telemetry(
    field_name: str,
    value: float | int,
) -> None:
    kwargs = _valid_sweep_result_kwargs()
    kwargs[field_name] = value

    with pytest.raises(ValidationError):
        ModelSweepResult.model_validate(kwargs)
