# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.overseer — overseer domain enums and wire types.

Shared between the global overseer, domain runners, and routing engine.
Zero upstream runtime deps.
"""

from omnibase_compat.overseer.enum_capability_tier import EnumCapabilityTier
from omnibase_compat.overseer.enum_context_bundle_level import EnumContextBundleLevel
from omnibase_compat.overseer.enum_failure_class import EnumFailureClass
from omnibase_compat.overseer.model_completion_report import (
    EnumCompletionOutcome,
    ModelCompletionReport,
)
from omnibase_compat.overseer.model_escalation_request import ModelEscalationRequest

__all__ = [
    "EnumCapabilityTier",
    "EnumCompletionOutcome",
    "EnumContextBundleLevel",
    "EnumFailureClass",
    "ModelCompletionReport",
    "ModelEscalationRequest",
]
