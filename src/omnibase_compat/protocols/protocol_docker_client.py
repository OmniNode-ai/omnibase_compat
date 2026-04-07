# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolDockerClient(Protocol):
    """Protocol shim for Docker client adapters.

    Implementations live in omnibase_infra or downstream repos.
    This protocol defines the structural contract only.
    """

    def pull(self, image: str, tag: str = "latest") -> None: ...

    def run(
        self,
        image: str,
        tag: str = "latest",
        env: dict[str, str] | None = None,
    ) -> str: ...

    def stop(self, container_id: str) -> None: ...

    def logs(self, container_id: str, tail: int = 100) -> str: ...

    def health(self, container_id: str) -> dict[str, Any]: ...
