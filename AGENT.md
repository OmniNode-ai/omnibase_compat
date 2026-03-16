# AGENT.md — omnibase_compat

> LLM navigation guide. Points to context sources — does not duplicate them.
> May contain local paths meaningful only in developer environments.

## Getting Context

- **Repo conventions**: read `CLAUDE.md`
- **Package structure**: read `src/omnibase_compat/`

## Commands

- Tests: `uv run pytest -m unit`
- Lint: `uv run ruff check src/`
- Type check: `uv run mypy src/omnibase_compat --strict`
- Build: `uv build && uv pip install dist/*.whl`
- Pre-commit: `pre-commit run --all-files`

## Cross-Repo

- Shared platform standards: `~/.claude/CLAUDE.md`
- Role vs omnibase_spi: see `README.md` § "Role vs omnibase_spi"

## Rules

- Zero upstream runtime deps by design — never import omnibase_core, omnibase_spi, or omnibase_infra
- CI enforces this via `validate_no_upstream_deps.py` (AST scan)
- Import from explicit submodules, not package root
