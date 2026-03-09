# omnibase_compat

Thin shared structural package for cross-repo enums, wire DTOs, event envelopes, primitives, and experimental schemas. Zero upstream runtime dependencies — only `pydantic` and `stdlib`.

---

## Package Purpose

`omnibase_compat` provides structural compatibility artifacts that are shared across multiple OmniNode repositories. It intentionally has zero `omnibase_core` dependency to decouple fast schema iteration and cloud env fixes from the full core release chain. All artifacts here are either stable shared types with clear provenance, or experimental schemas with explicit lifecycle governance.

---

## Role vs `omnibase_spi`

| Layer | Purpose |
|-------|---------|
| `omnibase_spi` | Implementation-facing service/provider interfaces, runtime integration protocols, abstract base contracts for concrete implementations |
| `omnibase_compat` | Shared enums, wire DTOs, event envelopes, primitives, experimental schemas, transitional cross-repo structural artifacts |

**Rule of thumb**: If it's a _protocol_ or _abstract interface_ that a service implementation must satisfy, it belongs in `omnibase_spi`. If it's a _structural type_ shared across repo boundaries (enum values, wire format, event envelope), it belongs here.

---

## Migration Policy

For cross-repo structural artifacts, `omnibase_compat` is the default import surface.

**Key rule**: New shared enums, wire DTOs, and transport-facing structural models should not be added to `omnibase_core` without documented justification and review. `omnibase_core` is for runtime-coupled models with business logic. `omnibase_compat` is for pure structural contracts.

When seeding a new enum here from an upstream canonical source:
1. Add a provenance comment header with source file, version, and git commit
2. Copy values exactly — no renames, no normalization
3. Strip helper methods that have upstream dependencies
4. Document the source in the class docstring

---

## What Does NOT Belong Here

Explicitly excluded from `omnibase_compat`:

- Domain-specific runtime models (e.g., `ModelHandlerOutput`, `ModelONEXContainer`)
- Persistence logic (database models, ORM types)
- Service orchestration (workflow coordination, FSM transitions)
- Convenience helpers (topic routing, format conversion)
- Service wrappers (Kafka clients, database clients)
- Implementation-facing adapters (anything that depends on `omnibase_infra`)

If it needs `omnibase_core` or any infra package to function, it does not belong here.

---

## Experimental Lane

Register experimental schemas with explicit lifecycle governance:

```python
from omnibase_compat.experimental._registry import register_experimental, get_experimental_artifacts
from omnibase_compat.metadata.artifact_status import ArtifactStatus

# Register a new experimental artifact
register_experimental(
    name="NewEventFormatV2",
    status=ArtifactStatus.experimental,
    ticket="OMN-9001",         # Required — must be non-empty
    review_milestone="v0.3",   # Required — when to review/promote/retire
)

# List all registered experimental artifacts
artifacts = get_experimental_artifacts()
print(artifacts["NewEventFormatV2"])
# {'status': 'experimental', 'ticket': 'OMN-9001', 'review_milestone': 'v0.3'}
```

Experimental artifacts without a ticket or milestone will raise `ValueError` at registration time. This enforces governance before code review.

---

## Import Surface Rule

Until the API stabilizes, import from explicit submodules rather than the package root:

```python
# Preferred — explicit submodule imports
from omnibase_compat.enums.enum_message_category import EnumMessageCategory
from omnibase_compat.enums.enum_node_kind import EnumNodeKind
from omnibase_compat.enums.enum_execution_status import EnumExecutionStatus
from omnibase_compat.models.event_envelope import EventEnvelopeV1Minimal
from omnibase_compat.metadata.artifact_status import ArtifactStatus
from omnibase_compat.metadata.transitional import TransitionalMeta

# Avoid until a stable __all__ is published at package root
from omnibase_compat import EnumMessageCategory  # not yet stable
```

---

## CI

All PRs run:

1. `validate_no_upstream_deps.py` — AST-based scan; exits 1 if any `omnibase_core`, `omnibase_spi`, or `omnibase_infra` import is found
2. `ruff check src/` — linting
3. `mypy src/omnibase_compat --strict` — type checking
4. `pytest -m unit` — unit tests
5. `uv build && uv pip install dist/*.whl` — build and install verification
