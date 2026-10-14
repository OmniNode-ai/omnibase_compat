# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-20074: the schema compatibility gate is named for what it checks.

The ``schema-compat`` job reads ``contracts/OMN-*.yaml`` against omnibase_core's
``ModelTicketContract`` and reads nothing from the change-control repository, so
its display name, which is also its required status context, must not name
change control. The required-checks manifest must carry the same name, still
REQUIRED, so the gate is exactly as strict as before the rename.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest
import yaml

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "onex-schema-compat.yml"
MANIFEST = REPO_ROOT / ".github" / "required-checks.yaml"
JOB_KEY = "schema-compat"
NEW_NAME = "ONEX Ticket Contract Schema Compatibility"
OLD_NAME = "ONEX Change Control Schema Compatibility"


def _job_name() -> str:
    workflow = cast("dict[str, Any]", yaml.safe_load(WORKFLOW.read_text(encoding="utf-8")))
    return str(workflow["jobs"][JOB_KEY]["name"])


def _manifest_entries() -> list[dict[str, Any]]:
    manifest = cast("dict[str, Any]", yaml.safe_load(MANIFEST.read_text(encoding="utf-8")))
    return [entry for entry in manifest["gates"] if entry.get("workflow") == WORKFLOW.name]


def test_job_display_name_does_not_name_change_control() -> None:
    assert _job_name() == NEW_NAME
    assert "change control" not in _job_name().lower()


def test_required_checks_entry_carries_the_job_name_and_stays_required() -> None:
    (entry,) = _manifest_entries()
    assert entry["name"] == _job_name()
    assert entry["mode"] == "REQUIRED"
    assert entry["job_path"] == [JOB_KEY]


def test_manifest_has_no_entry_under_the_old_name() -> None:
    names = [str(entry.get("name")) for entry in yaml.safe_load(MANIFEST.read_text())["gates"]]
    assert OLD_NAME not in names
