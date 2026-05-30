# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Regression tests for package-level delegation wire exports."""

from __future__ import annotations

import pytest

from omnibase_compat.contracts.delegation import wire


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_quality_contract_helpers_are_exported_from_wire_package() -> None:
    assert "response_non_empty" in wire.SUPPORTED_ACCEPTANCE_CRITERIA
    assert wire.MAX_WORDS_PER_SENTENCE_RE.match("max_words_per_sentence_20")
    assert wire.validate_acceptance_criteria(("response_non_empty",)) == ("response_non_empty",)
