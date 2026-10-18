# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.models.model_runner_fleet_observation_wire
# COMPAT_REMOVAL_DATE: 2027-01-31

"""Wire shape of one fleet observation cycle."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from omnibase_compat.models.model_runner_observation_wire import (
    ModelRunnerObservationWire,
)


class ModelRunnerFleetObservationWire(BaseModel):
    """The whole fleet, as of one monitor cycle.

    One message per cycle, not per runner. That is what makes the ABSENCE of a
    runner meaningful: a runner this host reported last cycle and does not
    report now has been deregistered. Per-runner messages could never state
    that, because a runner that stopped being published would be
    indistinguishable from one whose message was lost.
    """

    model_config = ConfigDict(frozen=True, extra="ignore")

    schema_version: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    host: str = Field(min_length=1)
    observed_at: datetime
    runners: tuple[ModelRunnerObservationWire, ...] = ()
