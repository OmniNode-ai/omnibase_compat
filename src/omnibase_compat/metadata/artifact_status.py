from enum import StrEnum


class ArtifactStatus(StrEnum):
    experimental = "experimental"
    candidate = "candidate"
    stable = "stable"
    deprecated = "deprecated"
    retired = "retired"
