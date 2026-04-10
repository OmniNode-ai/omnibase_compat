# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.enum_capability_tier import EnumCapabilityTier
from omnibase_compat.overseer.enum_provider import EnumProvider
from omnibase_compat.overseer.enum_retry_type import EnumRetryType
from omnibase_compat.overseer.enum_risk_level import EnumRiskLevel
from omnibase_compat.overseer.model_task_shape_features import ModelTaskShapeFeatures


@pytest.mark.unit
def test_task_shape_features_roundtrip() -> None:
    """Full field round-trip through model_dump / model_validate."""
    features = ModelTaskShapeFeatures(
        domain="code",
        capability_tier=EnumCapabilityTier.C3,
        risk_level=EnumRiskLevel.HIGH,
        retry_type=EnumRetryType.BACKOFF,
        preferred_provider=EnumProvider.ANTHROPIC,
        novelty_score=0.75,
        estimated_tokens=4096,
        requires_tool_use=True,
    )
    serialized = features.model_dump(mode="json")
    restored = ModelTaskShapeFeatures.model_validate(serialized)
    assert restored.domain == "code"
    assert restored.capability_tier == EnumCapabilityTier.C3
    assert restored.risk_level == EnumRiskLevel.HIGH
    assert restored.retry_type == EnumRetryType.BACKOFF
    assert restored.preferred_provider == EnumProvider.ANTHROPIC
    assert restored.novelty_score == 0.75
    assert restored.estimated_tokens == 4096
    assert restored.requires_tool_use is True


@pytest.mark.unit
def test_task_shape_features_defaults() -> None:
    """Minimal construction uses sensible defaults."""
    features = ModelTaskShapeFeatures(domain="reasoning")
    assert features.capability_tier == EnumCapabilityTier.C2
    assert features.risk_level == EnumRiskLevel.LOW
    assert features.retry_type == EnumRetryType.NONE
    assert features.preferred_provider == EnumProvider.UNKNOWN
    assert features.novelty_score == 0.0
    assert features.estimated_tokens == 0
    assert features.requires_tool_use is False


@pytest.mark.unit
def test_novelty_score_bounded() -> None:
    """novelty_score > 1.0 must raise ValidationError."""
    with pytest.raises(ValidationError):
        ModelTaskShapeFeatures(domain="code", novelty_score=1.1)


@pytest.mark.unit
def test_novelty_score_negative_bounded() -> None:
    """novelty_score < 0.0 must raise ValidationError."""
    with pytest.raises(ValidationError):
        ModelTaskShapeFeatures(domain="code", novelty_score=-0.1)


@pytest.mark.unit
def test_task_shape_features_frozen() -> None:
    """ModelTaskShapeFeatures is immutable."""
    features = ModelTaskShapeFeatures(domain="code")
    with pytest.raises((ValidationError, TypeError)):
        features.domain = "mutated"  # type: ignore[misc]


@pytest.mark.unit
def test_task_shape_features_forbids_extra() -> None:
    """Extra fields are rejected."""
    with pytest.raises(ValidationError):
        ModelTaskShapeFeatures(domain="code", unknown_field="bad")  # type: ignore[call-arg]


@pytest.mark.unit
def test_retry_type_all_values_unique() -> None:
    """EnumRetryType has no duplicate values."""
    values = [m.value for m in EnumRetryType]
    assert len(values) == len(set(values))


@pytest.mark.unit
def test_risk_level_all_values_unique() -> None:
    """EnumRiskLevel has no duplicate values."""
    values = [m.value for m in EnumRiskLevel]
    assert len(values) == len(set(values))


@pytest.mark.unit
def test_provider_all_values_unique() -> None:
    """EnumProvider has no duplicate values."""
    values = [m.value for m in EnumProvider]
    assert len(values) == len(set(values))


@pytest.mark.unit
def test_retry_type_members() -> None:
    """EnumRetryType contains expected members."""
    assert EnumRetryType.NONE == "none"
    assert EnumRetryType.IMMEDIATE == "immediate"
    assert EnumRetryType.BACKOFF == "backoff"
    assert EnumRetryType.ESCALATE == "escalate"


@pytest.mark.unit
def test_risk_level_members() -> None:
    """EnumRiskLevel contains expected members."""
    assert EnumRiskLevel.LOW == "low"
    assert EnumRiskLevel.MEDIUM == "medium"
    assert EnumRiskLevel.HIGH == "high"
    assert EnumRiskLevel.CRITICAL == "critical"


@pytest.mark.unit
def test_provider_members() -> None:
    """EnumProvider contains expected members."""
    assert EnumProvider.ANTHROPIC == "anthropic"
    assert EnumProvider.OPENAI == "openai"
    assert EnumProvider.GOOGLE == "google"
    assert EnumProvider.LOCAL == "local"
    assert EnumProvider.UNKNOWN == "unknown"
