# OMN-9459 — Add publish release workflow for omnibase_compat

## Epic / Ticket

- Linear: [OMN-9459](https://linear.app/omninode/issue/OMN-9459)
- PR: [omnibase_compat#76](https://github.com/OmniNode-ai/omnibase_compat/pull/76)

## Goal

Add `.github/workflows/release.yml` to `omnibase_compat` so it can publish to PyPI on
version tags / `workflow_dispatch`, matching the established `omnibase_*` release
pattern (modeled on `omnibase_spi/.github/workflows/release.yml`).

## Approach

Copy the `omnibase_spi` release workflow verbatim; only diverge on the dispatch-input
example version to match the current `omnibase_compat` `pyproject.toml`. No
dependency-cascade logic is needed — `omnibase_compat` has zero upstream runtime deps.

## Phases

1. **Author workflow** — done in commit `a37f8d3`.
2. **CI gates** — all passing on PR #76 except the CodeRabbit thread gate.
3. **Resolve CodeRabbit threads** — address the one open Major finding on
   line 99 (use `steps.tag.outputs.tag` instead of `github.ref_name` for
   `prerelease` detection, so `rc` tags are not misclassified as stable when
   the workflow is fired via `workflow_dispatch` from a branch context).
4. **Merge via auto-merge queue** once the gate clears.

## DoD (mirrors the Linear ticket)

- [x] `omnibase_compat/.github/workflows/release.yml` exists
- [x] Matches the `omnibase_*` publish pattern
- [x] Tag/version mismatch fails fast
- [x] Wheel + sdist published via `uv publish` with `PYPI_TOKEN`
- [x] GitHub Release created with artifacts attached
- [ ] CodeRabbit review threads resolved
- [ ] PR merged
