# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Wire type for the result produced by node_session_bootstrap.

Zero upstream runtime deps — pydantic only.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class EnumBootstrapStatus(StrEnum):
    """Terminal status for a session bootstrap run."""

    READY = "ready"
    DEGRADED = "degraded"
    FAILED = "failed"


class ModelSessionBootstrapResult(BaseModel, frozen=True, extra="forbid"):
    """Result emitted by node_session_bootstrap after a bootstrap run.

    Written as a wire type in omnibase_compat.telemetry so downstream
    consumers (overnight skill, overseer verifier) can import it without
    pulling in omnimarket as a runtime dependency.
    Frozen and extra-forbid for schema safety.
    """

    session_id: str
    status: EnumBootstrapStatus
    contract_path: str
    timer_configs: list[str]
    warnings: list[str]
    dry_run: bool
    bootstrapped_at: datetime
    schema_version: str = "1.0"
