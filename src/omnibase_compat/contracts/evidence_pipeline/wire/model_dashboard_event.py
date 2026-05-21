# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# COMPAT_MIGRATION_TARGET: omnibase_core.contracts.evidence_pipeline.wire
# COMPAT_REMOVAL_DATE: 2027-06-01

"""ModelDashboardEvent — normalized projection-write dashboard event."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from omnibase_compat.contracts.evidence_pipeline.wire.types import (
    DashboardStage,
    EvidenceLifecycleState,
)


class ModelDashboardEvent(BaseModel):
    """Normalized event persisted into reducer-owned dashboard projections."""

    model_config = ConfigDict(frozen=True, extra="forbid", from_attributes=True)

    schema_version: Literal["1.0.0"] = "1.0.0"
    event_id: str = Field(..., min_length=1)
    causation_id: str | None = Field(default=None, min_length=1)
    source_event_hash: str = Field(..., min_length=1)
    projection_cursor: str = Field(..., min_length=1)
    ingest_sequence: int = Field(..., ge=0)
    correlation_id: str = Field(..., min_length=1)
    ticket_id: str | None = Field(default=None, min_length=1)
    topic: str = Field(..., min_length=1)
    stage: DashboardStage
    timestamp: str = Field(..., min_length=1)
    payload_summary: Mapping[str, str] = Field(default_factory=dict)
    evidence_lifecycle_state: EvidenceLifecycleState


__all__: list[str] = ["ModelDashboardEvent"]
