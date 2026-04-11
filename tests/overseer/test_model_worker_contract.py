# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for ModelWorkerContract (OMN-8408)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.model_worker_contract import (
    ModelEvidenceRequirement,
    ModelWorkerContract,
    load_worker_contract,
)


class TestModelWorkerContractDefaults:
    def test_minimal_instance_uses_defaults(self) -> None:
        contract = ModelWorkerContract(worker_name="test-worker")

        assert contract.worker_name == "test-worker"
        assert contract.schema_version == "1.0.0"
        assert contract.heartbeat_interval_seconds == 300
        assert contract.stall_action == "kill_and_respawn"
        assert contract.required_evidence == {}
        assert contract.allowed_skills == "*"
        assert contract.allowed_tools == "*"
        assert contract.applicable_runbooks == ()
        assert contract.preflight_gates == ()
        assert contract.snapshot_on_tick is False
        assert contract.lease_seconds == 900

    def test_is_frozen(self) -> None:
        contract = ModelWorkerContract(worker_name="frozen-worker")
        with pytest.raises(ValidationError):
            contract.worker_name = "renamed"  # type: ignore[misc]


class TestModelWorkerContractValidation:
    def test_worker_name_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ModelWorkerContract()  # type: ignore[call-arg]
        assert "worker_name" in str(exc_info.value)

    def test_extra_fields_are_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ModelWorkerContract(
                worker_name="test",
                mystery_field="nope",  # type: ignore[call-arg]
            )
        assert "mystery_field" in str(exc_info.value) or "Extra" in str(exc_info.value)

    def test_heartbeat_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            ModelWorkerContract(worker_name="t", heartbeat_interval_seconds=0)
        with pytest.raises(ValidationError):
            ModelWorkerContract(worker_name="t", heartbeat_interval_seconds=-5)

    def test_lease_seconds_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            ModelWorkerContract(worker_name="t", lease_seconds=0)
        with pytest.raises(ValidationError):
            ModelWorkerContract(worker_name="t", lease_seconds=-1)

    def test_stall_action_enum_validates(self) -> None:
        for action in ("kill_and_respawn", "kill_only", "warn_only"):
            contract = ModelWorkerContract(worker_name="t", stall_action=action)  # type: ignore[arg-type]
            assert contract.stall_action == action

        with pytest.raises(ValidationError):
            ModelWorkerContract(worker_name="t", stall_action="explode")  # type: ignore[arg-type]

    def test_allowed_skills_accepts_wildcard_or_tuple(self) -> None:
        c1 = ModelWorkerContract(worker_name="w1", allowed_skills="*")
        assert c1.allowed_skills == "*"

        c2 = ModelWorkerContract(
            worker_name="w2", allowed_skills=("onex:ticket_pipeline", "onex:merge_sweep")
        )
        assert c2.allowed_skills == ("onex:ticket_pipeline", "onex:merge_sweep")

        c3 = ModelWorkerContract(worker_name="w3", allowed_skills=())
        assert c3.allowed_skills == ()

    def test_allowed_tools_accepts_wildcard_or_tuple(self) -> None:
        c1 = ModelWorkerContract(worker_name="w1", allowed_tools="*")
        assert c1.allowed_tools == "*"

        c2 = ModelWorkerContract(worker_name="w2", allowed_tools=("Bash", "Read", "Edit"))
        assert c2.allowed_tools == ("Bash", "Read", "Edit")


class TestModelEvidenceRequirement:
    def test_contains_kind(self) -> None:
        req = ModelEvidenceRequirement(
            evidence_id="pr-merged",
            description="PR view output must show MERGED state",
            kind="contains",
            pattern="MERGED",
        )
        assert req.kind == "contains"
        assert req.pattern == "MERGED"

    def test_regex_kind(self) -> None:
        req = ModelEvidenceRequirement(
            evidence_id="pytest-output",
            description="pytest output with passed count",
            kind="regex",
            pattern=r"\d+ passed",
        )
        assert req.kind == "regex"

    def test_fenced_block_kind(self) -> None:
        req = ModelEvidenceRequirement(
            evidence_id="json-block",
            description="JSON evidence block present",
            kind="fenced_block",
            pattern="json",
        )
        assert req.kind == "fenced_block"

    def test_invalid_kind_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ModelEvidenceRequirement(
                evidence_id="x",
                description="x",
                kind="bogus",  # type: ignore[arg-type]
                pattern="x",
            )

    def test_is_frozen(self) -> None:
        req = ModelEvidenceRequirement(
            evidence_id="x", description="x", kind="contains", pattern="x"
        )
        with pytest.raises(ValidationError):
            req.pattern = "y"  # type: ignore[misc]


class TestRequiredEvidenceMap:
    def test_evidence_map_populated(self) -> None:
        merged_req = ModelEvidenceRequirement(
            evidence_id="pr-merged",
            description="PR MERGED",
            kind="contains",
            pattern="MERGED",
        )
        contract = ModelWorkerContract(
            worker_name="merger",
            required_evidence={"completed": (merged_req,)},
        )
        assert "completed" in contract.required_evidence
        assert contract.required_evidence["completed"][0].evidence_id == "pr-merged"


class TestLoadWorkerContract:
    def test_loads_valid_mapping(self) -> None:
        data = {
            "worker_name": "pipeline-worker-1",
            "heartbeat_interval_seconds": 120,
            "stall_action": "kill_and_respawn",
            "allowed_skills": ["onex:ticket_pipeline"],
            "allowed_tools": ["Bash", "Edit", "Read", "Write", "Grep"],
            "applicable_runbooks": ["ci-failure-tests"],
            "preflight_gates": ["reality_check"],
            "snapshot_on_tick": True,
            "lease_seconds": 600,
        }
        contract = load_worker_contract(data)
        assert contract.worker_name == "pipeline-worker-1"
        assert contract.heartbeat_interval_seconds == 120
        assert contract.snapshot_on_tick is True
        assert contract.lease_seconds == 600
        assert contract.allowed_skills == ("onex:ticket_pipeline",)

    def test_rejects_non_mapping(self) -> None:
        with pytest.raises(TypeError):
            load_worker_contract(["not", "a", "dict"])  # type: ignore[arg-type]

    def test_rejects_none(self) -> None:
        with pytest.raises(TypeError):
            load_worker_contract(None)  # type: ignore[arg-type]

    def test_bubbles_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            load_worker_contract({"worker_name": "bad", "heartbeat_interval_seconds": -1})

    def test_rejects_unknown_fields(self) -> None:
        with pytest.raises(ValidationError):
            load_worker_contract({"worker_name": "bad", "undocumented": True})


class TestRoundTrip:
    def test_model_dump_and_revalidate(self) -> None:
        original = ModelWorkerContract(
            worker_name="round-trip",
            heartbeat_interval_seconds=60,
            stall_action="warn_only",
            allowed_skills=("onex:merge_sweep",),
            allowed_tools=("Bash",),
            applicable_runbooks=("merge-conflict",),
            preflight_gates=("branch_clean",),
            snapshot_on_tick=True,
            lease_seconds=1800,
            required_evidence={
                "completed": (
                    ModelEvidenceRequirement(
                        evidence_id="e1",
                        description="d",
                        kind="regex",
                        pattern=r"ok",
                    ),
                )
            },
        )
        dumped = original.model_dump()
        restored = ModelWorkerContract.model_validate(dumped)
        assert restored == original
