# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.model_contract_allowed_actions import (
    ModelContractAllowedActions,
)


@pytest.mark.unit
def test_is_action_permitted_happy_path() -> None:
    """Permitted action in allowed_actions and not in denied_actions returns True."""
    perms = ModelContractAllowedActions(
        role="executor",
        allowed_actions=frozenset({"run_task", "read_contract"}),
        denied_actions=frozenset(),
    )
    assert perms.is_action_permitted("run_task") is True
    assert perms.is_action_permitted("read_contract") is True


@pytest.mark.unit
def test_denied_takes_precedence_over_allowed() -> None:
    """Action in both allowed_actions and denied_actions is denied."""
    perms = ModelContractAllowedActions(
        role="executor",
        allowed_actions=frozenset({"run_task", "read_contract"}),
        denied_actions=frozenset({"run_task"}),
    )
    assert perms.is_action_permitted("run_task") is False
    # Other allowed action still works
    assert perms.is_action_permitted("read_contract") is True


@pytest.mark.unit
def test_empty_allowed_means_no_access() -> None:
    """Empty allowed_actions denies all actions regardless of denied_actions."""
    perms = ModelContractAllowedActions(
        role="observer",
        allowed_actions=frozenset(),
        denied_actions=frozenset(),
    )
    assert perms.is_action_permitted("run_task") is False
    assert perms.is_action_permitted("read_contract") is False
    assert perms.is_action_permitted("any_action") is False


@pytest.mark.unit
def test_action_not_in_allowed_is_denied() -> None:
    """Action absent from allowed_actions is denied even with no denied entries."""
    perms = ModelContractAllowedActions(
        role="reader",
        allowed_actions=frozenset({"read_contract"}),
        denied_actions=frozenset(),
    )
    assert perms.is_action_permitted("run_task") is False


@pytest.mark.unit
def test_model_is_frozen() -> None:
    """ModelContractAllowedActions is immutable."""
    perms = ModelContractAllowedActions(
        role="reader",
        allowed_actions=frozenset({"read_contract"}),
    )
    with pytest.raises((ValidationError, TypeError)):
        perms.role = "executor"  # type: ignore[misc]


@pytest.mark.unit
def test_model_forbids_extra_fields() -> None:
    """Extra fields raise ValidationError."""
    with pytest.raises(ValidationError):
        ModelContractAllowedActions(
            role="reader",
            allowed_actions=frozenset({"read_contract"}),
            unknown_field="bad",  # type: ignore[call-arg]
        )


@pytest.mark.unit
def test_roundtrip_serialization() -> None:
    """model_dump / model_validate round-trip preserves all fields."""
    perms = ModelContractAllowedActions(
        role="executor",
        allowed_actions=frozenset({"run_task", "read_contract"}),
        denied_actions=frozenset({"admin_action"}),
    )
    data = perms.model_dump(mode="json")
    restored = ModelContractAllowedActions.model_validate(data)
    assert restored.role == perms.role
    assert restored.allowed_actions == perms.allowed_actions
    assert restored.denied_actions == perms.denied_actions
