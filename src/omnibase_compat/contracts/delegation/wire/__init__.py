# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Canonical delegation wire DTOs.

These models are pure Pydantic schemas for shared delegation payloads. They do
not include routing decision models; OMN-8596 owns that path.
"""

from omnibase_compat.contracts.delegation.wire.model_bifrost_delegation_config import (
    ModelBifrostDelegationConfig,
    ModelDelegationBackendConfig,
    ModelDelegationCircuitBreakerConfig,
    ModelDelegationFailoverConfig,
    ModelDelegationFallbackPolicy,
    ModelDelegationRoutingRule,
    ModelDelegationShadowConfig,
)
from omnibase_compat.contracts.delegation.wire.model_budget import (
    EnumBudgetAction,
    ModelBudgetLimits,
)
from omnibase_compat.contracts.delegation.wire.model_delegation_request import (
    EnumQualityContractMode,
    ModelDelegationRequest,
    validate_acceptance_criteria,
)
from omnibase_compat.contracts.delegation.wire.model_delegation_result import (
    ModelDelegationResult,
)
from omnibase_compat.contracts.delegation.wire.model_event_envelope import (
    ModelDelegationEventEnvelope,
)
from omnibase_compat.contracts.delegation.wire.model_orchestrator_intents import (
    ModelBaselineIntent,
    ModelComplianceLoopResult,
    ModelInferenceIntent,
    ModelInferenceResponseData,
    ModelQualityGateIntent,
    ModelRoutingIntent,
)
from omnibase_compat.contracts.delegation.wire.model_quality_gate import (
    EnumQualityGateCategory,
    ModelQualityGateInput,
    ModelQualityGateResult,
)
from omnibase_compat.contracts.delegation.wire.model_routing_config import (
    ModelDelegationConfig,
    ModelRoutingTier,
    ModelTierModel,
)
from omnibase_compat.contracts.delegation.wire.model_task_delegated_event import (
    TASK_DELEGATED_TOPIC_V1,
    ModelTaskDelegatedEvent,
)

__all__: list[str] = [
    "EnumBudgetAction",
    "EnumQualityContractMode",
    "EnumQualityGateCategory",
    "ModelBaselineIntent",
    "ModelBifrostDelegationConfig",
    "ModelBudgetLimits",
    "ModelComplianceLoopResult",
    "ModelDelegationBackendConfig",
    "ModelDelegationCircuitBreakerConfig",
    "ModelDelegationConfig",
    "ModelDelegationEventEnvelope",
    "ModelDelegationFailoverConfig",
    "ModelDelegationFallbackPolicy",
    "ModelDelegationRequest",
    "ModelDelegationResult",
    "ModelDelegationRoutingRule",
    "ModelDelegationShadowConfig",
    "ModelInferenceIntent",
    "ModelInferenceResponseData",
    "ModelQualityGateInput",
    "ModelQualityGateIntent",
    "ModelQualityGateResult",
    "ModelRoutingIntent",
    "ModelRoutingTier",
    "ModelTaskDelegatedEvent",
    "ModelTierModel",
    "TASK_DELEGATED_TOPIC_V1",
    "validate_acceptance_criteria",
]
