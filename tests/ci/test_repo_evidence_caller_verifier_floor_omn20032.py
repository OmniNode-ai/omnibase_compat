# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-20032, OMN-21852: the repo-evidence caller pins a dev-merge tagged receipt-gate.

OMN-20032 added the verifier floor to the reusable. Since OMN-21852 the floor is an
ancestry fact the reusable checks (the omnimarket commit must descend from its floor
commit), so the caller pins the reusable by an omnibase_core dev-merge tag and passes
the verifier as an omnimarket dev-merge tag, not as a released version.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
CALLER = REPO_ROOT / ".github" / "workflows" / "call-repo-evidence-gate.yml"

# A dev-merge tag: dev-<UTC YYYYMMDDHHMMSS>-<first 12 hex digits of the merge commit>.
DEV_MERGE_TAG = r"dev-[0-9]{14}-[0-9a-f]{12}"
RECEIPT_GATE_USES = (
    r"OmniNode-ai/omnibase_core/\.github/workflows/receipt-gate\.yml@" + DEV_MERGE_TAG
)


def _job() -> dict[str, Any]:
    doc = yaml.safe_load(CALLER.read_text(encoding="utf-8"))
    job: dict[str, Any] = doc["jobs"]["repo-evidence"]
    return job


def test_caller_pins_the_reusable_that_carries_the_verifier_floor() -> None:
    uses = _job()["uses"]
    assert re.fullmatch(RECEIPT_GATE_USES, uses), (
        "pin the omnibase_core receipt-gate reusable by a dev-merge tag at or past #2203"
    )


def test_caller_verifier_tag_is_a_dev_merge_tag_at_or_above_the_floor() -> None:
    inputs = _job()["with"]
    assert re.fullmatch(DEV_MERGE_TAG, inputs["verifier-tag"]), (
        "verifier-tag must be an omnimarket dev-merge tag; the reusable refuses one that "
        "does not descend from its floor commit"
    )
    assert "verifier-version" not in inputs


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("0.4.310", False),
        ("dev-2026110100020-949993edf3b7", False),
        ("dev-20261101000200-949993EDF3B7", False),
        ("dev-20261101000200-949993edf3b", False),
        ("dev-20261101000200-949993edf3b7", True),
    ],
)
def test_floor_comparison_has_a_refusing_and_an_admitting_case(tag: str, expected: bool) -> None:
    assert (re.fullmatch(DEV_MERGE_TAG, tag) is not None) is expected
