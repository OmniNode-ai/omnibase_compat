# Release Workflow

**Owner:** `omnibase_compat`
**Last verified:** 2026-08-26
**Verification:** `.github/workflows/release.yml`, `pyproject.toml`, verified on docs refresh (OMN-16549)
**Source plan:** `docs/plans/release-workflow.md`

This is the canonical release runbook for publishing `omnibase_compat`.

## Truth Boundary

The dated release workflow plan is historical execution context. This runbook is the
stable release procedure.

## Preconditions

- The intended version is set in `[project].version` in `pyproject.toml`.
- The working tree is clean before tagging.
- CI passes on the release candidate branch.
- `PYPI_TOKEN` is configured in GitHub repository secrets.
- The release uses the `.github/workflows/release.yml` workflow.

## Release By Tag

1. Confirm the package version:

   ```bash
   rg -n '^version = ' pyproject.toml
   ```

2. Run the local validation path:

   ```bash
   uv sync --dev --frozen
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

3. Create and push a matching version tag:

   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

4. Watch the GitHub Actions `Release` workflow.

## Release By Workflow Dispatch

Use `workflow_dispatch` only when re-running a release from an existing tag.
Pass the full tag, including the `v` prefix.

Example:

```text
vX.Y.Z
```

The workflow checks out that tag and validates it against `pyproject.toml`.

## Workflow Guarantees

The release workflow:

- Fails if the working tree is not clean after checkout.
- Fails if the tag does not match `[project].version`.
- Builds a wheel and source distribution with `uv build`.
- Publishes both artifacts with `uv publish`.
- Generates `SHA256SUMS.txt`.
- Creates a GitHub Release with the artifacts attached.
- Marks releases whose tag contains `rc` as prerelease.

## Dependency Policy During Release

Do not add OmniNode packages as runtime dependencies to support release or docs
tooling. `omnibase_compat` may use tooling in CI or dev contexts, but runtime
dependencies must stay limited to the package's structural support dependencies.

## Failure Handling

- Tag/version mismatch: update `pyproject.toml` or create the correct tag, then rerun.
- Build failure: fix package metadata or source issues, then create a new commit and tag.
- Publish failure: verify `PYPI_TOKEN`, PyPI project permissions, and whether the version already exists.
- GitHub Release failure after PyPI publish: rerun workflow dispatch for the same tag after confirming artifacts exist.

