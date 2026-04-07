# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProtocolLinearClient(Protocol):
    """Protocol for Linear issue-tracking write operations.

    Implementations wrap the Linear GraphQL API for issue management.
    """

    def create_issue(
        self,
        title: str,
        description: str,
        team_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    def update_issue(
        self,
        issue_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    def list_issues(
        self,
        team_id: str,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]: ...

    def add_comment(
        self,
        issue_id: str,
        body: str,
    ) -> dict[str, Any]: ...

    def get_issue(
        self,
        issue_id: str,
    ) -> dict[str, Any]: ...
