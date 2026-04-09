# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from omnibase_compat.overseer.model_task_state_envelope import EnumTaskStatus


class ModelTaskDeltaEnvelope(BaseModel, frozen=True, extra="forbid"):
    """Incremental task state change for overseer projection.

    Carries only the fields that changed, plus the mandatory task_id.
    Wire type shared between the global overseer, domain runners,
    and routing engine. Frozen and extra-forbid for schema safety.
    """

    task_id: str
    status: EnumTaskStatus | None = None
    runner_id: str | None = None
    attempt: int | None = Field(default=None, ge=1)
    payload: dict[str, Any] | None = None
    error: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    schema_version: str = "1.0"
