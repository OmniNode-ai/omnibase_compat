# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Unit tests for delegation escalation terminal metadata (OMN-12254)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from omnibase_compat.contracts.delegation.wire.model_delegation_result import (
    ModelDelegationResult,
)
from omnibase_compat.contracts.delegation.wire.model_task_delegated_event import (
    ModelTaskDelegatedEvent,
)


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestDelegationEscalationTerminalMetadata:
    def test_delegation_result_defaults_are_backward_compatible(self) -> None:
        result = ModelDelegationResult(
            correlation_id=uuid4(),
            task_type="test",
            model_used="local-coder",
            endpoint_url="http://example.invalid",
            content="ok",
            quality_passed=True,
            quality_score=0.9,
            latency_ms=42,
            fallback_to_claude=False,
        )

        assert result.escalation_count == 0
        assert result.escalation_history == ()
        assert result.terminal_failure_reason is None
        assert result.attempts_count == 1

    def test_delegation_result_accepts_escalation_metadata(self) -> None:
        result = ModelDelegationResult(
            correlation_id=uuid4(),
            task_type="test",
            model_used="cloud-sonnet",
            endpoint_url="https://example.invalid",
            content="",
            quality_passed=False,
            quality_score=0.2,
            latency_ms=99,
            fallback_to_claude=True,
            escalation_count=1,
            escalation_history=({"tier_name": "local", "quality_score": 0.2},),
            terminal_failure_reason="max_escalation_attempts_reached",
            routing_tiers_hash="tiers-hash",
            escalation_config_hash="config-hash",
            attempts_count=2,
            cumulative_attempt_cost=0.3,
            cumulative_input_tokens=100,
            cumulative_output_tokens=200,
            final_attempt_cost=0.2,
        )

        data = result.model_dump()
        assert data["escalation_count"] == 1
        assert data["escalation_history"][0]["tier_name"] == "local"
        assert data["terminal_failure_reason"] == "max_escalation_attempts_reached"

    def test_task_delegated_event_accepts_escalation_metadata(self) -> None:
        event = ModelTaskDelegatedEvent(
            timestamp=datetime.now(tz=UTC).isoformat(),
            correlation_id=uuid4(),
            task_type="test",
            delegated_to="cloud-sonnet",
            quality_gate_passed=False,
            escalation_count=1,
            escalation_history=({"tier_name": "local"},),
            routing_tiers_hash="tiers-hash",
            escalation_config_hash="config-hash",
            attempts_count=2,
            cumulative_attempt_cost=0.3,
        )

        assert event.escalation_count == 1
        assert event.escalation_history == ({"tier_name": "local"},)
        assert event.attempts_count == 2

    def test_extra_forbid_still_applies(self) -> None:
        with pytest.raises(ValidationError):
            ModelDelegationResult(
                correlation_id=uuid4(),
                task_type="test",
                model_used="local-coder",
                endpoint_url="http://example.invalid",
                content="ok",
                quality_passed=True,
                quality_score=0.9,
                latency_ms=42,
                fallback_to_claude=False,
                unknown_extra_field="bad",  # type: ignore[call-arg]
            )
