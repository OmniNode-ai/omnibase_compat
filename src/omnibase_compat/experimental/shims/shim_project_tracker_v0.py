# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# sunset: omnibase_core >= 0.12.0 (2026-07-01)
"""Forward-compat shim for project-tracker issue shape.

This shim bridges callers that need a typed `assignee_id` on a project-tracker
issue before `ModelProjectTrackerIssueV0` lands in omnibase_core.

Delete this file and its adapter once omnibase_core >= 0.12.0 ships.
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ShimProjectTrackerIssueV0(BaseModel):
    """Canary shim shape for a project-tracker issue.

    Mirrors the expected omnibase_core shape so callers can import from here
    today and do a one-line re-point once the real model is promoted.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    issue_id: UUID
    title: str
    assignee_id: UUID | None = Field(default=None)
    status: str = "backlog"


@runtime_checkable
class ProtocolProjectTrackerIssueReader(Protocol):
    """Minimal read protocol for a project-tracker issue."""

    def get_issue(self, issue_id: UUID) -> ShimProjectTrackerIssueV0: ...


class ShimProjectTrackerIssueAdapterV0:
    """Trivial adapter that wraps a raw dict into ShimProjectTrackerIssueV0.

    Replace the body with a real omnibase_core adapter once the model lands.
    """

    def get_issue(self, raw: dict[str, object]) -> ShimProjectTrackerIssueV0:
        return ShimProjectTrackerIssueV0.model_validate(raw)
