# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""The runner-IP gate must actually see this repository's tests (OMN-17993).

This repository ships `.github/workflows/ban-hardcoded-runner-ip.yml`, whose
entire purpose is to reject the literal lab runner address — and carried that
exact literal as a fixture value under `tests/`. Whatever the gate scanned, it
did not scan here. Root cause 4.4 of the 2026-09-06 public-repo hygiene
inventory: a gate scoped to a subtree reports green over the rest of the tree.

Two halves, both required. The reusable workflow in omniclaude now scans
`tests/**`; this caller's `paths:` filter must list it too, or the change that
introduces a violation never triggers the job that would catch it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CALLER = REPO_ROOT / ".github" / "workflows" / "ban-hardcoded-runner-ip.yml"

# The banned literal, assembled rather than spelled, so this test file is not
# itself a finding for the gate it is testing.
BANNED = ".".join(["192", "168", "86", "201"])
_ANNOTATION = "onex-allow-internal-ip"


@pytest.mark.unit
def test_caller_paths_filter_includes_tests() -> None:
    doc = yaml.safe_load(CALLER.read_text(encoding="utf-8"))
    paths = doc[True]["pull_request"]["paths"]  # YAML 1.1 parses `on:` as True
    assert "tests/**" in paths
    assert ".github/workflows/**" in paths


@pytest.mark.unit
def test_no_unannotated_runner_ip_literal_in_tests() -> None:
    """The live invariant. RED before the delegation-profile fixture was
    repointed at a non-routable placeholder."""
    offenders: list[str] = []
    for path in sorted((REPO_ROOT / "tests").rglob("*")):
        if not path.is_file() or path.suffix in {".pyc", ".png", ".gz"}:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if re.search(re.escape(BANNED), line) and _ANNOTATION not in line:
                rel = path.relative_to(REPO_ROOT)
                offenders.append(f"{rel}:{lineno}")
    assert offenders == [], "\n".join(offenders)


@pytest.mark.unit
def test_caller_pins_reusable_to_an_exact_sha() -> None:
    """`@main` on this reusable is inert, so the ref must be a 40-hex SHA.

    omniclaude's `main` is release-synced and lags `dev` by design, so
    `...@main` still resolves to the pre-OMN-17993 scanner body that scans
    workflow files only. A tests-only diff carrying the banned literal
    triggers the job (this caller's `paths:` filter was widened) and the
    `@main` body prints "No workflow files to check." and exits 0 green.
    Pinning the exact SHA of the widened body is what makes the gate real.
    """
    doc = yaml.safe_load(CALLER.read_text(encoding="utf-8"))
    uses = doc["jobs"]["ban-hardcoded-runner-ip"]["uses"]
    ref = uses.rsplit("@", 1)[1]
    assert re.fullmatch(r"[0-9a-f]{40}", ref), (
        f"ban-hardcoded-runner-ip must pin an exact 40-hex SHA, got {ref!r}. "
        "A branch or tag ref re-introduces the OMN-17993 inert-gate defect."
    )
