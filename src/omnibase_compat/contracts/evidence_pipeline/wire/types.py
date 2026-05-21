# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Shared literal types for evidence pipeline DTOs."""

from __future__ import annotations

from typing import Literal

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type EvidenceLifecycleState = Literal[
    "PROVISIONAL",
    "VALIDATED",
    "FINALIZED",
    "SUPERSEDED",
    "REJECTED",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type GapClassification = Literal[
    "MISSING",
    "STALE",
    "SUPERSEDED",
    "HASH_MISMATCH",
    "RECEIPT_MISSING",
    "VALIDATION_FAILED",
    "UNKNOWN",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type ReadinessState = Literal[
    "READY",
    "BLOCKED",
    "DEGRADED",
    "ADVISORY_ONLY",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type TriggerSurface = Literal[
    "pull_request_merge",
    "merge_group",
    "deploy",
    "manual",
    "runtime_event",
]

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire.types
# COMPAT_REMOVAL_DATE: 2027-06-01
type ValidationState = Literal[
    "PASSED",
    "FAILED",
    "ADVISORY_ONLY",
]

__all__: list[str] = [
    "EvidenceLifecycleState",
    "GapClassification",
    "ReadinessState",
    "TriggerSurface",
    "ValidationState",
]
