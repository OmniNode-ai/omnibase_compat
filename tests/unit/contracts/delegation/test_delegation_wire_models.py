# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for delegation wire model schema parity and new fields (OMN-11969)."""

from __future__ import annotations

import re
from uuid import uuid4

import pytest

from omnibase_compat.contracts.delegation.wire.model_bifrost_delegation_config import (
    ModelDelegationBackendConfig,
)
from omnibase_compat.contracts.delegation.wire.model_delegation_request import (
    MAX_WORDS_PER_SENTENCE_RE,
    SUPPORTED_ACCEPTANCE_CRITERIA,
    ModelDelegationRequest,
)
from omnibase_compat.contracts.delegation.wire.model_orchestrator_intents import (
    ModelInferenceIntent,
    ModelInferenceResponseData,
)
from omnibase_compat.contracts.delegation.wire.model_routing_config import (
    ModelRoutingTier,
)


@pytest.mark.unit
class TestModelInferenceIntentNewFields:
    """Verify api_key, extra_headers, and timeout_seconds on ModelInferenceIntent."""

    def test_defaults_are_none(self) -> None:
        intent = ModelInferenceIntent(
            base_url="http://localhost:8000",
            model="test-model",
            system_prompt="you are helpful",
            prompt="hello",
            max_tokens=100,
            correlation_id=uuid4(),
        )
        assert intent.api_key is None
        assert intent.extra_headers is None
        assert intent.timeout_seconds == 30.0

    def test_api_key_populated(self) -> None:
        intent = ModelInferenceIntent(
            base_url="http://localhost:8000",
            model="test-model",
            system_prompt="you are helpful",
            prompt="hello",
            max_tokens=100,
            correlation_id=uuid4(),
            api_key="sk-test-key-123",
        )
        assert intent.api_key == "sk-test-key-123"

    def test_extra_headers_populated(self) -> None:
        headers = {"X-Custom-Header": "value", "Authorization": "Bearer xyz"}
        intent = ModelInferenceIntent(
            base_url="http://localhost:8000",
            model="test-model",
            system_prompt="you are helpful",
            prompt="hello",
            max_tokens=100,
            correlation_id=uuid4(),
            extra_headers=headers,
        )
        assert intent.extra_headers == headers

    def test_timeout_seconds_custom(self) -> None:
        intent = ModelInferenceIntent(
            base_url="http://localhost:8000",
            model="test-model",
            system_prompt="you are helpful",
            prompt="hello",
            max_tokens=100,
            correlation_id=uuid4(),
            timeout_seconds=120.0,
        )
        assert intent.timeout_seconds == 120.0

    def test_timeout_seconds_validation_min(self) -> None:
        with pytest.raises(Exception):  # noqa: B017
            ModelInferenceIntent(
                base_url="http://localhost:8000",
                model="test-model",
                system_prompt="you are helpful",
                prompt="hello",
                max_tokens=100,
                correlation_id=uuid4(),
                timeout_seconds=0.5,
            )

    def test_frozen_model(self) -> None:
        intent = ModelInferenceIntent(
            base_url="http://localhost:8000",
            model="test-model",
            system_prompt="you are helpful",
            prompt="hello",
            max_tokens=100,
            correlation_id=uuid4(),
        )
        with pytest.raises(Exception):  # noqa: B017
            intent.api_key = "changed"  # type: ignore[misc]


@pytest.mark.unit
class TestModelInferenceResponseDataErrorMessage:
    """Verify error_message field on ModelInferenceResponseData."""

    def test_default_empty(self) -> None:
        data = ModelInferenceResponseData(
            correlation_id=uuid4(),
            content="generated text",
            model_used="test-model",
        )
        assert data.error_message == ""

    def test_with_error_message(self) -> None:
        data = ModelInferenceResponseData(
            correlation_id=uuid4(),
            content="",
            model_used="test-model",
            error_message="Connection timed out",
        )
        assert data.error_message == "Connection timed out"


