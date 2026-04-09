# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.enum_failure_class import EnumFailureClass
from omnibase_compat.overseer.enum_verifier_verdict import EnumVerifierVerdict
from omnibase_compat.overseer.model_verifier_output import (
    ModelVerifierCheckResult,
    ModelVerifierOutput,
)


@pytest.mark.unit
def test_verifier_verdict_pass_exact() -> None:
    """EnumVerifierVerdict.PASS == 'PASS' and str() round-trip."""
    assert EnumVerifierVerdict.PASS == "PASS"
    assert str(EnumVerifierVerdict.PASS) == "PASS"
    assert EnumVerifierVerdict("PASS") == EnumVerifierVerdict.PASS


@pytest.mark.unit
def test_verifier_verdict_all_members() -> None:
    expected = {"PASS", "FAIL", "RETRY_REQUIRED", "ESCALATE"}
    assert {e.value for e in EnumVerifierVerdict} == expected


@pytest.mark.unit
def test_verifier_output_frozen() -> None:
    """ModelVerifierOutput is immutable."""
    output = ModelVerifierOutput(verdict=EnumVerifierVerdict.PASS)
    with pytest.raises(ValidationError):
        output.verdict = EnumVerifierVerdict.FAIL


@pytest.mark.unit
def test_verifier_output_with_violations() -> None:
    """Construct with a list of check results, some failed."""
    checks = (
        ModelVerifierCheckResult(name="schema_valid", passed=True),
        ModelVerifierCheckResult(
            name="invariant_hold",
            passed=False,
            message="invariant X violated",
            failure_class=EnumFailureClass.DATA_INTEGRITY,
        ),
        ModelVerifierCheckResult(name="timeout_check", passed=True),
    )
    output = ModelVerifierOutput(
        verdict=EnumVerifierVerdict.FAIL,
        checks=checks,
        failure_class=EnumFailureClass.DATA_INTEGRITY,
        summary="1 of 3 checks failed",
    )
    assert output.verdict == EnumVerifierVerdict.FAIL
    assert len(output.checks) == 3
    failed = [c for c in output.checks if not c.passed]
    assert len(failed) == 1
    assert failed[0].failure_class == EnumFailureClass.DATA_INTEGRITY


@pytest.mark.unit
def test_verifier_output_failure_class_is_enum() -> None:
    """Construct with EnumFailureClass, assert isinstance after round-trip."""
    output = ModelVerifierOutput(
        verdict=EnumVerifierVerdict.FAIL,
        failure_class=EnumFailureClass.UNKNOWN,
    )
    data = output.model_dump()
    restored = ModelVerifierOutput.model_validate(data)
    assert isinstance(restored.failure_class, EnumFailureClass)
    assert restored.failure_class == EnumFailureClass.UNKNOWN


@pytest.mark.unit
def test_verifier_check_result_frozen() -> None:
    """ModelVerifierCheckResult is immutable."""
    check = ModelVerifierCheckResult(name="test", passed=True)
    with pytest.raises(ValidationError):
        check.passed = False


@pytest.mark.unit
def test_verifier_output_extra_forbid() -> None:
    """Extra fields are rejected."""
    with pytest.raises(ValidationError):
        ModelVerifierOutput(
            verdict=EnumVerifierVerdict.PASS,
            unknown_field="bad",  # type: ignore[call-arg]
        )


@pytest.mark.unit
def test_verifier_output_shim_outputs() -> None:
    """Shim outputs round-trip correctly."""
    output = ModelVerifierOutput(
        verdict=EnumVerifierVerdict.PASS,
        shim_outputs={"key1": "val1", "key2": "val2"},
    )
    data = output.model_dump()
    restored = ModelVerifierOutput.model_validate(data)
    assert restored.shim_outputs == {"key1": "val1", "key2": "val2"}
