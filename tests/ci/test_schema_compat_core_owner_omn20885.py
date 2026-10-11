# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-20885: ``ONEX Change Control Schema Compatibility`` reads the schema owner.

The job used to check out onex_change_control as "the upstream schema
authority" and compare that package's version with a hardcoded reader version.
No file in this repository matched its artifact globs, so it validated nothing,
and a package version is not a wire schema version. The wire schema this
repository reads and writes is the ticket contract (``contracts/OMN-*.yaml``),
whose model is ``omnibase_core``'s ``ModelTicketContract``.

The job now compares the ``schema_version`` every repo contract declares with
the one the pinned ``omnibase_core`` model carries, through ``omnibase_spi``'s
``is_compatible``: a major mismatch fails. ``omnibase_compat`` has no upstream
runtime dependency, so core is installed only inside the workflow step
(``uv run --with``), never in ``pyproject.toml``. These tests run the step's own
shell command, extracted from the workflow file, against the repo contracts and
against planted ones.
"""

from __future__ import annotations

import os
import re
import subprocess
import tomllib
from pathlib import Path
from typing import Any, cast

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "onex-schema-compat.yml"
PYPROJECT = REPO_ROOT / "pyproject.toml"
JOB_NAME = "ONEX Change Control Schema Compatibility"
STEP_NAME = "Check ticket-contract schema compatibility"

_GOOD = 'schema_version: "1.0.0"\nticket_id: "OMN-1"\ntitle: "planted"\n'
_EXACT_PIN = re.compile(r"--with\s+(omnibase-core|omnibase-spi)==\d+\.\d+\.\d+\b")


def _workflow() -> dict[str, Any]:
    loaded = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return cast("dict[str, Any]", loaded)


def _steps() -> list[dict[str, Any]]:
    jobs = cast("dict[str, dict[str, Any]]", _workflow()["jobs"])
    (job,) = [job for job in jobs.values() if job.get("name") == JOB_NAME]
    steps = job["steps"]
    assert isinstance(steps, list)
    return cast("list[dict[str, Any]]", steps)


def _step_run() -> str:
    (step,) = [step for step in _steps() if step.get("name") == STEP_NAME]
    return str(step["run"])


def _run_step(cwd: Path) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PYTHON_VERSION"] = str(_workflow()["env"]["PYTHON_VERSION"])
    return subprocess.run(
        ["bash", "-eo", "pipefail", "-c", _step_run()],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _contracts(tmp_path: Path, files: dict[str, str]) -> Path:
    contracts = tmp_path / "contracts"
    contracts.mkdir()
    for name, text in files.items():
        (contracts / name).write_text(text, encoding="utf-8")
    return tmp_path


def test_job_reads_no_onex_change_control() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "onex_change_control" not in text
    assert "validate-yaml" not in text
    for step in _steps():
        assert "onex_change_control" not in str(step.get("with", {}))


def test_core_and_spi_are_exactly_pinned_in_the_step() -> None:
    pins = {m.group(1) for m in _EXACT_PIN.finditer(_step_run())}
    assert pins == {"omnibase-core", "omnibase-spi"}, _step_run()


def test_core_is_a_ci_tool_not_a_runtime_dependency() -> None:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    declared = [
        *project.get("dependencies", []),
        *[d for group in project.get("optional-dependencies", {}).values() for d in group],
    ]
    assert not [d for d in declared if re.match(r"omnibase[-_](core|spi)\b", d)], declared
    lock = (REPO_ROOT / "uv.lock").read_text(encoding="utf-8")
    assert "omnibase-core" not in lock
    assert "omnibase-spi" not in lock


def test_repo_contracts_are_compatible_with_the_core_model() -> None:
    result = _run_step(REPO_ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    count = len(list((REPO_ROOT / "contracts").glob("OMN-*.yaml")))
    assert count > 0
    assert f"{count} ticket contract(s)" in result.stdout


def test_planted_major_mismatch_fails(tmp_path: Path) -> None:
    root = _contracts(
        tmp_path,
        {"OMN-1.yaml": _GOOD, "OMN-2.yaml": _GOOD.replace("1.0.0", "2.0.0")},
    )
    result = _run_step(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "contracts/OMN-2.yaml" in result.stdout
    assert "contracts/OMN-1.yaml" not in result.stdout


def test_minor_difference_passes(tmp_path: Path) -> None:
    root = _contracts(tmp_path, {"OMN-1.yaml": _GOOD.replace("1.0.0", "1.4.0")})
    result = _run_step(root)
    assert result.returncode == 0, result.stdout + result.stderr


def test_unparseable_version_fails(tmp_path: Path) -> None:
    root = _contracts(tmp_path, {"OMN-1.yaml": _GOOD.replace('"1.0.0"', '"one"')})
    result = _run_step(root)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "contracts/OMN-1.yaml" in result.stdout


def test_empty_contracts_dir_fails(tmp_path: Path) -> None:
    root = _contracts(tmp_path, {"README.md": "no contracts\n"})
    result = _run_step(root)
    assert result.returncode == 1, result.stdout + result.stderr


def test_no_contracts_dir_passes(tmp_path: Path) -> None:
    result = _run_step(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
