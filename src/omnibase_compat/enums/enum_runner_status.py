# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.enums.enum_runner_status
# COMPAT_REMOVAL_DATE: 2027-01-31

"""The three states a self-hosted runner can be in at an observation."""

from __future__ import annotations

from enum import StrEnum


class EnumRunnerStatus(StrEnum):
    """A runner is exactly one of these at an observation.

    ``BUSY`` is a state of its own rather than a flag on ``ONLINE``: folding it
    in makes "the fleet is saturated" indistinguishable from "the fleet is
    idle", which is the question a capacity panel exists to answer.

    There is deliberately no ``UNKNOWN``. An observation that could not read the
    fleet is not published at all: the emitter refuses rather than emitting a
    fleet of unknowns.
    """

    ONLINE = "online"
    BUSY = "busy"
    OFFLINE = "offline"
