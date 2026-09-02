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
# Install dev dependencies
uv sync --dev --frozen

# Install pre-commit hooks
pre-commit install
```

## Commands

```bash
uv run pytest -m unit                      # unit tests
uv run ruff check src/                     # lint
uv run mypy src/omnibase_compat --strict   # type check
uv build && uv pip install dist/*.whl      # build + install check
pre-commit run --all-files                 # full local gate
```

Run `pytest` with no positional path so it inherits `testpaths` from
`pyproject.toml` (`src/omnibase_compat/tests` and the root `tests/` —
OMN-15541). Passing `src/omnibase_compat/tests/` explicitly silently drops the
root `tests/` directory from collection.

## Navigation

- Package structure: `src/omnibase_compat/`
- Role vs `omnibase_spi`, install, and usage: `README.md`
- Contribution flow (setup, required checks, release changes):
  [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)
- Shared cross-repo development standards: `~/.claude/CLAUDE.md`
- Everything else — structural inventory, release runbook, architecture — is in
  the knowledge base, not in this repository. See the Documentation section of
  `README.md`.

---

## Key Rules

- **Zero runtime upstream deps**: `[project.dependencies]` contains only `pydantic` and `typing-extensions`. Never add OmniNode packages there.
- `omnibase_core` is **not in `pyproject.toml`** at all — neither as a runtime dep nor in `[dependency-groups] dev`. It appears only as an `additional_dependencies` entry (an isolated git-pinned hook environment, not a `pyproject.toml`/`uv.lock` edge) inside two `.pre-commit-config.yaml` hooks: `normalization-symmetry` and `no-noncanonical-lifecycle-classes` (OMN-14350). Do not add it to pyproject; the no-infra-edge guard (`scripts/check_no_infra_edge.py`, wired as a pre-commit hook) will fail if any OmniNode upstream package appears in `pyproject.toml` or `uv.lock`.
- **Import from explicit submodules**, not the package root. Package-root
  exports are convenience only, not the stable compatibility surface.
- **Document new public compatibility surfaces in the knowledge base**, not in
  this repository. This repo holds no prose documentation directory.