@pytest.mark.unit
class TestModelDelegationBackendConfigNewFields:
    """Verify api_key_env and extra_headers on ModelDelegationBackendConfig."""

    def test_defaults(self) -> None:
        config = ModelDelegationBackendConfig(
            backend_id="local-qwen",
            model_name="Qwen3-Coder-30B",
            tier="local",
        )
        assert config.api_key_env is None
        assert config.extra_headers is None

    def test_with_api_key_env_and_headers(self) -> None:
        config = ModelDelegationBackendConfig(
            backend_id="cloud-provider",
            model_name="gpt-4",
            tier="frontier_api",
            api_key_env="PROVIDER_API_KEY",
            extra_headers={"X-Provider": "custom"},
        )
        assert config.api_key_env == "PROVIDER_API_KEY"
        assert config.extra_headers == {"X-Provider": "custom"}


@pytest.mark.unit
class TestModelRoutingTierCostField:
    """Verify cost_per_1k_tokens on ModelRoutingTier."""

    def test_default_zero(self) -> None:
        tier = ModelRoutingTier(name="local")
        assert tier.cost_per_1k_tokens == 0.0

    def test_custom_cost(self) -> None:
        tier = ModelRoutingTier(name="cheap_cloud", cost_per_1k_tokens=0.002)
        assert tier.cost_per_1k_tokens == 0.002


@pytest.mark.unit
class TestModelDelegationRequestTaskTypes:
    """Verify expanded task_type Literal."""

    @pytest.mark.parametrize(
        "task_type",
        [
            "test",
            "document",
            "research",
            "code_generation",
            "refactor",
            "reasoning",
            "complex_reasoning",
            "planning",
            "review",
            "summarization",
            "agent_delegation",
            "escalation",
        ],
    )
    def test_all_task_types_accepted(self, task_type: str) -> None:
        from datetime import UTC, datetime

        req = ModelDelegationRequest(
            prompt="test prompt",
            task_type=task_type,  # type: ignore[arg-type]
            correlation_id=uuid4(),
            emitted_at=datetime.now(UTC),
        )
        assert req.task_type == task_type


@pytest.mark.unit
class TestDelegationRequestExports:
    """Verify package-level exports include constants."""

    def test_max_words_re_exported(self) -> None:
        assert isinstance(MAX_WORDS_PER_SENTENCE_RE, re.Pattern)

    def test_supported_criteria_exported(self) -> None:
        assert isinstance(SUPPORTED_ACCEPTANCE_CRITERIA, frozenset)
        assert "response_non_empty" in SUPPORTED_ACCEPTANCE_CRITERIA


@pytest.mark.unit
class TestMigrationAnnotations:
    """Verify COMPAT_MIGRATION_TARGET annotations exist in module docstrings."""

    @pytest.mark.parametrize(
        "module_path",
        [
            "omnibase_compat.contracts.delegation.wire.model_orchestrator_intents",
            "omnibase_compat.contracts.delegation.wire.model_delegation_request",
            "omnibase_compat.contracts.delegation.wire.model_bifrost_delegation_config",
            "omnibase_compat.contracts.delegation.wire.model_routing_config",
            "omnibase_compat.contracts.delegation.wire.model_budget",
            "omnibase_compat.contracts.delegation.wire.model_delegation_result",
            "omnibase_compat.contracts.delegation.wire.model_event_envelope",
            "omnibase_compat.contracts.delegation.wire.model_quality_gate",
            "omnibase_compat.contracts.delegation.wire.model_task_delegated_event",
        ],
    )
    def test_migration_annotation_present(self, module_path: str) -> None:
        import importlib

        mod = importlib.import_module(module_path)
        assert mod.__doc__ is not None
        assert "COMPAT_MIGRATION_TARGET: omnibase_core" in mod.__doc__
        assert "COMPAT_REMOVAL_DATE: 2026-06-25" in mod.__doc__
