# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Unit tests for ModelRoutingIntent.min_tier_name field (OMN-12256).

Verifies backward compatibility and correct behavior of the optional
min_tier_name field added for delegation tier escalation (OMN-12254).
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from omnibase_compat.contracts.delegation.wire.model_delegation_request import (
    ModelDelegationRequest,
)
from omnibase_compat.contracts.delegation.wire.model_orchestrator_intents import (
    ModelRoutingIntent,
)


def _make_delegation_request() -> ModelDelegationRequest:
    """Create a minimal valid delegation request for testing."""
    return ModelDelegationRequest(
        prompt="test prompt",
        task_type="test",
        correlation_id=uuid4(),
        emitted_at=datetime.now(tz=UTC),
    )


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestModelRoutingIntentMinTierName:
    """Tests for the min_tier_name optional field on ModelRoutingIntent."""

    def test_default_min_tier_name_is_none(self) -> None:
        """Backward compat: existing callers that omit min_tier_name get None."""
        intent = ModelRoutingIntent(payload=_make_delegation_request())
        assert intent.min_tier_name is None

    def test_explicit_none_min_tier_name(self) -> None:
        """Explicitly passing None works."""
        intent = ModelRoutingIntent(
            payload=_make_delegation_request(),
            min_tier_name=None,
        )
        assert intent.min_tier_name is None

    def test_set_min_tier_name_to_string(self) -> None:
        """Escalation path: set min_tier_name to a tier name."""
        intent = ModelRoutingIntent(
            payload=_make_delegation_request(),
            min_tier_name="cheap_cloud",
        )
        assert intent.min_tier_name == "cheap_cloud"

    def test_min_tier_name_in_serialized_output(self) -> None:
        """Field appears in model_dump when set."""
        intent = ModelRoutingIntent(
            payload=_make_delegation_request(),
            min_tier_name="claude",
        )
        data = intent.model_dump()
        assert data["min_tier_name"] == "claude"

    def test_min_tier_name_absent_from_serialized_when_none(self) -> None:
        """Field appears as None in model_dump when not set."""
        intent = ModelRoutingIntent(payload=_make_delegation_request())
        data = intent.model_dump()
        assert data["min_tier_name"] is None

    def test_frozen_prevents_mutation(self) -> None:
        """ModelRoutingIntent is frozen — cannot mutate min_tier_name."""
        intent = ModelRoutingIntent(
            payload=_make_delegation_request(),
            min_tier_name="local",
        )
        with pytest.raises((ValidationError, TypeError)):
            intent.min_tier_name = "claude"  # type: ignore[misc]

    def test_extra_forbid_still_enforced(self) -> None:
        """Adding unknown fields still raises ValidationError."""
        with pytest.raises(ValidationError):
            ModelRoutingIntent(
                payload=_make_delegation_request(),
                min_tier_name="local",
                unknown_extra_field="bad",  # type: ignore[call-arg]
            )

    def test_roundtrip_through_model_validate(self) -> None:
        """Deserialize from dict works with min_tier_name."""
        req = _make_delegation_request()
        raw = {
            "intent": "routing_reducer",
            "payload": req.model_dump(),
            "min_tier_name": "cheap_cloud",
        }
        intent = ModelRoutingIntent.model_validate(raw)
        assert intent.min_tier_name == "cheap_cloud"
        assert intent.payload.prompt == "test prompt"

    def test_roundtrip_without_min_tier_name(self) -> None:
        """Deserialize from dict without min_tier_name (backward compat)."""
        req = _make_delegation_request()
        raw = {
            "intent": "routing_reducer",
            "payload": req.model_dump(),
        }
        intent = ModelRoutingIntent.model_validate(raw)
        assert intent.min_tier_name is None
