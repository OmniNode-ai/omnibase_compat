# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for omnibase_compat.overseer package exports (OMN-8033)."""

from enum import StrEnum

import pytest

from omnibase_compat.overseer import (
    EnumArtifactStoreAction,
    EnumCapabilityTier,
    EnumCodeRepositoryAction,
    EnumCompletionOutcome,
    EnumContextBundleLevel,
    EnumEventBusAction,
    EnumFailureClass,
    EnumLLMProviderAction,
    EnumNotificationAction,
    EnumProcessRunnerState,
    EnumTaskStatus,
    EnumTicketServiceAction,
    EnumVerifierVerdict,
    ModelCompletionReport,
    ModelContractAllowedActions,
    ModelContextBundleL0,
    ModelContextBundleL1,
    ModelContextBundleL2,
    ModelContextBundleL3,
    ModelContextBundleL4,
    ModelEscalationRequest,
    ModelProcessRunnerStateTransition,
    ModelSessionContract,
    ModelSessionHaltCondition,
    ModelSessionPhaseSpec,
    ModelTaskDeltaEnvelope,
    ModelTaskStateEnvelope,
    ModelVerifierCheckResult,
    ModelVerifierOutput,
)


@pytest.mark.unit
def test_all_overseer_types_importable() -> None:
    """All 29 overseer types are importable from omnibase_compat.overseer."""
    types = [
        EnumArtifactStoreAction,
        EnumCapabilityTier,
        EnumCodeRepositoryAction,
        EnumCompletionOutcome,
        EnumContextBundleLevel,
        EnumEventBusAction,
        EnumFailureClass,
        EnumLLMProviderAction,
        EnumNotificationAction,
        EnumProcessRunnerState,
        EnumTaskStatus,
        EnumTicketServiceAction,
        EnumVerifierVerdict,
        ModelCompletionReport,
        ModelContractAllowedActions,
        ModelContextBundleL0,
        ModelContextBundleL1,
        ModelContextBundleL2,
        ModelContextBundleL3,
        ModelContextBundleL4,
        ModelEscalationRequest,
        ModelProcessRunnerStateTransition,
        ModelSessionContract,
        ModelSessionHaltCondition,
        ModelSessionPhaseSpec,
        ModelTaskDeltaEnvelope,
        ModelTaskStateEnvelope,
        ModelVerifierCheckResult,
        ModelVerifierOutput,
    ]
    assert len(types) == 29


@pytest.mark.unit
def test_enum_task_status_is_str_enum() -> None:
    assert issubclass(EnumTaskStatus, StrEnum)
    assert EnumTaskStatus.PENDING == "pending"  # type: ignore[comparison-overlap]
    assert EnumTaskStatus.COMPLETED == "completed"  # type: ignore[comparison-overlap]
    assert EnumTaskStatus.FAILED == "failed"  # type: ignore[comparison-overlap]


@pytest.mark.unit
def test_enum_context_bundle_level_is_str_enum() -> None:
    assert issubclass(EnumContextBundleLevel, StrEnum)
    assert EnumContextBundleLevel.L0 == "L0"
    assert EnumContextBundleLevel.L4 == "L4"


@pytest.mark.unit
def test_enum_capability_tier_is_str_enum() -> None:
    assert issubclass(EnumCapabilityTier, StrEnum)
    assert EnumCapabilityTier.C0 == "C0"
    assert EnumCapabilityTier.C4 == "C4"


@pytest.mark.unit
def test_all_exports_in_dunder_all() -> None:
    """__all__ covers every exported name."""
    import omnibase_compat.overseer as overseer_mod

    exported_names = {
        "EnumArtifactStoreAction",
        "EnumCapabilityTier",
        "EnumCodeRepositoryAction",
        "EnumCompletionOutcome",
        "EnumContextBundleLevel",
        "EnumEventBusAction",
        "EnumFailureClass",
        "EnumLLMProviderAction",
        "EnumNotificationAction",
        "EnumProcessRunnerState",
        "EnumTaskStatus",
        "EnumTicketServiceAction",
        "EnumVerifierVerdict",
        "ModelCompletionReport",
        "ModelContractAllowedActions",
        "ModelContextBundleL0",
        "ModelContextBundleL1",
        "ModelContextBundleL2",
        "ModelContextBundleL3",
        "ModelContextBundleL4",
        "ModelEscalationRequest",
        "ModelProcessRunnerStateTransition",
        "ModelSessionContract",
        "ModelSessionHaltCondition",
        "ModelSessionPhaseSpec",
        "ModelTaskDeltaEnvelope",
        "ModelTaskStateEnvelope",
        "ModelVerifierCheckResult",
        "ModelVerifierOutput",
    }
    assert set(overseer_mod.__all__) == exported_names
