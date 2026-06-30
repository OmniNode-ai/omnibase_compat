# omnibase_compat Documentation

**Owner:** `omnibase_compat`
**Last verified:** 2026-06-21
**Verification:** docs refresh (verified against code on this refresh)

This is the canonical docs map for `omnibase_compat`.

## Start Here

- [Root README](../README.md) - repo role, install, dependency boundary, common workflows, and docs map.
- [Release workflow](runbooks/release.md) - stable release runbook promoted from the dated release workflow plan.
- [CLAUDE.md](../CLAUDE.md) - local agent/developer rules.

## Current Architecture

`omnibase_compat` is a structural compatibility package. It owns values and
wire shapes that must cross repo boundaries without importing OmniNode runtime
packages.

The core dependency rule is:

```text
Allowed runtime deps: pydantic, typing-extensions, Python standard library
Forbidden runtime deps: omnibase_core, omnibase_spi, omnibase_infra
```

`omnibase_compat` differs from `omnibase_spi` by owning data shapes, not
implementation contracts. If a consumer needs a protocol that an implementation
must satisfy, the owner is `omnibase_spi`. If a consumer needs a stable enum,
event envelope, DTO, or primitive shared across repos, the owner is
`omnibase_compat`.

## Structural Types

Current structural surfaces live under `src/omnibase_compat/`:

- `models/` - `event_envelope.py` (`EventEnvelopeV1Minimal`) and `model_project_tracker.py` (`ModelTeam`, `ModelLabel`, `ModelIssueStatus`).
- `routing/` - routing policy and degraded-routing event DTOs (`model_routing_policy.py`, `model_routing_degraded_event.py`).
- `telemetry/` - sweep result DTO (`model_sweep_result.py`, `ModelSweepResult`).
- `overseer/` - routing decision model (`model_routing_decision.py`, `ModelRoutingDecision` plus tier/provider/retry/risk enums) and agent scope presets (`model_agent_scope_presets.py`).
- `registration/` - idempotent registration helper (`decorator_idempotent_register.py`) and optional-injectable decorator (`decorator_injectable_optional.py`).
- `concurrency/` - synchronous coroutine bridge utility (`util_run_coro_sync.py`).
- `env/` - strict-mode environment helper (`util_is_strict_mode.py`).
- `adapters/` - protocol adapters (`adapter_project_tracker_linear.py`).
- `metadata/` - artifact status and transitional metadata models (`artifact_status.py`, `transitional.py`).
- `protocols/` - cross-repo protocol definitions: `protocol_project_tracker.py`, `protocol_projection_database.py`, `protocol_projection_database_sync.py`.
- `tooling/` - TTL check shim (`shim_ttl_check.py`).

The `types/` and `primitives/` subpackages currently hold only their `__init__.py`
placeholders; no JSON typing or primitive modules are present.

### contracts/ Sub-modules

Domain-specific wire DTOs live under `src/omnibase_compat/contracts/`:

- `contracts/delegation/` - delegation runtime profile, LLM backend config, datastore, event bus endpoint, projection API, security, and secret reference wire models.
- `contracts/evidence/` - contract evidence proof, spec, and provenance models.
- `contracts/evidence_pipeline/wire/` - evidence pipeline wire DTOs: dashboard events, pipeline commands, evidence bundles, correlation traces, gap reports, OCC PR references, raw payloads, readiness aggregates, topic constants, and wire types.
- `contracts/pricing/` - LLM pricing and pricing contract models.
- `contracts/runtime_deployment/wire/` - runtime deployment proof, request, and type wire models.

Note: `contracts/delegation/wire/` (the old shim module) was deleted in PR #132. Import from `contracts/delegation/` directly.

Every class-like compatibility artifact must either carry retention metadata or
an explicit retention exemption:

```python
# COMPAT_MIGRATION_TARGET: canonical.repo.module
# COMPAT_REMOVAL_DATE: YYYY-MM-DD
```

## Enums

