# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.overseer — wire types for the global overseer domain.

Exports all enums, models, and type aliases shared between the global
overseer, domain runners, and routing engine.
Zero upstream runtime deps.
"""

from omnibase_compat.overseer.enum_capability_tier import EnumCapabilityTier
from omnibase_compat.overseer.enum_context_bundle_level import EnumContextBundleLevel
from omnibase_compat.overseer.enum_failure_class import EnumFailureClass
from omnibase_compat.overseer.enum_verifier_verdict import EnumVerifierVerdict
from omnibase_compat.overseer.model_completion_report import (
    EnumCompletionOutcome,
    ModelCompletionReport,
)
from omnibase_compat.overseer.model_context_bundle import (
    ModelContextBundleL0,
    ModelContextBundleL1,
    ModelContextBundleL2,
    ModelContextBundleL3,
    ModelContextBundleL4,
)
from omnibase_compat.overseer.model_escalation_request import ModelEscalationRequest
from omnibase_compat.overseer.model_task_delta_envelope import ModelTaskDeltaEnvelope
from omnibase_compat.overseer.model_task_state_envelope import (
    EnumTaskStatus,
    ModelTaskStateEnvelope,
)
from omnibase_compat.overseer.model_verifier_output import (
    ModelVerifierCheckResult,
    ModelVerifierOutput,
)

__all__ = [
    "EnumCapabilityTier",
    "EnumCompletionOutcome",
    "EnumContextBundleLevel",
    "EnumFailureClass",
    "EnumTaskStatus",
    "EnumVerifierVerdict",
    "ModelCompletionReport",
    "ModelContextBundleL0",
    "ModelContextBundleL1",
    "ModelContextBundleL2",
    "ModelContextBundleL3",
    "ModelContextBundleL4",
    "ModelEscalationRequest",
    "ModelTaskDeltaEnvelope",
    "ModelTaskStateEnvelope",
    "ModelVerifierCheckResult",
    "ModelVerifierOutput",
]
