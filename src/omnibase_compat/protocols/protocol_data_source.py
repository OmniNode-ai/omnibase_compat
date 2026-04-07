# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolDataSource(Protocol):
    """Protocol shim for data source adapters.

    Implementations live in omnibase_infra or downstream repos.
    This protocol defines the structural contract only.
    """

    def fetch(
        self,
        resource: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]: ...

    def query(self, expression: str) -> list[dict[str, Any]]: ...