Enums live under `src/omnibase_compat/enums/`:

- `EnumExecutionStatus`
- `EnumMessageCategory`
- `EnumNodeKind`

Enum copies are intentionally minimal. They carry source provenance comments and
must not copy helper behavior that belongs in `omnibase_core`.

## Event Envelope

`EventEnvelopeV1Minimal` lives in
`src/omnibase_compat/models/event_envelope.py`.

It is intentionally narrow:

- `event_id`
- `event_type`
- `payload`
- `schema_version`
- `data_provenance` (optional provenance label)

Do not add runtime tracing, source, timestamp, or helper behavior without a
versioned compatibility decision and downstream consumer evidence.

## Artifact Registry

Experimental artifacts use `src/omnibase_compat/experimental/_registry.py`.

Each registered artifact must include:

- `name`
- `status`
- `ticket`
- `review_milestone`

The registry is local scaffolding for governance visibility. If artifacts need
cross-environment discoverability, promote the registry to file-backed or
CI-enforced metadata in a separate change.

## Validation Scripts

Scripts under `scripts/` enforce the zero-upstream-dependency and structural invariants:

- `scripts/validate_no_upstream_deps.py` - AST scan of `src/` for import statements referencing forbidden upstream packages.
- `scripts/check_compat_retention.py` - enforces `COMPAT_MIGRATION_TARGET` and `COMPAT_REMOVAL_DATE` retention comments on all class-bearing modules.
- `scripts/check_no_infra_edge.py` - closure scan of `pyproject.toml` and `uv.lock` for any `omnibase_infra`, `omnibase_core`, or `omnibase_spi` edge; wired as a pre-commit hook.
- `scripts/ci/` - CI tooling: change-aware test path detection (`detect_test_paths.py`), test selection models and adjacency configuration.

## Reference

- [Package source](../src/omnibase_compat/)
- [No-upstream-dependency validator](../scripts/validate_no_upstream_deps.py)
- [No-infra-edge closure guard](../scripts/check_no_infra_edge.py)
- [Compat retention validator](../scripts/check_compat_retention.py)
- [Release workflow](../.github/workflows/release.yml)
- [Release dry run workflow](../.github/workflows/release-dry-run.yml)
- [Contract files](../contracts/)

## Runbooks

- [Release workflow](runbooks/release.md)

## Migrations

Migration truth is embedded in module-level retention metadata:

- `COMPAT_MIGRATION_TARGET`
- `COMPAT_REMOVAL_DATE`

Do not use a dated plan as the primary migration source unless it has been
promoted into a stable migration doc.

## Decisions

Current decisions are reflected in:

- The root README dependency boundary.
- This docs index.
- `CLAUDE.md` retention policy.
- The AST validator in `scripts/validate_no_upstream_deps.py`.

Add ADRs under `docs/decisions/` only when a new compatibility policy affects
multiple repos or changes the allowed dependency shape.

## Testing And Validation

Run the repo validation path before changing public compatibility surfaces:

```bash
uv sync --dev --frozen
uv run python scripts/validate_no_upstream_deps.py
uv run python scripts/check_no_infra_edge.py
uv run python scripts/check_compat_retention.py
uv run ruff check src/
uv run mypy src/omnibase_compat --strict
uv run pytest -m unit --tb=short
uv build
```

`pyproject.toml` lists both `src/omnibase_compat/tests` and the root `tests/`
directory in `testpaths`. Both are exercised by `uv run pytest`. The root
`tests/` directory holds `test_overseer_exports.py` (integration export check),
`tests/unit/` (event-envelope provenance, no-infra-edge, plus nested
`contracts/` and `protocols/` wire tests), and `tests/experimental/`.

Docs validation must not add an OmniNode runtime dependency. If link validation
is needed before a standalone local entrypoint exists here, run it as CI-only
tooling or from the repo that owns the validator.

## Historical Context

- [Release workflow plan](plans/release-workflow.md) - source plan for the stable [release runbook](runbooks/release.md).

