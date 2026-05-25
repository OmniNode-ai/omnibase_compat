# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Unit tests for ModelTierModel, ModelRoutingTier, ModelDelegationConfig."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from omnibase_compat.contracts.delegation.wire.model_routing_config import (
    ModelDelegationConfig,
    ModelRoutingTier,
    ModelTierModel,
)


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestModelTierModel:
    def test_minimal_valid_tier(self) -> None:
        tier = ModelTierModel(
            id="qwen3-coder",
            backend_ref="LLM_CODER_URL",
            max_context_tokens=112000,
        )
        assert tier.id == "qwen3-coder"
        assert tier.backend_ref == "LLM_CODER_URL"
        assert tier.max_context_tokens == 112000
        assert tier.use_for == ()
        assert tier.fast_path_threshold_tokens is None
        assert tier.min_success_rate == 0.0

    def test_min_success_rate_default_is_zero(self) -> None:
        tier = ModelTierModel(
            id="m",
            backend_ref="ref",
            max_context_tokens=1000,
        )
        assert tier.min_success_rate == 0.0

    def test_min_success_rate_explicit_value(self) -> None:
        tier = ModelTierModel(
            id="m",
            backend_ref="ref",
            max_context_tokens=1000,
            min_success_rate=0.85,
        )
        assert tier.min_success_rate == 0.85

    def test_min_success_rate_zero_means_no_threshold(self) -> None:
        tier = ModelTierModel(
            id="m",
            backend_ref="ref",
            max_context_tokens=1000,
            min_success_rate=0.0,
        )
        assert tier.min_success_rate == 0.0

    def test_tier_is_frozen(self) -> None:
        tier = ModelTierModel(
            id="m",
            backend_ref="ref",
            max_context_tokens=1000,
        )
        with pytest.raises((ValidationError, TypeError)):
            tier.min_success_rate = 0.5  # type: ignore[misc]

    def test_tier_rejects_extra_fields(self) -> None:
        with pytest.raises(ValidationError):
            ModelTierModel(
                id="m",
                backend_ref="ref",
                max_context_tokens=1000,
                unknown="field",  # type: ignore[call-arg]
            )

    def test_use_for_tuple(self) -> None:
        tier = ModelTierModel(
            id="m",
            backend_ref="ref",
            max_context_tokens=1000,
            use_for=("code", "summarize"),
        )
        assert tier.use_for == ("code", "summarize")

    def test_fast_path_threshold_tokens(self) -> None:
        tier = ModelTierModel(
            id="m",
            backend_ref="ref",
            max_context_tokens=1000,
            fast_path_threshold_tokens=512,
        )
        assert tier.fast_path_threshold_tokens == 512


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestModelRoutingTier:
    def test_minimal_routing_tier(self) -> None:
        rt = ModelRoutingTier(name="local")
        assert rt.name == "local"
        assert rt.models == ()
        assert rt.eval_before_accept is False
        assert rt.eval_model is None
        assert rt.max_retries == 0

    def test_routing_tier_is_frozen(self) -> None:
        rt = ModelRoutingTier(name="local")
        with pytest.raises((ValidationError, TypeError)):
            rt.name = "cloud"  # type: ignore[misc]


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestModelDelegationConfig:
    def test_empty_config(self) -> None:
        cfg = ModelDelegationConfig()
        assert cfg.tiers == ()

    def test_config_with_tier_containing_min_success_rate(self) -> None:
        tier = ModelTierModel(
            id="qwen3",
            backend_ref="LLM_CODER_URL",
            max_context_tokens=112000,
            min_success_rate=0.9,
        )
        routing_tier = ModelRoutingTier(name="local", models=(tier,))
        cfg = ModelDelegationConfig(tiers=(routing_tier,))
        assert cfg.tiers[0].models[0].min_success_rate == 0.9
