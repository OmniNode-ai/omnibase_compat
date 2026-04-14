# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Canonical wire type for session bootstrap contract.

Defines the lightweight machine-readable contract for session bootstrapping:
timers, phase expectations, and advisory cost ceilings. This is the canonical
single definition — all consumers must import from here.

Related: OMN-8368 (collapse duplicate ModelSessionContract definitions)
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


# COMPAT_MIGRATION_TARGET: omnimarket.nodes.session_bootstrap.contract (OMN-8368)
# COMPAT_REMOVAL_DATE: 2026-10-01
class ModelSessionContract(BaseModel, frozen=True, extra="forbid"):
    """Session-level verification contract for autonomous sessions.

    Read by node_session_bootstrap at session start to configure timers,
    phase expectations, and advisory cost ceilings. Frozen and extra-forbid
    for schema safety.
    """

    session_id: str
    session_label: str
    phases_expected: list[str]
    max_cycles: int = 0
    cost_ceiling_usd: float = Field(default=10.0, ge=0.0)
    halt_on_build_loop_failure: bool = True
    dry_run: bool = False
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    schema_version: str = "1.0"


__all__: list[str] = ["ModelSessionContract"]
