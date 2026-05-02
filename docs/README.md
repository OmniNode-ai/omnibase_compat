# omnibase_compat Documentation

**Owner:** `omnibase_compat`
**Last verified:** 2026-04-24
**Verification:** OMN-9597 docs pass

This is the canonical docs map for `omnibase_compat`.

## Start Here

- [Root README](../README.md) - repo role, install, dependency boundary, common workflows, and docs map.
- [Release workflow](runbooks/release.md) - stable release runbook promoted from the OMN-9459 dated plan.
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

- `types/type_json.py` - shared JSON typing.
- `routing/` - routing policy and degraded-routing event DTOs.
- `telemetry/` - post-mortem, session bootstrap, and sweep result DTOs.
- `overseer/` - routing decision and session contract DTOs.
- `registration/` - idempotent registration helper.
- `concurrency/` - synchronous coroutine bridge utility.
- `env/` - strict-mode environment helper.

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

## Reference

- [Package source](../src/omnibase_compat/)
- [No-upstream-dependency validator](../scripts/validate_no_upstream_deps.py)
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
uv run python scripts/check_compat_retention.py
uv run ruff check src/
uv run mypy src/omnibase_compat --strict
uv run pytest src/omnibase_compat/tests/ -m unit --tb=short
uv build
```

Docs validation must not add an OmniNode runtime dependency. If link validation
is needed before a standalone local entrypoint exists here, run it as CI-only
tooling or from the repo that owns the validator.

## Historical Context

- [OMN-9459 release workflow plan](plans/omn-9459-release-workflow.md) - source plan for the stable [release runbook](runbooks/release.md).

