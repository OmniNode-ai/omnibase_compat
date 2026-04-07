# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolProjectionDatabase(Protocol):
    """Protocol shim for projection database adapters.

    Implementations live in omnibase_infra or downstream repos.
    This protocol defines the structural contract only.
    """

    def upsert(
        self,
        table: str,
        data: dict[str, Any],
        conflict_keys: list[str],
    ) -> None: ...

    def query(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]: ...

    def schema_version(self, table: str) -> str: ...
