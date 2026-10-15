# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-20074: the last change-control residue in omnibase_compat's gates.

Failure modes this catches: the repo-evidence caller pins a receipt-gate
reusable that still carries the change-control evidence mode, or passes the
retired comparison input; the no-infra-edge guard admits a dependency on the
retired change-control package; the skip-token hook tells an author to push a
contract to the change-control repository instead of to this repository.
"""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
CALLER = REPO_ROOT / ".github" / "workflows" / "call-repo-evidence-gate.yml"
HOOK = REPO_ROOT / ".pre-commit-hooks" / "reject-deploy-gate-skip-token.sh"
GUARD = REPO_ROOT / "scripts" / "check_no_infra_edge.py"

# Squash commit of omnibase_core#1983 on that repository's dev branch. It
# descends from omnibase_core#1974, which removes the change-control evidence
# mode from receipt-gate.yml, and from #1932 (VERIFIER_FLOOR).
RECEIPT_GATE_PIN = "b192b64626e8aba609a261b3bec2e19b353195a1"
# Pins whose receipt-gate.yml still carries the change-control evidence mode.
PRE_REMOVAL_PINS = (
    "4e4f5e0404d364e296c5d37db6aa3ab9e07f8ffa",
    "fb0c6c2117d5868a398b0920cd0048d0824415b1",
)


def _job() -> dict[str, Any]:
    doc = yaml.safe_load(CALLER.read_text(encoding="utf-8"))
    job: dict[str, Any] = doc["jobs"]["repo-evidence"]
    return job


def _guard() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_no_infra_edge", GUARD)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_caller_pins_the_receipt_gate_without_the_change_control_mode() -> None:
    sha = _job()["uses"].split("@", 1)[1]
    assert sha == RECEIPT_GATE_PIN
    assert sha not in PRE_REMOVAL_PINS


def test_caller_passes_no_retired_comparison_input() -> None:
    inputs = _job()["with"]
    assert "compare-with-occ" not in inputs
    assert inputs == {
        "evidence-source": "caller",
        "verifier-version": "0.4.310",
        "shadow": "false",
    }


def test_caller_comments_describe_no_change_control_rollback() -> None:
    text = CALLER.read_text(encoding="utf-8")
    assert "compare-with-occ" not in text
    assert "OCC" not in text


def test_no_infra_edge_refuses_a_declared_change_control_dependency(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[project]\n"
        'name = "omnibase-compat"\n'
        'version = "0.0.0"\n'
        'dependencies = ["onex_change_control>=0.1.0"]\n',
        encoding="utf-8",
    )
    violations = _guard().scan_dependency_closure(tmp_path)
    assert any("onex-change-control" in v and "pyproject" in v for v in violations), violations


def test_no_infra_edge_refuses_a_locked_change_control_package(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "omnibase-compat"\nversion = "0.0.0"\ndependencies = []\n',
        encoding="utf-8",
    )
    (tmp_path / "uv.lock").write_text(
        'version = 1\n\n[[package]]\nname = "onex-change-control"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )
    violations = _guard().scan_dependency_closure(tmp_path)
    assert any("onex-change-control" in v and "uv.lock" in v for v in violations), violations


def test_skip_token_hook_points_receipt_gate_at_this_repository(tmp_path: Path) -> None:
    body = tmp_path / "body.md"
    # Built from parts so this source file holds no literal token.
    body.write_text("[" + "skip-" + "receipt-gate: x]\n", encoding="utf-8")
    result = subprocess.run(
        ["/bin/bash", str(HOOK), str(body)],
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 1, result.stderr
    assert "contracts/OMN-" in result.stderr
    assert "OCC" not in result.stderr
