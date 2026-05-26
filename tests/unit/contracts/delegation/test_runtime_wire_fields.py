# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Regression tests for delegation runtime wire fields."""

from __future__ import annotations

from uuid import uuid4

import pytest

from omnibase_compat.contracts.delegation.wire.model_orchestrator_intents import (
    ModelInferenceIntent,
    ModelInferenceResponseData,
)
from omnibase_compat.contracts.delegation.wire.model_routing_config import (
    ModelRoutingTier,
)


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_inference_intent_accepts_runtime_dispatch_fields() -> None:
    intent = ModelInferenceIntent(
        base_url="https://example.invalid",
        model="test-model",
        system_prompt="system",
        prompt="prompt",
        max_tokens=128,
        timeout_seconds=42.0,
        correlation_id=uuid4(),
        api_key="secret",
        extra_headers={"HTTP-Referer": "https://example.invalid"},
    )

    assert intent.timeout_seconds == 42.0
    assert intent.api_key == "secret"
    assert intent.extra_headers == {"HTTP-Referer": "https://example.invalid"}


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_inference_response_accepts_error_message() -> None:
    response = ModelInferenceResponseData(
        correlation_id=uuid4(),
        content="",
        model_used="test-model",
        error_message="TimeoutError: inference timed out",
    )

    assert response.error_message == "TimeoutError: inference timed out"


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_routing_tier_accepts_cost_per_1k_tokens() -> None:
    tier = ModelRoutingTier(name="cheap_cloud", cost_per_1k_tokens=0.002)

    assert tier.cost_per_1k_tokens == 0.002
