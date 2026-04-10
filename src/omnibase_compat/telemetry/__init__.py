# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.telemetry — wire types for observability and telemetry.

Exports structured result types for sweep skill runs and other
observability artifacts. Zero upstream runtime deps.
"""

from omnibase_compat.telemetry.model_sweep_result import ModelSweepResult

__all__ = [
    "ModelSweepResult",
]
