# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for all six protocol domain action enums."""

import pytest

from omnibase_compat.overseer.enum_artifact_store_action import EnumArtifactStoreAction
from omnibase_compat.overseer.enum_code_repository_action import EnumCodeRepositoryAction
from omnibase_compat.overseer.enum_event_bus_action import EnumEventBusAction
from omnibase_compat.overseer.enum_llm_provider_action import EnumLLMProviderAction
from omnibase_compat.overseer.enum_notification_action import EnumNotificationAction
from omnibase_compat.overseer.enum_ticket_service_action import EnumTicketServiceAction

ALL_ENUM_CLASSES = [
    EnumCodeRepositoryAction,
    EnumTicketServiceAction,
    EnumEventBusAction,
    EnumLLMProviderAction,
    EnumArtifactStoreAction,
    EnumNotificationAction,
]


@pytest.mark.parametrize("enum_cls", ALL_ENUM_CLASSES)
def test_values_are_unique(enum_cls):
    """Each enum must have unique string values — no two members share a value."""
    values = [m.value for m in enum_cls]
    assert len(values) == len(set(values)), f"{enum_cls.__name__} has duplicate values"


@pytest.mark.parametrize("enum_cls", ALL_ENUM_CLASSES)
def test_round_trip(enum_cls):
    """Every member must be recoverable from its string value."""
    for member in enum_cls:
        assert enum_cls(member.value) is member


@pytest.mark.parametrize("enum_cls", ALL_ENUM_CLASSES)
def test_is_str(enum_cls):
    """Every member must compare equal to its string value (StrEnum contract)."""
    for member in enum_cls:
        assert member == member.value
        assert isinstance(member, str)


@pytest.mark.parametrize("enum_cls", ALL_ENUM_CLASSES)
def test_at_least_one_member(enum_cls):
    """Every enum must define at least one member."""
    assert len(list(enum_cls)) >= 1


# --- per-enum spot-checks ---


def test_code_repository_action_has_expected_members():
    assert EnumCodeRepositoryAction.CLONE == "CLONE"
    assert EnumCodeRepositoryAction.CREATE_PULL_REQUEST == "CREATE_PULL_REQUEST"
    assert EnumCodeRepositoryAction.MERGE_PULL_REQUEST == "MERGE_PULL_REQUEST"


def test_ticket_service_action_has_expected_members():
    assert EnumTicketServiceAction.CREATE_ISSUE == "CREATE_ISSUE"
    assert EnumTicketServiceAction.TRANSITION_STATUS == "TRANSITION_STATUS"
    assert EnumTicketServiceAction.ADD_COMMENT == "ADD_COMMENT"


def test_event_bus_action_has_expected_members():
    assert EnumEventBusAction.PUBLISH == "PUBLISH"
    assert EnumEventBusAction.SUBSCRIBE == "SUBSCRIBE"
    assert EnumEventBusAction.DRAIN == "DRAIN"


def test_llm_provider_action_has_expected_members():
    assert EnumLLMProviderAction.COMPLETE == "COMPLETE"
    assert EnumLLMProviderAction.EMBED == "EMBED"
    assert EnumLLMProviderAction.STREAM == "STREAM"


def test_artifact_store_action_has_expected_members():
    assert EnumArtifactStoreAction.UPLOAD == "UPLOAD"
    assert EnumArtifactStoreAction.DOWNLOAD == "DOWNLOAD"
    assert EnumArtifactStoreAction.EXISTS == "EXISTS"


def test_notification_action_has_expected_members():
    assert EnumNotificationAction.SEND == "SEND"
    assert EnumNotificationAction.SEND_ALERT == "SEND_ALERT"
    assert EnumNotificationAction.RESOLVE == "RESOLVE"
