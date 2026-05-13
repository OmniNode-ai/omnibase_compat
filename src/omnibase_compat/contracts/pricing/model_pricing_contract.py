# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# COMPAT_MIGRATION_TARGET: onex_change_control.models.pricing.model_pricing_contract
# COMPAT_REMOVAL_DATE: 2026-12-01

"""ModelPricingContract — versioned pricing contract wire DTO."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from omnibase_compat.contracts.pricing.model_model_pricing import ModelModelPricing


class ModelPricingContract(BaseModel):
    """Versioned contract declaring per-model costs and savings methodology.

    Frozen so contract declarations are immutable after parse. Each projection
    row records the pricing contract version to enable auditable savings replay.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(..., min_length=1)
    version: int = Field(..., ge=1)
    baseline_model: str = Field(..., min_length=1)
    savings_method: str = Field(..., min_length=1)
    models: dict[str, ModelModelPricing] = Field(default_factory=dict)


__all__: list[str] = ["ModelPricingContract"]
