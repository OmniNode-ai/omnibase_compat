# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""TDD test for OMN-8368: omnibase_compat.overseer exports exactly the right models.

After OMN-8431 removed the old overseer models and OMN-8038 re-introduced
ModelRoutingDecision, OMN-8368 adds the canonical ModelSessionContract.
The overseer module must export exactly these two names — no more, no less.
"""

from __future__ import annotations

import importlib

import pytest


def test_overseer_module_importable() -> None:
    """omnibase_compat.overseer must be importable after OMN-8368."""
    spec = importlib.util.find_spec("omnibase_compat.overseer")
    assert spec is not None, (
        "omnibase_compat.overseer module not found — "
        "ensure the overseer package is present (OMN-8368)"
    )


def test_overseer_exports_exactly_one_contract_model() -> None:
    """__all__ must contain exactly one contract model: ModelSessionContract.

    DoD requirement from OMN-8368: the canonical contract type is
    ModelSessionContract only — ModelOvernightContract must not be exported
    from omnibase_compat.overseer.
    """
    from omnibase_compat import overseer

    assert set(overseer.__all__) == {"ModelRoutingDecision", "ModelSessionContract"}, (
        "Expected overseer.__all__ to contain exactly "
        "{'ModelRoutingDecision', 'ModelSessionContract'}, "
        f"got: {set(overseer.__all__)}"
    )


def test_model_session_contract_importable() -> None:
    """ModelSessionContract must be importable from omnibase_compat.overseer."""
    from omnibase_compat.overseer import ModelSessionContract

    assert ModelSessionContract is not None


def test_model_session_contract_fields() -> None:
    """ModelSessionContract must have the expected fields (schema stability)."""
    from omnibase_compat.overseer import ModelSessionContract

    fields = set(ModelSessionContract.model_fields.keys())
    required = {
        "session_id",
        "session_label",
        "phases_expected",
        "max_cycles",
        "cost_ceiling_usd",
        "halt_on_build_loop_failure",
        "dry_run",
        "started_at",
        "schema_version",
    }
    assert required <= fields, f"ModelSessionContract is missing fields: {required - fields}"


def test_model_session_contract_instantiation() -> None:
    """ModelSessionContract must be instantiable with minimum required fields."""
    from omnibase_compat.overseer import ModelSessionContract

    contract = ModelSessionContract(
        session_id="test-session-001",
        session_label="test-session",
        phases_expected=["build", "verify"],
    )
    assert contract.session_id == "test-session-001"
    assert contract.schema_version == "1.0"
    assert contract.dry_run is False


def test_model_routing_decision_still_exported() -> None:
    """ModelRoutingDecision must still be exported (regression guard for OMN-8038)."""
    from omnibase_compat.overseer import ModelRoutingDecision

    assert ModelRoutingDecision is not None


@pytest.mark.parametrize("name", ["ModelOvernightContract"])
def test_overnight_contract_not_exported(name: str) -> None:
    """ModelOvernightContract must NOT be exported from omnibase_compat.overseer.

    The overnight contract lives in onex_change_control.overseer. Exporting it
    here would violate the zero-upstream-deps rule for omnibase_compat.
    """
    from omnibase_compat import overseer

    assert name not in overseer.__all__, (
        f"{name} must not appear in omnibase_compat.overseer.__all__ — "
        "it lives in onex_change_control (OMN-8368)"
    )
