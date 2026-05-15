# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Round-trip and validation coverage for canonical delegation wire DTOs."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import BaseModel, ValidationError

from omnibase_compat.contracts.delegation import wire
from omnibase_compat.contracts.delegation.wire import (
    EnumBudgetAction,
    ModelBaselineIntent,
    ModelBifrostDelegationConfig,
    ModelBudgetLimits,
    ModelComplianceLoopResult,
    ModelDelegationBackendConfig,
    ModelDelegationConfig,
    ModelDelegationEventEnvelope,
    ModelDelegationFallbackPolicy,
    ModelDelegationRequest,
    ModelDelegationResult,
    ModelDelegationRoutingRule,
    ModelInferenceIntent,
    ModelInferenceResponseData,
    ModelQualityGateInput,
    ModelQualityGateIntent,
    ModelQualityGateResult,
    ModelRoutingIntent,
    ModelRoutingTier,
    ModelTaskDelegatedEvent,
    ModelTierModel,
    validate_acceptance_criteria,
)

CORRELATION_ID = UUID("11111111-1111-1111-1111-111111111111")
SESSION_ID = UUID("22222222-2222-2222-2222-222222222222")
RULE_ID = UUID("33333333-3333-3333-3333-333333333333")
SHADOW_POLICY_ID = UUID("44444444-4444-4444-4444-444444444444")


def _round_trip[T: BaseModel](model: T) -> T:
    return type(model).model_validate_json(model.model_dump_json())


def _request() -> ModelDelegationRequest:
    return ModelDelegationRequest(
        prompt="Write two focused test cases.",
        task_type="test",
        source_session_id="session-1",
        source_file_path="src/example.py",
        correlation_id=CORRELATION_ID,
        emitted_at=datetime(2026, 5, 14, 20, 15, tzinfo=UTC),
        output_schema_key="delegation.result.v1",
        compliance_budget=ModelBudgetLimits(
            max_tokens=4096,
            max_cost_usd=0.25,
            max_time_s=45.0,
        ),
        acceptance_criteria=("response_non_empty", "max_words_per_sentence_12"),
    )


def _result() -> ModelDelegationResult:
    return ModelDelegationResult(
        correlation_id=CORRELATION_ID,
        task_type="test",
        model_used="qwen3-coder",
        endpoint_url="http://127.0.0.1:8000/v1/chat/completions",
        content="Focused test output.",
        quality_passed=True,
        quality_score=0.94,
        latency_ms=321,
        prompt_tokens=120,
        completion_tokens=45,
        total_tokens=165,
        fallback_to_claude=False,
        tokens_to_compliance=165,
        compliance_attempts=1,
    )


def test_delegation_request_round_trip_and_validation() -> None:
    request = _request()

    assert _round_trip(request) == request

    with pytest.raises(ValidationError, match="compliance_budget is required"):
        ModelDelegationRequest(
            prompt="Write tests.",
            task_type="test",
            correlation_id=CORRELATION_ID,
            emitted_at=datetime(2026, 5, 14, 20, 15, tzinfo=UTC),
            output_schema_key="delegation.result.v1",
        )

    with pytest.raises(ValidationError, match="unsupported acceptance criteria"):
        ModelDelegationRequest(
            prompt="Write tests.",
            task_type="test",
            correlation_id=CORRELATION_ID,
            emitted_at=datetime(2026, 5, 14, 20, 15, tzinfo=UTC),
            acceptance_criteria=("unknown_check",),
        )


def test_delegation_result_event_and_task_event_round_trip() -> None:
    result = _result()
    event = ModelDelegationEventEnvelope(topic="onex.evt.delegation.result.v1", payload=result)
    delegated = ModelTaskDelegatedEvent(
        timestamp="2026-05-14T20:15:00Z",
        correlation_id=CORRELATION_ID,
        session_id=SESSION_ID,
        task_type="test",
        delegated_to="local-qwen",
        model_name="qwen3-coder",
        quality_gate_passed=True,
        prompt_text="Write tests.",
        response_text="Focused test output.",
        pricing_manifest_version=3,
    )

    assert _round_trip(result) == result
    assert _round_trip(event) == event
    assert _round_trip(delegated) == delegated
    assert delegated.topic == "onex.evt.omniclaude.task-delegated.v1"


