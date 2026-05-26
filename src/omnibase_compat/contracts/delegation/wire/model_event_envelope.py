# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.models.delegation.wire
# COMPAT_REMOVAL_DATE: 2026-06-25

"""Delegation event envelope wire DTO."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from omnibase_compat.contracts.delegation.wire.model_delegation_result import (
    ModelDelegationResult,
)


class ModelDelegationEventEnvelope(BaseModel):
    """Topic plus delegation result payload envelope."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    topic: str
    payload: ModelDelegationResult


__all__: list[str] = ["ModelDelegationEventEnvelope"]
