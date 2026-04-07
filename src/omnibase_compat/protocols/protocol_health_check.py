# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolHealthCheck(Protocol):
    """Protocol shim for health check adapters.

    Implementations live in omnibase_infra or downstream repos.
    This protocol defines the structural contract only.
    """

    def check(self, target: str, timeout_ms: int = 5000) -> dict[str, Any]: ...
