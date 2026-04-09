# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.overseer.enum_context_bundle_level import EnumContextBundleLevel
from omnibase_compat.overseer.model_context_bundle import (
    ModelContextBundleL0,
    ModelContextBundleL1,
    ModelContextBundleL2,
    ModelContextBundleL3,
    ModelContextBundleL4,
)

# --- Shared fixtures ---

L0_KWARGS = {
    "run_id": "run-001",
    "task_id": "task-abc",
    "role": "implementer",
    "fsm_state": "working",
}

L1_KWARGS = {
    **L0_KWARGS,
    "ticket_id": "OMN-1234",
    "summary": "Implement feature X",
}

L2_KWARGS = {
    **L1_KWARGS,
    "entrypoints": ["src/foo.py:42", "src/bar.py:10"],
    "file_scope": ["src/foo.py", "src/bar.py"],
}

L3_KWARGS = {
    **L2_KWARGS,
    "decisions": ["Use Kafka for async comms"],
    "history": ["Previous attempt failed due to timeout"],
}

L4_KWARGS = {
    **L3_KWARGS,
    "dependency_graph": {"task-abc": ["task-def", "task-ghi"]},
    "raw_context": {"extra_key": "extra_value"},
}


# --- test_l0_bundle_minimal_fields ---


@pytest.mark.unit
def test_l0_bundle_minimal_fields() -> None:
    bundle = ModelContextBundleL0.model_validate(L0_KWARGS)
    assert bundle.run_id == "run-001"
    assert bundle.task_id == "task-abc"
    assert bundle.role == "implementer"
    assert bundle.fsm_state == "working"
    assert bundle.level == EnumContextBundleLevel.L0


@pytest.mark.unit
def test_l0_rejects_missing_required() -> None:
    with pytest.raises(ValidationError):
        ModelContextBundleL0.model_validate({"run_id": "run-001"})


# --- test_l4_bundle_includes_all_levels ---


@pytest.mark.unit
def test_l4_bundle_includes_all_levels() -> None:
    bundle = ModelContextBundleL4.model_validate(L4_KWARGS)
    # L0 fields
    assert bundle.run_id == "run-001"
    assert bundle.task_id == "task-abc"
    assert bundle.role == "implementer"
    assert bundle.fsm_state == "working"
    # L1 fields
    assert bundle.ticket_id == "OMN-1234"
    assert bundle.summary == "Implement feature X"
    # L2 fields
    assert bundle.entrypoints == ["src/foo.py:42", "src/bar.py:10"]
    assert bundle.file_scope == ["src/foo.py", "src/bar.py"]
    # L3 fields
    assert bundle.decisions == ["Use Kafka for async comms"]
    assert bundle.history == ["Previous attempt failed due to timeout"]
    # L4 fields
    assert bundle.dependency_graph == {"task-abc": ["task-def", "task-ghi"]}
    assert bundle.raw_context == {"extra_key": "extra_value"}
    # Level marker
    assert bundle.level == EnumContextBundleLevel.L4


# --- test_context_bundle_level_invariant ---


@pytest.mark.unit
def test_context_bundle_level_invariant_l2_requires_l1_fields() -> None:
    """L2 bundle cannot be created without L1 fields (ticket_id, summary)."""
    with pytest.raises(ValidationError):
        ModelContextBundleL2.model_validate(
            {
                "run_id": "run-001",
                "task_id": "task-abc",
                "role": "implementer",
                "fsm_state": "working",
                "entrypoints": ["src/foo.py"],
                # missing ticket_id and summary (L1 fields)
            }
        )


@pytest.mark.unit
def test_context_bundle_level_invariant_l3_requires_l2_fields() -> None:
    """L3 bundle cannot be created without L2 fields (entrypoints)."""
    with pytest.raises(ValidationError):
        ModelContextBundleL3.model_validate(
            {**L1_KWARGS, "decisions": ["some decision"]}
            # missing entrypoints (L2 field)
        )


# --- test_bundle_frozen ---


@pytest.mark.unit
def test_bundle_frozen() -> None:
    """All bundle levels are immutable."""
    bundle_l0 = ModelContextBundleL0.model_validate(L0_KWARGS)
    with pytest.raises(ValidationError):
        bundle_l0.run_id = "changed"  # type: ignore[misc]

    bundle_l4 = ModelContextBundleL4.model_validate(L4_KWARGS)
    with pytest.raises(ValidationError):
        bundle_l4.ticket_id = "changed"  # type: ignore[misc]


# --- extra=forbid ---


@pytest.mark.unit
def test_bundle_forbids_extra_fields() -> None:
    with pytest.raises(ValidationError):
        ModelContextBundleL0.model_validate({**L0_KWARGS, "unknown_field": "bad"})


# --- default level markers ---


@pytest.mark.unit
def test_default_level_markers() -> None:
    assert ModelContextBundleL0.model_validate(L0_KWARGS).level == EnumContextBundleLevel.L0
    assert ModelContextBundleL1.model_validate(L1_KWARGS).level == EnumContextBundleLevel.L1
    assert ModelContextBundleL2.model_validate(L2_KWARGS).level == EnumContextBundleLevel.L2
    assert ModelContextBundleL3.model_validate(L3_KWARGS).level == EnumContextBundleLevel.L3
    assert ModelContextBundleL4.model_validate(L4_KWARGS).level == EnumContextBundleLevel.L4


# --- Pydantic serialization round-trip ---


@pytest.mark.unit
def test_l4_serialization_round_trip() -> None:
    bundle = ModelContextBundleL4.model_validate(L4_KWARGS)
    data = bundle.model_dump()
    restored = ModelContextBundleL4.model_validate(data)
    assert restored == bundle
