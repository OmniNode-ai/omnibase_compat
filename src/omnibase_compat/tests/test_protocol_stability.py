# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest

from omnibase_compat.protocols.protocol_data_source import ProtocolDataSource
from omnibase_compat.protocols.protocol_docker_client import ProtocolDockerClient
from omnibase_compat.protocols.protocol_health_check import ProtocolHealthCheck
from omnibase_compat.protocols.protocol_idempotency_store import (
    ProtocolIdempotencyStore,
)
from omnibase_compat.protocols.protocol_projection_database import (
    ProtocolProjectionDatabase,
)


@pytest.mark.unit
def test_projection_database_protocol_is_runtime_checkable() -> None:
    assert hasattr(ProtocolProjectionDatabase, "__protocol_attrs__") or hasattr(
        ProtocolProjectionDatabase, "__abstractmethods__"
    )
    methods = {"upsert", "query", "schema_version"}
    actual = {
        name
        for name in dir(ProtocolProjectionDatabase)
        if not name.startswith("_") and callable(getattr(ProtocolProjectionDatabase, name, None))
    }
    assert methods.issubset(actual), f"Missing methods: {methods - actual}"


@pytest.mark.unit
def test_idempotency_store_protocol_is_runtime_checkable() -> None:
    methods = {"store_result", "get_result", "is_duplicate"}
    actual = {
        name
        for name in dir(ProtocolIdempotencyStore)
        if not name.startswith("_") and callable(getattr(ProtocolIdempotencyStore, name, None))
    }
    assert methods.issubset(actual), f"Missing methods: {methods - actual}"


@pytest.mark.unit
def test_docker_client_protocol_is_runtime_checkable() -> None:
    methods = {"pull", "run", "stop", "logs", "health"}
    actual = {
        name
        for name in dir(ProtocolDockerClient)
        if not name.startswith("_") and callable(getattr(ProtocolDockerClient, name, None))
    }
    assert methods.issubset(actual), f"Missing methods: {methods - actual}"


@pytest.mark.unit
def test_health_check_protocol_is_runtime_checkable() -> None:
    methods = {"check"}
    actual = {
        name
        for name in dir(ProtocolHealthCheck)
        if not name.startswith("_") and callable(getattr(ProtocolHealthCheck, name, None))
    }
    assert methods.issubset(actual), f"Missing methods: {methods - actual}"


@pytest.mark.unit
def test_data_source_protocol_is_runtime_checkable() -> None:
    methods = {"fetch", "query"}
    actual = {
        name
        for name in dir(ProtocolDataSource)
        if not name.startswith("_") and callable(getattr(ProtocolDataSource, name, None))
    }
    assert methods.issubset(actual), f"Missing methods: {methods - actual}"


@pytest.mark.unit
@pytest.mark.parametrize(
    "protocol_cls",
    [
        ProtocolProjectionDatabase,
        ProtocolIdempotencyStore,
        ProtocolDockerClient,
        ProtocolHealthCheck,
        ProtocolDataSource,
    ],
)
def test_protocols_are_runtime_checkable(protocol_cls: type) -> None:
    """All protocol shims must be @runtime_checkable for isinstance() checks."""
    assert getattr(protocol_cls, "_is_runtime_protocol", False), (
        f"{protocol_cls.__name__} is not @runtime_checkable"
    )
