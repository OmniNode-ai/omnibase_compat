# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from omnibase_compat.enums.enum_runner_status import EnumRunnerStatus
from omnibase_compat.models import (
    ModelRunnerFleetObservationWire,
    ModelRunnerObservationWire,
)

_SRC = Path(__file__).resolve().parents[2] / "src" / "omnibase_compat"


def _runner(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "runner_name": "runner-1",
        "runner_id": 7,
        "label_class": "lab",
        "labels": ["self-hosted", "host-h201"],
        "host": "h201",
        "status": "busy",
        "current_job_id": "job-9",
        "observed_at": "2026-10-18T10:00:00Z",
    }
    base.update(overrides)
    return base


def _fleet(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "schema_version": "1",
        "event_type": "runner-fleet.observed",
        "host": "h201",
        "observed_at": "2026-10-18T10:00:00Z",
        "runners": [_runner()],
    }
    base.update(overrides)
    return base


@pytest.mark.unit
@pytest.mark.timeout(30)
class TestRunnerFleetObservationWire:
    def test_accepts_a_fleet_observation(self) -> None:
        fleet = ModelRunnerFleetObservationWire.model_validate(_fleet())
        assert fleet.runners[0].status is EnumRunnerStatus.BUSY
        assert fleet.runners[0].labels == ("self-hosted", "host-h201")

    def test_absent_runners_is_an_empty_fleet(self) -> None:
        payload = _fleet()
        del payload["runners"]
        assert ModelRunnerFleetObservationWire.model_validate(payload).runners == ()

    def test_unknown_fields_are_ignored(self) -> None:
        payload = _fleet(emitter_note="added later", runners=[_runner(extra_field=1)])
        fleet = ModelRunnerFleetObservationWire.model_validate(payload)
        assert not hasattr(fleet, "emitter_note")
        assert not hasattr(fleet.runners[0], "extra_field")

    def test_optional_runner_fields_default_to_none(self) -> None:
        payload = _runner()
        del payload["runner_id"]
        del payload["current_job_id"]
        runner = ModelRunnerObservationWire.model_validate(payload)
        assert runner.runner_id is None
        assert runner.current_job_id is None
        assert runner.observing_host is None

    @pytest.mark.parametrize("status", ["unknown", "", "ONLINE", None])
    def test_status_outside_the_three_states_is_refused(self, status: object) -> None:
        with pytest.raises(ValidationError):
            ModelRunnerObservationWire.model_validate(_runner(status=status))

    @pytest.mark.parametrize("status", ["online", "busy", "offline"])
    def test_each_of_the_three_states_is_accepted(self, status: str) -> None:
        runner = ModelRunnerObservationWire.model_validate(_runner(status=status))
        assert runner.status.value == status

    @pytest.mark.parametrize("field", ["runner_name", "label_class", "host"])
    def test_empty_required_runner_strings_are_refused(self, field: str) -> None:
        with pytest.raises(ValidationError):
            ModelRunnerObservationWire.model_validate(_runner(**{field: ""}))

    @pytest.mark.parametrize("field", ["schema_version", "event_type", "host"])
    def test_empty_required_fleet_strings_are_refused(self, field: str) -> None:
        with pytest.raises(ValidationError):
            ModelRunnerFleetObservationWire.model_validate(_fleet(**{field: ""}))

    def test_missing_observed_at_is_refused(self) -> None:
        payload = _fleet()
        del payload["observed_at"]
        with pytest.raises(ValidationError):
            ModelRunnerFleetObservationWire.model_validate(payload)

    def test_a_malformed_runner_refuses_the_whole_observation(self) -> None:
        with pytest.raises(ValidationError):
            ModelRunnerFleetObservationWire.model_validate(
                _fleet(runners=[_runner(), _runner(status="unknown")])
            )

    def test_models_are_frozen(self) -> None:
        fleet = ModelRunnerFleetObservationWire.model_validate(_fleet())
        field = "host"
        with pytest.raises(ValidationError):
            setattr(fleet, field, "other")

    @pytest.mark.parametrize(
        "relative",
        [
            "enums/enum_runner_status.py",
            "models/model_runner_observation_wire.py",
            "models/model_runner_fleet_observation_wire.py",
        ],
    )
    def test_module_declares_its_retention(self, relative: str) -> None:
        head = (_SRC / relative).read_text(encoding="utf-8").splitlines()[:10]
        text = "\n".join(head)
        assert "COMPAT_MIGRATION_TARGET:" in text
        assert "COMPAT_REMOVAL_DATE:" in text
