# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolHealthCheck(Protocol):
    """Protocol for health check targets.

    Matches the CheckTarget interface used by omnimarket's process
    watchdog node. Each implementation represents a single checkable
    component (HTTP endpoint, socket, Docker container, etc.).
    """

    @property
    def name(self) -> str:
        """Unique identifier for this check target."""
        ...

    @property
    def category(self) -> Any:
        """Category enum value for this target (e.g. EnumCheckTarget)."""
        ...

    def check(self) -> Any:
        """Execute the health check and return a structured result."""
        ...

    def restart(self) -> bool:
        """Attempt to restart the target. Returns True if restart succeeded."""
        ...
