# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.telemetry — wire types for session-level telemetry reporting.

Exports cross-repo observable artifacts for session post-mortems and
friction event collection. Zero upstream runtime deps.
"""

from omnibase_compat.telemetry.model_post_mortem_report import (
    EnumPostMortemOutcome,
    ModelFrictionEvent,
    ModelPostMortemReport,
)

__all__ = [
    "EnumPostMortemOutcome",
    "ModelFrictionEvent",
    "ModelPostMortemReport",
]
