# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""OMN-21291: each ticket contract moved into ``contracts/`` by omnibase_compat#244 is present.

omnibase_compat#244 moves ticket contracts out of the retired change-control
repository into this repository's ``contracts/`` directory. Each moved contract
must exist, load as a YAML mapping, and carry its own ticket id.

Failure modes this catches: a moved contract missing from ``contracts/``; a file
that does not parse as a mapping; a file whose ``ticket_id`` names another ticket.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.unit

CONTRACTS_DIR = Path(__file__).resolve().parents[2] / "contracts"
MOVED_CONTRACT_IDS = ("OMN-19642",)


@pytest.mark.parametrize("ticket_id", MOVED_CONTRACT_IDS)
def test_moved_contract_exists_and_names_its_ticket(ticket_id: str) -> None:
    path = CONTRACTS_DIR / f"{ticket_id}.yaml"
    assert path.is_file(), f"{path.name} is absent from contracts/"
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(doc, dict), f"{path.name} does not load as a mapping"
    assert doc.get("ticket_id") == ticket_id
