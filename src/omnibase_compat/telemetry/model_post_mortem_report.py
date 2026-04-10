# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Wire types for session post-mortem reports.

Zero upstream runtime deps — pydantic only.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class EnumPostMortemOutcome(StrEnum):
    """Terminal outcome for an overnight session."""

    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
    ABORTED = "aborted"


class ModelFrictionEvent(BaseModel, frozen=True, extra="forbid"):
    """A single friction event recorded during an overnight session.

    Parsed from files in .onex_state/friction/. Frozen and extra-forbid
    for schema safety.
    """

    event_id: str
    ticket_id: str | None = None
    agent_id: str | None = None
    friction_type: str
    description: str
    recorded_at: datetime
    schema_version: str = "1.0"


class ModelPostMortemReport(BaseModel, frozen=True, extra="forbid"):
    """Session post-mortem report produced by node_session_post_mortem.

    Cross-repo observable artifact: written to docs/post-mortems/ and
    emitted to Kafka. Frozen and extra-forbid for schema safety.
    """

    session_id: str
    session_label: str
    outcome: EnumPostMortemOutcome
    phases_planned: list[str]
    phases_completed: list[str]
    phases_failed: list[str]
    phases_skipped: list[str]
    stalled_agents: list[str]
    friction_events: list[ModelFrictionEvent]
    prs_merged: list[str]
    prs_open: list[str]
    prs_failed: list[str]
    carry_forward_items: list[str]
    report_path: str
    started_at: datetime
    completed_at: datetime
    schema_version: str = "1.0"
