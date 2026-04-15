# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for ShimProjectTrackerIssueV0 and its adapter."""

import uuid

import pytest
from pydantic import ValidationError

from omnibase_compat.experimental.shims.shim_project_tracker_v0 import (
    ShimProjectTrackerIssueAdapterV0,
    ShimProjectTrackerIssueV0,
)


def test_shim_loads_minimal() -> None:
    issue = ShimProjectTrackerIssueV0(issue_id=uuid.uuid4(), title="Do the thing")
    assert issue.status == "backlog"
    assert issue.assignee_id is None


def test_shim_loads_with_assignee() -> None:
    aid = uuid.uuid4()
    issue = ShimProjectTrackerIssueV0(
        issue_id=uuid.uuid4(),
        title="Assigned task",
        assignee_id=aid,
        status="in_progress",
    )
    assert issue.assignee_id == aid


def test_shim_is_frozen() -> None:
    issue = ShimProjectTrackerIssueV0(issue_id=uuid.uuid4(), title="Frozen")
    with pytest.raises((TypeError, ValidationError)):
        issue.title = "mutated"  # type: ignore[misc]


def test_shim_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        ShimProjectTrackerIssueV0(
            issue_id=uuid.uuid4(),
            title="Extra",
            unknown_field="boom",  # type: ignore[call-arg]
        )


def test_adapter_wraps_raw_dict() -> None:
    raw: dict[str, object] = {
        "issue_id": str(uuid.uuid4()),
        "title": "Via adapter",
        "assignee_id": None,
        "status": "backlog",
    }
    adapter = ShimProjectTrackerIssueAdapterV0()
    issue = adapter.get_issue(raw)
    assert issue.title == "Via adapter"
