# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Tests for omnibase_compat.overseer exports.

After OMN-7326 removed dead shims (including ModelSessionContract),
the overseer module exports only ModelRoutingDecision.
"""

from __future__ import annotations

import importlib


def test_overseer_module_importable() -> None:
    """omnibase_compat.overseer must be importable."""
    spec = importlib.util.find_spec("omnibase_compat.overseer")
    assert spec is not None, "omnibase_compat.overseer module not found"


def test_overseer_exports_exactly_routing_decision() -> None:
    """__all__ must contain exactly ModelRoutingDecision."""
    from omnibase_compat import overseer

    assert set(overseer.__all__) == {"ModelRoutingDecision"}, (
        f"Expected overseer.__all__ to be {{'ModelRoutingDecision'}}, got: {set(overseer.__all__)}"
    )


def test_model_routing_decision_still_exported() -> None:
    """ModelRoutingDecision must still be exported (regression guard for OMN-8038)."""
    from omnibase_compat.overseer import ModelRoutingDecision

    assert ModelRoutingDecision is not None
