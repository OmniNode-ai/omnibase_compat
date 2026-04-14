# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for ProtocolProjectionDatabaseSync (sync adapter protocol)."""

from __future__ import annotations

import pytest

from omnibase_compat.protocols.protocol_projection_database_sync import (
    ProtocolProjectionDatabaseSync,
)


class _MockSyncAdapter:
    def upsert(self, table: str, conflict_key: str, row: dict[str, object]) -> bool:
        return True

    def query(
        self,
        table: str,
        filters: dict[str, object] | None = None,
    ) -> list[dict[str, object]]:
        return []


class _MissingUpsert:
    def query(
        self,
        table: str,
        filters: dict[str, object] | None = None,
    ) -> list[dict[str, object]]:
        return []


class _MissingQuery:
    def upsert(self, table: str, conflict_key: str, row: dict[str, object]) -> bool:
        return True


@pytest.mark.unit
def test_runtime_checkable_mock_is_instance() -> None:
    assert isinstance(_MockSyncAdapter(), ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_missing_upsert_is_not_instance() -> None:
    assert not isinstance(_MissingUpsert(), ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_missing_query_is_not_instance() -> None:
    assert not isinstance(_MissingQuery(), ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_empty_class_is_not_instance() -> None:
    class _Broken:
        pass

    assert not isinstance(_Broken(), ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_protocol_is_runtime_checkable() -> None:
    try:
        isinstance(object(), ProtocolProjectionDatabaseSync)
    except TypeError:
        pytest.fail("ProtocolProjectionDatabaseSync is not @runtime_checkable")


@pytest.mark.unit
def test_protocol_class_name() -> None:
    assert ProtocolProjectionDatabaseSync.__name__ == "ProtocolProjectionDatabaseSync"


@pytest.mark.unit
def test_protocol_has_expected_methods() -> None:
    methods = {"upsert", "query"}
    for method in methods:
        assert hasattr(ProtocolProjectionDatabaseSync, method), f"Missing method: {method}"
