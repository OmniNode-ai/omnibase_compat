# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Regression tests for bifrost backend config wire fields."""

from __future__ import annotations

import pytest

from omnibase_compat.contracts.delegation.wire import ModelDelegationBackendConfig


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_backend_config_accepts_overlay_resolved_optional_fields() -> None:
    backend = ModelDelegationBackendConfig(
        backend_id="local-coder",
        endpoint_url=None,
        model_name=None,
        tier="local",
    )

    assert backend.endpoint_url is None
    assert backend.model_name is None


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_backend_config_accepts_auth_and_static_headers() -> None:
    backend = ModelDelegationBackendConfig(
        backend_id="openrouter-glm-flash",
        endpoint_url="https://openrouter.ai/api/v1/chat/completions",
        model_name="thudm/glm-4-9b-chat:free",
        api_key_env="OPENROUTER_API_KEY",
        tier="cheap_cloud",
        extra_headers={
            "HTTP-Referer": "https://omninode.ai",
            "X-Title": "OmniNode ONEX Build Loop",
        },
    )

    assert backend.api_key_env == "OPENROUTER_API_KEY"
    assert backend.extra_headers == {
        "HTTP-Referer": "https://omninode.ai",
        "X-Title": "OmniNode ONEX Build Loop",
    }
