# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest

from omnibase_compat.protocols.protocol_github_client import ProtocolGitHubClient
from omnibase_compat.protocols.protocol_linear_client import ProtocolLinearClient


@pytest.mark.unit
def test_github_client_protocol_has_required_methods() -> None:
    required = {"create_pr", "merge_pr", "list_prs", "add_comment", "enable_auto_merge"}
    actual = {
        name
        for name in dir(ProtocolGitHubClient)
        if not name.startswith("_")
    }
    assert required.issubset(actual), f"Missing methods: {required - actual}"


@pytest.mark.unit
def test_linear_client_protocol_has_required_methods() -> None:
    required = {"create_issue", "update_issue", "list_issues", "add_comment", "get_issue"}
    actual = {
        name
        for name in dir(ProtocolLinearClient)
        if not name.startswith("_")
    }
    assert required.issubset(actual), f"Missing methods: {required - actual}"


@pytest.mark.unit
def test_github_client_protocol_is_runtime_checkable() -> None:
    assert hasattr(ProtocolGitHubClient, "__protocol_attrs__") or hasattr(
        ProtocolGitHubClient, "_is_runtime_protocol"
    )


@pytest.mark.unit
def test_linear_client_protocol_is_runtime_checkable() -> None:
    assert hasattr(ProtocolLinearClient, "__protocol_attrs__") or hasattr(
        ProtocolLinearClient, "_is_runtime_protocol"
    )
