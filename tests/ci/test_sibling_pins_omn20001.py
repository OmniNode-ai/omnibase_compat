# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Workflows must read sibling repos at a pinned sha, never a live branch (OMN-20001).

Ruling: each repo checks only itself; any read of a sibling uses the version this
repo has pinned, so a merge in one repo cannot turn another repo red. A new
sibling version is integration-tested by the consumer in a PR that moves the pin.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
SHA = re.compile(r"^[0-9a-f]{40}$")
USES_SIBLING = re.compile(r"^OmniNode-ai/(?!omnibase_compat/)[^/@]+/[^@]+@(?P<ref>\S+)$")
CLONE_SIBLING = re.compile(r"git\s+clone\b[^\n]*github\.com/OmniNode-ai/(?!omnibase_compat\b)\S+")
FETCH_SHA = re.compile(r"fetch\b[^\n]*github\.com/OmniNode-ai/\S+\s+(?P<ref>\S+)")


def _steps(doc: dict) -> list[dict]:
    jobs = doc.get("jobs") or {}
    out: list[dict] = []
    for job in jobs.values():
        if "uses" in job:
            out.append({"uses": job["uses"]})
        out.extend(job.get("steps") or [])
    return out


@pytest.mark.unit
def test_workflow_corpus_is_not_empty() -> None:
    """Positive control: the scan below sees sibling reads at all."""
    reads = 0
    for wf in WORKFLOWS:
        for step in _steps(yaml.safe_load(wf.read_text(encoding="utf-8"))):
            if USES_SIBLING.match(str(step.get("uses", ""))):
                reads += 1
    assert reads >= 10


@pytest.mark.unit
@pytest.mark.parametrize("wf", WORKFLOWS, ids=lambda p: p.name)
def test_sibling_reads_are_pinned_to_a_sha(wf: Path) -> None:
    offenders: list[str] = []
    for step in _steps(yaml.safe_load(wf.read_text(encoding="utf-8"))):
        uses = str(step.get("uses", ""))
        m = USES_SIBLING.match(uses)
        if m and not SHA.match(m.group("ref")):
            offenders.append(f"uses {uses}")
        with_ = step.get("with") or {}
        repo = str(with_.get("repository", ""))
        if (
            uses.startswith("actions/checkout")
            and repo.startswith("OmniNode-ai/")
            and repo != "OmniNode-ai/omnibase_compat"
            and not SHA.match(str(with_.get("ref", "")))
        ):
            offenders.append(f"checkout {repo} ref={with_.get('ref')!r}")
        run = str(step.get("run", ""))
        if CLONE_SIBLING.search(run):
            offenders.append("git clone of a sibling (use init + fetch <sha>)")
        for fm in FETCH_SHA.finditer(run):
            if not SHA.match(fm.group("ref")):
                offenders.append(f"fetch ref {fm.group('ref')}")
    assert offenders == [], f"{wf.name}: " + "; ".join(offenders)
