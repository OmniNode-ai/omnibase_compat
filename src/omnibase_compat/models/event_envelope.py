# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.models.event_envelope
# COMPAT_REMOVAL_DATE: 2026-07-01

import uuid
from typing import Any

from pydantic import BaseModel, Field


class EventEnvelopeV1Minimal(BaseModel, frozen=True):
    """Minimal shared transport envelope for cross-repo event compatibility.

    Intentionally narrow. Does not include timestamp, source, trace_id,
    correlation_id, or category. Add those in a versioned successor or
    additive minor release once real usage patterns are established.
    """

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    schema_version: str = "1.0"
