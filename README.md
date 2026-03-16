# omnibase_compat

Thin shared structural package for cross-repo enums, wire DTOs, event envelopes, and primitives. Zero upstream runtime dependencies.

[![CI](https://github.com/OmniNode-ai/omnibase_compat/actions/workflows/ci.yml/badge.svg)](https://github.com/OmniNode-ai/omnibase_compat/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)

## Install

```bash
uv add omnibase_compat
```

## Usage

```python
from omnibase_compat.enums.enum_message_category import EnumMessageCategory
from omnibase_compat.enums.enum_node_kind import EnumNodeKind
from omnibase_compat.models.event_envelope import EventEnvelopeV1Minimal
```

Import from explicit submodules — the package root `__all__` is not yet stable.

## Role vs `omnibase_spi`

| Layer | Purpose |
|-------|---------|
| `omnibase_spi` | Protocols and abstract interfaces that service implementations must satisfy |
| `omnibase_compat` | Shared enums, wire DTOs, event envelopes, structural types across repo boundaries |

**Rule of thumb**: protocols → `omnibase_spi`. Structural types → `omnibase_compat`.

## Key Features

- Zero dependency on `omnibase_core`, `omnibase_spi`, or `omnibase_infra` (CI-enforced)
- Experimental artifact registry with lifecycle governance (`ticket` + `review_milestone` required)
- Provenance-tracked enum seeding from upstream canonical sources
- Strict mypy + ruff + AST-based import validation

## Docs

- [CLAUDE.md](CLAUDE.md) — developer conventions and repo context
- [AGENT.md](AGENT.md) — LLM navigation guide

## License

See [LICENSE](LICENSE).
