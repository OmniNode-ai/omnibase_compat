# CLAUDE.md

This file provides guidance to Claude Code when working with the `omnibase_compat` repository.

---

## What This Repo Is

`omnibase_compat` is a thin shared structural package providing cross-repo enums, wire DTOs, event envelopes, primitives, and experimental schemas. It has **zero upstream runtime dependencies** on other OmniNode packages (pydantic and typing-extensions only).

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
