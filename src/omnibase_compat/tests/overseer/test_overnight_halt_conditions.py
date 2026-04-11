# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for OMN-8375 halt_condition + required_outcomes schema."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.model_overnight_contract import (
    ModelOvernightContract,
    ModelOvernightHaltCondition,
    ModelOvernightPhaseSpec,
)


@pytest.mark.unit
def test_halt_condition_legacy_shape_still_validates() -> None:
    """Pre-OMN-8375 halt conditions (only the four original fields) still load."""
    cond = ModelOvernightHaltCondition(
        condition_id="cost_ceiling",
        description="Stop if cost exceeds ceiling",
        check_type="cost_ceiling",
        threshold=5.0,
    )
    assert cond.on_halt == "hard_halt"
    assert cond.skill is None
    assert cond.pr is None
    assert cond.outcome is None


@pytest.mark.unit
def test_halt_condition_pr_blocked_too_long_with_dispatch_skill() -> None:
    """pr_blocked_too_long halt condition with dispatch_skill action."""
    cond = ModelOvernightHaltCondition(
        condition_id="pr1227_blocked",
        description="PR #1227 stuck too long",
        check_type="pr_blocked_too_long",
        pr=1227,
        threshold_minutes=10.0,
        on_halt="dispatch_skill",
        skill="onex:pr_polish",
    )
    assert cond.check_type == "pr_blocked_too_long"
    assert cond.pr == 1227
    assert cond.threshold_minutes == 10.0
    assert cond.on_halt == "dispatch_skill"
    assert cond.skill == "onex:pr_polish"


@pytest.mark.unit
def test_halt_condition_required_outcome_missing() -> None:
    cond = ModelOvernightHaltCondition(
        condition_id="need_delegation",
        description="delegation pipeline must be active",
        check_type="required_outcome_missing",
        outcome="delegation_pipeline_active",
        on_halt="halt_and_notify",
    )
    assert cond.outcome == "delegation_pipeline_active"
    assert cond.on_halt == "halt_and_notify"


@pytest.mark.unit
def test_halt_condition_unknown_check_type_rejected() -> None:
    with pytest.raises(ValidationError):
        ModelOvernightHaltCondition(
            condition_id="bad",
            description="nope",
            check_type="not_a_type",  # type: ignore[arg-type]
        )


@pytest.mark.unit
def test_halt_condition_unknown_on_halt_rejected() -> None:
    with pytest.raises(ValidationError):
        ModelOvernightHaltCondition(
            condition_id="bad",
            description="nope",
            check_type="custom",
            on_halt="explode",  # type: ignore[arg-type]
        )


@pytest.mark.unit
def test_phase_spec_required_outcomes_and_halt_conditions() -> None:
    """ModelOvernightPhaseSpec accepts per-phase halt_conditions + required_outcomes."""
    cond = ModelOvernightHaltCondition(
        condition_id="pr1227_blocked",
        description="watch PR #1227",
        check_type="pr_blocked_too_long",
        pr=1227,
        threshold_minutes=10.0,
        on_halt="dispatch_skill",
        skill="onex:pr_polish",
    )
    spec = ModelOvernightPhaseSpec(
        phase_name="merge_sweep",
        required_outcomes=("all_phase_prs_merged",),
        halt_conditions=(cond,),
    )
    assert spec.required_outcomes == ("all_phase_prs_merged",)
    assert spec.halt_conditions[0].skill == "onex:pr_polish"


@pytest.mark.unit
def test_contract_round_trip_with_new_fields() -> None:
    """Full contract with new fields round-trips through model_dump/validate."""
    contract = ModelOvernightContract(
        session_id="omn-8375-test",
        created_at=datetime.now(tz=UTC),
        phases=(
            ModelOvernightPhaseSpec(
                phase_name="build_loop_orchestrator",
                required_outcomes=("delegation_pipeline_active",),
                halt_conditions=(
                    ModelOvernightHaltCondition(
                        condition_id="need_delegation",
                        description="must be active",
                        check_type="required_outcome_missing",
                        outcome="delegation_pipeline_active",
                        on_halt="halt_and_notify",
                    ),
                ),
            ),
        ),
    )
    dumped = contract.model_dump()
    reloaded = ModelOvernightContract.model_validate(dumped)
    assert reloaded.phases[0].required_outcomes == ("delegation_pipeline_active",)
    assert reloaded.phases[0].halt_conditions[0].outcome == "delegation_pipeline_active"
