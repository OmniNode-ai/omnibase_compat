# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Canonical helper for the ``AUTOWIRE_STRICT`` env flag.

This module hosts a single function, :func:`is_strict_mode`, which reports
whether the runtime-boot auto-wiring layer should run in strict mode.

The helper exists so every call site agrees on the exact semantic and a
future state-triggered follow-up (flipping the default from lenient to
strict) can replace one comparison site instead of grepping every consumer.
"""

from __future__ import annotations

import os

_ENV_VAR: str = "AUTOWIRE_STRICT"
_STRICT_LITERAL: str = "1"


def is_strict_mode() -> bool:
    """Return ``True`` iff ``AUTOWIRE_STRICT`` is set to the literal string ``"1"``.

    The comparison is **strictly** against the one-character string ``"1"``.
    All other values, including common truthy strings, produce ``False``.

    Examples of values that return ``False`` (non-strict / lenient):

    - variable unset in the environment
    - ``""`` (empty string)
    - ``"0"``
    - ``"true"`` / ``"True"`` / ``"TRUE"``
    - ``"yes"`` / ``"on"``
    - ``"1 "`` (with trailing whitespace — no implicit trimming)

    Only ``"1"`` — exact, unpadded — returns ``True``.

    This literal-``"1"``-only invariant is intentional: it preserves the
    hot-patch semantic in the runtime-boot durability plan (``OMN-9220``
    Task 3) so the strict-default flip can later be a single-line change.
    Loosening the semantic (e.g. accepting ``"true"``) is a breaking
    behavior change for downstream consumers and MUST be coordinated with
    those consumers.

    The env var is read on every call, so tests can toggle it via
    ``monkeypatch.setenv`` / ``monkeypatch.delenv`` without reloading the
    module.

    Returns:
        ``True`` if ``os.environ["AUTOWIRE_STRICT"] == "1"`` exactly,
        otherwise ``False``.
    """
    return os.environ.get(_ENV_VAR) == _STRICT_LITERAL
