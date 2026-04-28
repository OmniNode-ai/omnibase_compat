# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_infra.adapters.adapter_project_tracker_linear
# COMPAT_REMOVAL_DATE: 2026-09-01

from __future__ import annotations

import json
import urllib.request

from omnibase_compat.models.model_project_tracker import (
    ModelIssueStatus,
    ModelLabel,
    ModelTeam,
)
from omnibase_compat.protocols.protocol_project_tracker import ProtocolProjectTracker

_LINEAR_API_URL = "https://api.linear.app/graphql"


class AdapterProjectTrackerLinear(ProtocolProjectTracker):
    def __init__(self, api_key: str, *, base_url: str = _LINEAR_API_URL) -> None:
        self._api_key = api_key
        self._base_url = base_url

    def _graphql(self, query: str, variables: dict[str, object] | None = None) -> dict[str, object]:
        body: dict[str, object] = {"query": query}
        if variables is not None:
            body["variables"] = variables
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            self._base_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self._api_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def list_teams(self) -> list[ModelTeam]:
        result = self._graphql(
            """query {
                teams { nodes { id name key } }
            }"""
        )
        nodes = _extract_nodes(result, "teams")
        return [ModelTeam(**n) for n in nodes]

    def list_issue_labels(self, team: str) -> list[ModelLabel]:
        result = self._graphql(
            """query ($filter: IssueLabelFilter!) {
                issueLabels(filter: $filter) {
                    nodes { id name color team { id } }
                }
            }""",
            {"filter": {"team": {"key": {"eq": team}}}},
        )
        nodes = _extract_nodes(result, "issueLabels")
        out: list[ModelLabel] = []
        for n in nodes:
            tid = n.pop("team", {}).get("id") if isinstance(n.get("team"), dict) else None
            out.append(ModelLabel(**n, team_id=tid))
        return out

    def list_issue_statuses(self, team: str) -> list[ModelIssueStatus]:
        result = self._graphql(
            """query ($filter: WorkflowStateFilter!) {
                workflowStates(filter: $filter) {
                    nodes { id name type team { id } }
                }
            }""",
            {"filter": {"team": {"key": {"eq": team}}}},
        )
        nodes = _extract_nodes(result, "workflowStates")
        out: list[ModelIssueStatus] = []
        for n in nodes:
            tid = n.pop("team", {}).get("id") if isinstance(n.get("team"), dict) else None
            out.append(ModelIssueStatus(**n, team_id=tid))
        return out


def _extract_nodes(payload: dict[str, object], root_key: str) -> list[dict[str, object]]:
    data = payload.get("data")
    if not isinstance(data, dict):
        raise ValueError(f"Unexpected Linear response: {payload}")
    root = data.get(root_key)
    if not isinstance(root, dict):
        raise ValueError(f"Missing '{root_key}' in Linear response: {data}")
    nodes = root.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError(f"Missing 'nodes' under '{root_key}': {root}")
    return nodes


__all__: list[str] = [
    "AdapterProjectTrackerLinear",
]
