# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-20074: contract-validation validates with omnibase_core, not onex_change_control.

OCC retirement S8. The workflow used to check out the change-control repository
at a pinned sha and run its ``validate-yaml``. It now validates the branch
ticket's ``contracts/<ticket>.yaml`` with omnibase_core's ``ModelTicketContract``
at an exact version pinned in the validation step (this repository declares no
omnibase_core dependency, so the pin cannot live in pyproject.toml or uv.lock).
The required context name ``contract-validation`` does not change.

Failure modes this catches: a change-control reference creeping back in (checkout,
auth preflight, ``validate-yaml``); the validation step validating with anything but
``ModelTicketContract``; the core pin dropping below the release that carries the
``binds_ac`` strictness or becoming a range; the job or workflow name moving and
retiring the required context.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "contract-validation.yml"
# First omnibase_core release whose ModelTicketContract refuses a binds_ac entry
# that is not a criterion label and a binds_ac item with check type command_exit_0
# (omnibase_core#1935).
CORE_FLOOR = (0, 47, 39)
CORE_PIN = re.compile(r"--with\s+omnibase-core==(?P<version>\d+\.\d+\.\d+)(?=\s|\\|$)")
HEREDOC = re.compile(r"<<\s*'(?P<tag>\w+)'\n(?P<body>.*?)\n\s*(?P=tag)\n", re.DOTALL)


def _doc() -> dict[Any, Any]:
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(doc, dict)
    return doc


def _steps() -> list[dict[str, Any]]:
    return _doc()["jobs"]["contract-validation"]["steps"]


def _validation_step() -> dict[str, Any]:
    matches = [step for step in _steps() if step.get("id") == "validate-contract"]
    assert len(matches) == 1
    return matches[0]


def test_workflow_names_no_change_control_repository() -> None:
    offenders = [
        number
        for number, line in enumerate(WORKFLOW.read_text(encoding="utf-8").splitlines(), 1)
        if re.search(r"onex[_-]change[_-]control|validate-yaml", line, re.IGNORECASE)
    ]
    assert offenders == [], f"change-control references at lines {offenders}"


def test_reference_detector_sees_a_planted_change_control_checkout() -> None:
    """Positive control: the scan above flags the shapes this change removed."""
    planted = (
        "repository: OmniNode-ai/onex_change_control",
        "path: .onex_change_control_validators",
        "uv run validate-yaml contracts/OMN-1.yaml",
    )
    for line in planted:
        assert re.search(r"onex[_-]change[_-]control|validate-yaml", line, re.IGNORECASE)


def test_workflow_checks_out_only_the_calling_repository() -> None:
    for step in _steps():
        if str(step.get("uses", "")).startswith("actions/checkout"):
            assert "repository" not in (step.get("with") or {}), step.get("name")


def test_required_context_name_is_unchanged() -> None:
    doc = _doc()
    assert doc["name"] == "Contract Validation"
    assert list(doc["jobs"]) == ["contract-validation"]
    assert doc["jobs"]["contract-validation"]["name"] == "contract-validation"


def test_validation_step_pins_omnibase_core_exactly_at_or_above_the_binds_ac_release() -> None:
    run = _validation_step()["run"]
    pins = CORE_PIN.findall(run)
    assert len(pins) == 1, "exactly one exact omnibase-core pin in the validation step"
    assert tuple(int(part) for part in pins[0].split(".")) >= CORE_FLOOR
    assert "omnibase-core>" not in run
    assert "omnibase-core<" not in run


def test_validation_step_validates_with_model_ticket_contract() -> None:
    run = _validation_step()["run"]
    heredocs = HEREDOC.findall(run)
    assert len(heredocs) == 1
    tree = ast.parse(heredocs[0][1])
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module == "omnibase_core.models.ticket.model_ticket_contract"
        for alias in node.names
    }
    assert imported == {"ModelTicketContract"}
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "model_validate"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "ModelTicketContract"
        for node in ast.walk(tree)
    )


def test_validation_step_skips_without_a_ticket_or_a_contract_and_fails_on_an_invalid_one() -> None:
    run = _validation_step()["run"]
    assert run.count("validation-status=skipped") == 2
    assert "validation-status=passed" in run
    assert "validation-status=failed" in run
    assert re.search(r"sys\.exit\(1\)", run)
