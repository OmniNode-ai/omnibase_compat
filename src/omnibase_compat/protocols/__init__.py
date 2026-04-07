# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.protocols — cross-repo protocol shims."""

from omnibase_compat.protocols.protocol_data_source import ProtocolDataSource
from omnibase_compat.protocols.protocol_docker_client import ProtocolDockerClient
from omnibase_compat.protocols.protocol_health_check import ProtocolHealthCheck
from omnibase_compat.protocols.protocol_idempotency_store import ProtocolIdempotencyStore
from omnibase_compat.protocols.protocol_projection_database import ProtocolProjectionDatabase

__all__: list[str] = [
    "ProtocolDataSource",
    "ProtocolDockerClient",
    "ProtocolHealthCheck",
    "ProtocolIdempotencyStore",
    "ProtocolProjectionDatabase",
]
