# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolGitHubClient(Protocol):
    """Protocol for GitHub write operations.

    Implementations wrap the GitHub API for PR management and commenting.
    """

    def create_pr(
        self,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ) -> dict[str, Any]: ...

    def merge_pr(
        self,
        repo: str,
        pr_number: int,
        method: str = "squash",
    ) -> bool: ...

    def list_prs(
        self,
        repo: str,
        state: str = "open",
    ) -> list[dict[str, Any]]: ...

    def add_comment(
        self,
        repo: str,
        pr_number: int,
        body: str,
    ) -> dict[str, Any]: ...

    def enable_auto_merge(
        self,
        repo: str,
        pr_number: int,
    ) -> bool: ...
