# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: delegation wire DTO — permanent zero-upstream-dep schema layer (OMN-10919)

"""Pricing manifest reference model for delegation runtime configuration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ModelDelegationPricingManifestRef(BaseModel):
    """Reference to a pricing manifest with version pinning."""

    model_config = ConfigDict(frozen=True, extra="forbid", from_attributes=True)

    manifest_ref: str = Field(..., description="Reference to the pricing manifest resource")
    version: int = Field(..., ge=1, description="Manifest version; must be >= 1")
