# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import BaseModel

from omnibase_compat.overseer.enum_capability_tier import EnumCapabilityTier
from omnibase_compat.overseer.enum_context_bundle_level import EnumContextBundleLevel
from omnibase_compat.overseer.enum_failure_class import EnumFailureClass

# --- EnumCapabilityTier ---


@pytest.mark.unit
def test_capability_tier_ordering() -> None:
    assert EnumCapabilityTier.C0 < EnumCapabilityTier.C1
    assert EnumCapabilityTier.C1 < EnumCapabilityTier.C2
    assert EnumCapabilityTier.C2 < EnumCapabilityTier.C3
    assert EnumCapabilityTier.C3 < EnumCapabilityTier.C4
    assert not (EnumCapabilityTier.C4 < EnumCapabilityTier.C0)


@pytest.mark.unit
def test_capability_tier_str_round_trip() -> None:
    assert EnumCapabilityTier("C2") == EnumCapabilityTier.C2
    assert str(EnumCapabilityTier.C2) == "C2"


@pytest.mark.unit
def test_capability_tier_pydantic_serializes_as_string() -> None:
    class _Model(BaseModel):
        tier: EnumCapabilityTier

    m = _Model(tier=EnumCapabilityTier.C2)
    data = m.model_dump()
    assert data["tier"] == "C2"
    assert isinstance(data["tier"], str)


# --- EnumFailureClass ---


@pytest.mark.unit
def test_failure_class_all_values_unique() -> None:
    values = [e.value for e in EnumFailureClass]
    assert len(values) == len(set(values))


@pytest.mark.unit
def test_failure_class_expected_members() -> None:
    expected = {
        "transient",
        "permanent",
        "resource_exhaustion",
        "timeout",
        "dependency",
        "configuration",
        "data_integrity",
        "unknown",
    }
    assert {e.value for e in EnumFailureClass} == expected


# --- EnumContextBundleLevel ---


@pytest.mark.unit
def test_enum_context_bundle_level_values() -> None:
    assert EnumContextBundleLevel.L0 < EnumContextBundleLevel.L1
    assert EnumContextBundleLevel.L1 < EnumContextBundleLevel.L2
    assert EnumContextBundleLevel.L2 < EnumContextBundleLevel.L3
    assert EnumContextBundleLevel.L3 < EnumContextBundleLevel.L4
    assert not (EnumContextBundleLevel.L4 < EnumContextBundleLevel.L0)


@pytest.mark.unit
def test_context_bundle_level_str_round_trip() -> None:
    assert EnumContextBundleLevel("L2") == EnumContextBundleLevel.L2
    assert str(EnumContextBundleLevel.L2) == "L2"
