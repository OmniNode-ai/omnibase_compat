# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Wire type for overnight session contract.

Defines the machine-readable contract for an overnight pipeline session,
including expected phases, cost ceiling, halt conditions, and evidence
requirements. Replaces the markdown-only standing orders pattern.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ModelOvernightPhaseSpec(BaseModel):
    """Specification for a single overnight phase."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    phase_name: str
    required: bool = True
    timeout_seconds: int = 3600  # 1 hour default
    halt_on_failure: bool = False
    success_criteria: list[str] = Field(default_factory=list)


class ModelOvernightHaltCondition(BaseModel):
    """Condition that triggers an immediate halt of the overnight session."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    condition_id: str
    description: str
    check_type: Literal["cost_ceiling", "phase_failure_count", "time_elapsed", "custom"]
    threshold: float  # USD for cost_ceiling, count for failures, seconds for time


class ModelOvernightContract(BaseModel):
    """Machine-readable contract for an overnight pipeline session.

    This is the session-level analogue of ModelTicketContract (per-ticket).
    It declares the expected phases, success criteria, cost constraints,
    and halt conditions for an autonomous overnight run.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = "1.0.0"
    session_id: str  # correlation ID for the overnight session
    created_at: datetime
    max_cost_usd: float = 5.0
    max_duration_seconds: int = 28800  # 8 hours
    dry_run: bool = False

    # Expected phases in order.
    # No default — phases must be supplied explicitly (from session contract YAML or template).
    # Operational defaults live in overnight_contract.template.yaml, not baked into the wire type.
    phases: tuple[ModelOvernightPhaseSpec, ...] = Field(default_factory=tuple)

    # Halt conditions
    halt_conditions: tuple[ModelOvernightHaltCondition, ...] = Field(
        default_factory=lambda: (
            ModelOvernightHaltCondition(
                condition_id="cost_ceiling",
                description="Stop if accumulated cost exceeds ceiling",
                check_type="cost_ceiling",
                threshold=5.0,
            ),
            ModelOvernightHaltCondition(
                condition_id="phase_failure_limit",
                description="Stop after 3 consecutive phase failures",
                check_type="phase_failure_count",
                threshold=3.0,
            ),
        )
    )

    # Standing orders (replaces nightly-loop-decisions.md)
    standing_orders: tuple[str, ...] = Field(default_factory=tuple)

    # Evidence requirements (parallel to ModelTicketContract.dod_evidence)
    required_outcomes: tuple[str, ...] = Field(
        default_factory=lambda: (
            "merge_sweep_completed",
            "platform_readiness_gate_passed",
        )
    )


__all__ = [
    "ModelOvernightContract",
    "ModelOvernightHaltCondition",
    "ModelOvernightPhaseSpec",
]
