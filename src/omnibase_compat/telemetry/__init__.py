# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.telemetry — wire types for session-level observability.

Exports all enums and models used for session bootstrap results and
post-mortem reports. These are cross-repo observable artifacts emitted
to Kafka and written to disk.
Zero upstream runtime deps.
"""

from omnibase_compat.telemetry.model_post_mortem_report import (
    EnumPostMortemOutcome,
    ModelFrictionEvent,
    ModelPostMortemReport,
)
from omnibase_compat.telemetry.model_session_bootstrap_result import (
    EnumBootstrapStatus,
    ModelSessionBootstrapResult,
)

__all__ = [
    "EnumBootstrapStatus",
    "EnumPostMortemOutcome",
    "ModelFrictionEvent",
    "ModelPostMortemReport",
    "ModelSessionBootstrapResult",
]
