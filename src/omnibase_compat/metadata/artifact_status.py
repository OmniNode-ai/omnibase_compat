# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

from enum import StrEnum


class ArtifactStatus(StrEnum):
    experimental = "experimental"
    candidate = "candidate"
    stable = "stable"
    deprecated = "deprecated"
    retired = "retired"
