# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""TDD-first test for OMN-8431: omnibase_compat.overseer module fully removed.

Fails before removal (directory still present), passes after.
"""

from __future__ import annotations

import importlib


def test_omnibase_compat_overseer_module_absent() -> None:
    """After migration, omnibase_compat must NOT have an overseer submodule.

    The entire overseer/ directory has been removed as part of OMN-8431.
    Canonical location is now onex_change_control.overseer.
    """
    result = importlib.util.find_spec("omnibase_compat.overseer")
    assert result is None, (
        "omnibase_compat.overseer module still importable — "
        "directory should be fully removed (OMN-8431)"
    )
