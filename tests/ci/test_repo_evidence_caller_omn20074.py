# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-20074: omnibase_compat's repo-evidence caller enforces after the S6 cut-over.

The caller verifies repo-owned evidence without shadowing or comparing with OCC.

Failure modes this catches: the caller regained ``shadow`` true or passes the
retired ``compare-with-occ`` input; the pin moved to a branch name or an older
reusable; the verifier moved back to a released version; the caller moved to
``pull_request`` (a PR could then edit what judges it); a job name was added
(the context prefix would change); the repo contract lost a falsifier.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
CALLER = WORKFLOWS / "call-repo-evidence-gate.yml"
CONTRACT = REPO_ROOT / "contracts" / "OMN-20074.yaml"

# The omnibase_core dev-merge tag the caller pins (OMN-21852). Its history holds
# omnibase_core#2203, which adds verifier-tag, and descends from #1983 (caller
# evidence is the only mode) and #1932 (OMN-20032). The verifier is installed from
# the omnimarket dev-merge tag, not from a released version.
DEV_MERGE_TAG = r"dev-[0-9]{14}-[0-9a-f]{12}"
RECEIPT_GATE_TAG = "dev-20261101005012-ac2f26e3e5bf"
VERIFIER_TAG = "dev-20261101000200-949993edf3b7"


def _load(path: Path) -> dict[Any, Any]:
    assert path.is_file(), f"missing {path}"
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _job() -> dict[str, Any]:
    job: dict[str, Any] = _load(CALLER)["jobs"]["repo-evidence"]
    return job


def test_caller_runs_from_the_base_branch_on_dev_and_main() -> None:
    doc = _load(CALLER)
    # YAML 1.1 reads a bare `on` as the boolean True.
    triggers = doc["on"] if "on" in doc else doc[True]
    assert set(triggers) == {"pull_request_target"}
    assert triggers["pull_request_target"]["branches"] == ["dev", "main"]
    assert triggers["pull_request_target"]["types"] == [
        "opened",
        "synchronize",
        "reopened",
        "edited",
        "ready_for_review",
    ]
    assert doc["permissions"] == {"contents": "read", "pull-requests": "read"}
    assert set(doc["jobs"]) == {"repo-evidence"}


def test_caller_job_is_a_bare_call_with_no_secrets() -> None:
    job = _job()
    for key in ("steps", "secrets", "if", "name", "permissions"):
        assert key not in job, f"caller job must not declare {key}"
    assert "secrets: inherit" not in CALLER.read_text(encoding="utf-8")


def test_caller_pins_the_current_receipt_gate_by_dev_merge_tag() -> None:
    uses = _job()["uses"]
    assert re.fullmatch(
        r"OmniNode-ai/omnibase_core/\.github/workflows/receipt-gate\.yml@" + DEV_MERGE_TAG,
        uses,
    )
    assert uses.split("@", 1)[1] == RECEIPT_GATE_TAG


def test_current_receipt_gate_verifier_tag_is_a_dev_merge_tag_and_no_version() -> None:
    inputs = _job()["with"]
    assert re.fullmatch(DEV_MERGE_TAG, inputs["verifier-tag"])
    assert inputs["verifier-tag"] == VERIFIER_TAG
    assert "verifier-version" not in inputs


def test_caller_passes_no_retired_comparison_input() -> None:
    # OMN-20074: the pinned reusable defaults the retired comparison input to
    # "false" and fails dod-verify on any other value.
    assert "compare-with-occ" not in _job()["with"]


def test_caller_enforces_with_the_pinned_inputs() -> None:
    job = _job()
    assert job["uses"] == (
        f"OmniNode-ai/omnibase_core/.github/workflows/receipt-gate.yml@{RECEIPT_GATE_TAG}"
    )
    # Quoted strings: the reusable's boolean-like inputs are string inputs.
    assert job["with"] == {
        "evidence-source": "caller",
        "verifier-tag": VERIFIER_TAG,
        "shadow": "false",
    }


def test_repo_contract_names_a_falsifier_per_criterion() -> None:
    contract = _load(CONTRACT)
    assert contract["ticket_id"] == "OMN-20074"
    criteria = [ac for req in contract["requirements"] for ac in req["acceptance"]]
    assert criteria, "contract must declare acceptance criteria"
    checks = [check["check_value"] for item in contract["dod_evidence"] for check in item["checks"]]
    for criterion in criteria:
        assert "falsifier:" in criterion["statement"]
        falsifier = criterion["statement"].split("falsifier:", 1)[1].strip()
        assert falsifier in checks, f"{criterion['id']} falsifier has no dod check"
        test_file = falsifier.split()[3]
        assert (REPO_ROOT / test_file).is_file(), f"{test_file} does not exist"
