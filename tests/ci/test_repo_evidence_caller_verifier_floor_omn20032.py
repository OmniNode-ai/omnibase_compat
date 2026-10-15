# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-20032: pin the receipt-gate reusable that refuses a verifier below the floor."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
CALLER = REPO_ROOT / ".github" / "workflows" / "call-repo-evidence-gate.yml"

# Full shas of omnibase_core dev squash commits whose receipt-gate.yml carries the
# VERIFIER_FLOOR refusal in its "Install the pinned verifier" step: #1932, which adds
# it, and #1983, a descendant the caller pins since OMN-20074.
FLOOR_REUSABLE_PINS = (
    "4e4f5e0404d364e296c5d37db6aa3ab9e07f8ffa",
    "b192b64626e8aba609a261b3bec2e19b353195a1",
)

# 0.4.303 is the first omnimarket release carrying omnimarket#3511, the refusal of
# a contract that leaves an acceptance criterion unbound.
VERIFIER_FLOOR = (0, 4, 303)


def _version(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("."))


def _job() -> dict[str, Any]:
    doc = yaml.safe_load(CALLER.read_text(encoding="utf-8"))
    job: dict[str, Any] = doc["jobs"]["repo-evidence"]
    return job


def test_caller_pins_the_reusable_that_carries_the_verifier_floor() -> None:
    uses = _job()["uses"]
    assert re.fullmatch(
        r"OmniNode-ai/omnibase_core/\.github/workflows/receipt-gate\.yml@[0-9a-f]{40}",
        uses,
    )
    assert uses.split("@", 1)[1] in FLOOR_REUSABLE_PINS, (
        "pin the omnibase_core receipt-gate reusable at or past omnibase_core#1932"
    )


def test_caller_verifier_version_is_at_or_above_the_floor() -> None:
    assert _version(_job()["with"]["verifier-version"]) >= VERIFIER_FLOOR, (
        "verifier-version must be at or above the reusable's VERIFIER_FLOOR 0.4.303"
    )


@pytest.mark.parametrize(
    ("version", "expected"),
    [("0.4.280", False), ("0.4.302", False), ("0.4.303", True), ("0.4.305", True)],
)
def test_floor_comparison_has_a_refusing_and_an_admitting_case(
    version: str, expected: bool
) -> None:
    assert (_version(version) >= VERIFIER_FLOOR) is expected
