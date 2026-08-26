# Contributing

## Development Setup

```bash
uv sync --dev --frozen
pre-commit install
```

## Required Checks

```bash
uv run python scripts/validate_no_upstream_deps.py
uv run python scripts/check_compat_retention.py
uv run ruff check src/
uv run mypy src/omnibase_compat --strict
uv run pytest -m unit --tb=short
uv build
```

`pytest` must run with no positional path so it inherits `testpaths` from
`pyproject.toml` (`src/omnibase_compat/tests` and the root `tests/` — OMN-15541).
Passing `src/omnibase_compat/tests/` explicitly silently drops the root
`tests/` directory from collection.

## Compatibility Rules

- Do not add runtime imports from `omnibase_core`, `omnibase_spi`, or `omnibase_infra`.
- Do not copy implementation behavior from canonical owner repos.
- Add `COMPAT_MIGRATION_TARGET` and `COMPAT_REMOVAL_DATE` to class-like compatibility artifacts.
- Keep package-root exports non-authoritative; consumers should import explicit submodules.
- Document new public compatibility surfaces in [docs/README.md](docs/README.md).

## Release Changes

Release changes must update:

- `[project].version` in `pyproject.toml`
- [CHANGELOG.md](CHANGELOG.md)
- Any changed docs under `docs/`