def test_orchestrator_intents_and_compliance_result_round_trip() -> None:
    request = _request()
    quality_input = ModelQualityGateInput(
        correlation_id=CORRELATION_ID,
        task_type="test",
        llm_response_content="Focused response that is long enough to pass.",
        expected_markers=("pytest",),
        dod_deterministic=("output_parses",),
        acceptance_criteria=("plain_text_only",),
    )

    models = [
        ModelRoutingIntent(payload=request),
        ModelInferenceIntent(
            base_url="http://127.0.0.1:8000",
            model="qwen3-coder",
            system_prompt="Return concise output.",
            prompt=request.prompt,
            max_tokens=1024,
            correlation_id=CORRELATION_ID,
        ),
        ModelQualityGateIntent(payload=quality_input),
        ModelBaselineIntent(
            correlation_id=CORRELATION_ID,
            task_type="test",
            baseline_cost_usd=0.42,
            candidate_cost_usd=0.01,
            prompt_tokens=120,
            completion_tokens=45,
            total_tokens=165,
        ),
        ModelInferenceResponseData(
            correlation_id=CORRELATION_ID,
            content="Focused response.",
            model_used="qwen3-coder",
            llm_call_id="call-123",
            latency_ms=321,
            prompt_tokens=120,
            completion_tokens=45,
            total_tokens=165,
        ),
        ModelComplianceLoopResult(
            compliant=False,
            tokens_to_compliance=165,
            compliance_attempts=1,
            repair_prompt="Return valid JSON.",
            budget_action=EnumBudgetAction.CONTINUE,
        ),
    ]

    for model in models:
        assert _round_trip(model) == model


def test_quality_gate_and_routing_config_round_trip() -> None:
    quality_input = ModelQualityGateInput(
        correlation_id=CORRELATION_ID,
        task_type="document",
        llm_response_content="Documentation response.",
        quality_contract_mode="replace_task_class",
    )
    quality_result = ModelQualityGateResult(
        correlation_id=CORRELATION_ID,
        passed=False,
        fail_category="fail_heuristic",
        quality_score=0.52,
        failure_reasons=("too short",),
        fallback_recommended=True,
    )
    routing_config = ModelDelegationConfig(
        tiers=(
            ModelRoutingTier(
                name="local",
                models=(
                    ModelTierModel(
                        id="qwen3-coder",
                        backend_ref="local-qwen",
                        max_context_tokens=32768,
                        use_for=("test", "document"),
                    ),
                ),
                eval_before_accept=True,
                eval_model="qwen3-eval",
                max_retries=1,
            ),
        )
    )

    assert _round_trip(quality_input) == quality_input
    assert _round_trip(quality_result) == quality_result
    assert _round_trip(routing_config) == routing_config


def test_bifrost_delegation_config_round_trip_and_constraints() -> None:
    config = ModelBifrostDelegationConfig(
        config_version="1.0.0",
        schema_version="bifrost.delegation.v1",
        backends=(
            ModelDelegationBackendConfig(
                backend_id="local-qwen",
                base_url_env="BIFROST_LOCAL_QWEN_URL",
                model_name="qwen3-coder",
                tier="local",
                capabilities=("code", "tests"),
            ),
        ),
        routing_rules=(
            ModelDelegationRoutingRule(
                rule_id=RULE_ID,
                task_class="test",
                task_class_contract_version="1.0.0",
                backend_policy_version="2026-05-14",
                backend_ids=("local-qwen",),
                fallback_policy=ModelDelegationFallbackPolicy(
                    action="escalate_to_next_tier",
                    max_retries=2,
                ),
                shadow_policy_id=SHADOW_POLICY_ID,
            ),
        ),
        default_backends=("local-qwen",),
    )

    assert _round_trip(config) == config

    with pytest.raises(ValidationError):
        ModelBifrostDelegationConfig(
            config_version="1.0.0",
            schema_version="bifrost.delegation.v1",
            backends=(),
            routing_rules=config.routing_rules,
        )


def test_wire_package_excludes_model_routing_decision() -> None:
    assert "ModelRoutingDecision" not in wire.__all__
    assert not hasattr(wire, "ModelRoutingDecision")


def test_acceptance_criteria_helper_returns_validated_tuple() -> None:
    criteria = ("exactly_two_sentences", "max_words_per_sentence_9")

    assert validate_acceptance_criteria(criteria) == criteria
