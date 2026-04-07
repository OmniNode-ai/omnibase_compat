# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolIdempotencyStore(Protocol):
    """Protocol shim for idempotency store adapters.

    Implementations live in omnibase_infra or downstream repos.
    This protocol defines the structural contract only.
    """

    def store_result(
        self,
        key: str,
        result: Any,
        ttl_seconds: int | None = None,
    ) -> None: ...

    def get_result(self, key: str) -> Any | None: ...

    def is_duplicate(self, key: str) -> bool: ...
