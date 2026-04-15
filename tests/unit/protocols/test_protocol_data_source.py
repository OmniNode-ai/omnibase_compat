# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for ProtocolDataSource (tabular data source adapter protocol)."""

from __future__ import annotations

import pytest

from omnibase_compat.protocols.protocol_data_source import ProtocolDataSource


class _MockDataSource:
    def get_row_count(self, table_name: str) -> int:
        return 0

    def get_sample_rows(self, table_name: str, sample_size: int) -> list[dict[str, str]]:
        return []

    def get_columns(self, table_name: str) -> list[str]:
        return []


class _MissingGetRowCount:
    def get_sample_rows(self, table_name: str, sample_size: int) -> list[dict[str, str]]:
        return []

    def get_columns(self, table_name: str) -> list[str]:
        return []


class _MissingGetColumns:
    def get_row_count(self, table_name: str) -> int:
        return 0

    def get_sample_rows(self, table_name: str, sample_size: int) -> list[dict[str, str]]:
        return []


@pytest.mark.unit
def test_runtime_checkable_mock_is_instance() -> None:
    assert isinstance(_MockDataSource(), ProtocolDataSource)


@pytest.mark.unit
def test_missing_get_row_count_is_not_instance() -> None:
    assert not isinstance(_MissingGetRowCount(), ProtocolDataSource)


@pytest.mark.unit
def test_missing_get_columns_is_not_instance() -> None:
    assert not isinstance(_MissingGetColumns(), ProtocolDataSource)


@pytest.mark.unit
def test_empty_class_is_not_instance() -> None:
    class _Broken:
        pass

    assert not isinstance(_Broken(), ProtocolDataSource)


@pytest.mark.unit
def test_protocol_is_runtime_checkable() -> None:
    # Verifies @runtime_checkable is applied — isinstance must not raise TypeError
    try:
        isinstance(object(), ProtocolDataSource)
    except TypeError:
        pytest.fail("ProtocolDataSource is not @runtime_checkable")


@pytest.mark.unit
def test_protocol_class_name() -> None:
    assert ProtocolDataSource.__name__ == "ProtocolDataSource"


@pytest.mark.unit
def test_protocol_has_expected_methods() -> None:
    methods = {"get_row_count", "get_sample_rows", "get_columns"}
    for method in methods:
        assert hasattr(ProtocolDataSource, method), f"Missing method: {method}"
