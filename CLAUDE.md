# CLAUDE.md

This file provides guidance to Claude Code when working with the `omnibase_compat` repository.

---

> **TEMPORARY SHIM ONLY — NOT A PERMANENT HOME**
>
> `omnibase_compat` is a migration shim. Every model, protocol, or enum here must have a declared migration target and removal date. Do **not** add new models to this repo as a permanent home — they belong in the canonical repo for their domain (e.g. `omnibase_core`, `omnibase_spi`, `onex_change_control`).
>
> Models without a `COMPAT_REMOVAL_DATE` comment are flagged as stale by CI after 30 days.

---

## What This Repo Is

`omnibase_compat` is a **temporary shim layer** used during cross-repo migrations. It provides cross-repo enums, wire DTOs, event envelopes, primitives, and experimental schemas only for as long as needed to complete a migration. It has **zero upstream runtime dependencies** on other OmniNode packages (pydantic and typing-extensions only).

**This is not a permanent home for any model or protocol.** Once a migration is complete, the compat version must be removed.

---

## Compat Retention Policy

Every module added to `omnibase_compat` must carry a retention comment:

```python
# COMPAT_MIGRATION_TARGET: omnibase_core.models.foo
# COMPAT_REMOVAL_DATE: YYYY-MM-DD
```

Both lines are required. The CI check `scripts/check_compat_retention.py` enforces this:

- Any `.py` file under `src/omnibase_compat/` that defines a class **without** a `COMPAT_REMOVAL_DATE` comment will fail CI if the file was committed more than 30 days ago.
- Files exempt from this check: `__init__.py`, files with `# compat-skip-retention: <reason>` in the first 10 lines.

**When adding a module to compat:**

1. Determine the canonical destination repo and path.
2. Add both `COMPAT_MIGRATION_TARGET` and `COMPAT_REMOVAL_DATE` comments.
3. Create a follow-up ticket to complete the migration before the removal date.

**When the migration is complete:**

1. Remove the module from `omnibase_compat`.
2. Update any consumers to import from the canonical location.
3. Bump the compat package version and release.

---

## SPDX Headers

All source files in `src/`, `tests/`, `scripts/`, `examples/` require MIT SPDX headers.
Canonical spec: `omnibase_core/docs/conventions/FILE_HEADERS.md`

- Stamp missing headers: `onex spdx fix src scripts`
- Check without writing: `onex spdx fix --check src && onex spdx fix --check scripts`
- Bypass a file: add `# spdx-skip: <reason>` in the first 10 lines

---

## Development Setup

```bash
# Install dev dependencies (includes omnibase_core as dev-only dep)
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Run tests
uv run pytest
```

---

## Key Rules

- **Zero runtime upstream deps**: `[project.dependencies]` contains only `pydantic` and `typing-extensions`. Never add OmniNode packages there.
- `omnibase_core` is a **dev-only** dependency (in `[dependency-groups] dev`) for tooling (SPDX, pre-commit hooks). It is NOT a runtime dep.
